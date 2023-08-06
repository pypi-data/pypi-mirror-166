import logging
from .utils import deserialize_hashes, default_logger


class database:
    framworks = deserialize_hashes()

    def update_frameworks():
        database.framworks = deserialize_hashes()


def show_database(logger: logging.Logger = default_logger) -> None:
    logger.info(f'database contains {len(database.framworks)} entries: ')
    res = ""
    for h, f in database.framworks.items():
        res += f"{f}:{h}\n"
    logger.info(res)
    logger.info("happy hacking")
