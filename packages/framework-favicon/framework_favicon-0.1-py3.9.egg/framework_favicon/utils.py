import os
from typing import Callable
import logging
from rich.logging import RichHandler
from .grab_result import GrabResult, Status
from .framework_hash import FrameworkHash
from .values import get_error, get_info, hashes_url, hdr


logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
default_logger = logging.getLogger("framework_favicon_logger")
default_logger.setLevel(logging.INFO)
dir_path = os.path.dirname(os.path.realpath(__file__))
database_location = os.path.join(dir_path, "database.json")


def obj_dict(obj):
    return obj.__dict__


hash = str
framework = str


def deserialize_hashes(logger: logging.Logger = default_logger) -> dict[hash, framework]:
    import json
    res = {}
    if not os.path.exists(database_location):
        logger.error(f'{database_location} not found, try to update the database.')
        return res
    database_content = json.load(open(database_location, 'r'))
    for framework in database_content:
        res[framework["hash"]] = framework["framework"]
    found = len(res)
    if found > 0:
        logger.info(f'database has {found} hashes.')
    else:
        logger.warn('no hash is found in the database, results may be invalid.')
    return res


def handle_response(
    resource: str,
    action: Callable[[str], GrabResult],
    logger: logging.Logger = default_logger
) -> None:
    response = action(resource)
    if response.status == Status.STATUS_OK:
        logger.info(get_info(resource, response.data))
    if response.status == Status.STATUS_NOT_FOUND:
        logger.error(get_error(resource))


def serialize_hashes(frameworks: list[FrameworkHash]) -> None:
    import json
    open(database_location, "w").write(json.dumps(frameworks, default=obj_dict))


def get_hashes(logger: logging.Logger = default_logger) -> str:
    import urllib.request
    logger.info(f'attempting to get hash database from {hashes_url}')
    req = urllib.request.Request(hashes_url, headers=hdr)
    response = urllib.request.urlopen(req)
    if response.status == 200:
        content = response.read()
    if content:
        logger.info('managed to retrieve answer from website, parsing data')
    else:
        logger.warn(
            'unable to update, falling back on existing database version, results may be invalid'
        )
        return ''
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    return str(soup.pre.text)


def update_hashes_database(logger: logging.Logger = default_logger) -> None:
    logger.info("updating database")
    lis = []
    for line in get_hashes().splitlines():
        hash, framework = line.split(':', 1)
        lis.append(FrameworkHash(framework, hash))
    found = len(lis)
    if (found):
        logger.info(f'found {found} hashes, overwriting existing database')
        serialize_hashes(lis)
        logger.info("database updated")
    else:
        logger.warn('could not find any database, falling back on previous database version')
