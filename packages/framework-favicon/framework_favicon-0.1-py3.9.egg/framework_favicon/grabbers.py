from os import path
from .database import database
from .grab_result import GrabResult, Status
from .values import hdr


def grab_favicon_from_md5(md5: str) -> GrabResult:
    if md5 in database.framworks:
        return GrabResult(Status.STATUS_OK, database.framworks[md5])
    else:
        return GrabResult(Status.STATUS_NOT_FOUND, '')


def grab_favicon_from_data(data: bytes) -> GrabResult:
    import hashlib
    return grab_favicon_from_md5(hashlib.md5(data).hexdigest())


def grab_favicon_from_file(file: str) -> GrabResult:
    # local file
    if (path.exists(file)):
        return grab_favicon_from_data(open(file, 'rb').read())
    else:
        import validators
        # internet url
        if validators.url(file):
            import urllib.request
            req = urllib.request.Request(file, headers=hdr)
            with urllib.request.urlopen(req) as f:
                return grab_favicon_from_data(f.read())
    raise FileNotFoundError(f'{file} not found')


def try_grab_favicon_from_file(file: str) -> GrabResult:
    try:
        return grab_favicon_from_file(file)
    except Exception:
        return GrabResult(Status.STATUS_NOT_FOUND, '')


def grab_favicon_from_website(url: str) -> GrabResult:
    import urllib
    from urllib.parse import urlparse, urljoin
    from bs4 import BeautifulSoup
    import re
    req = urllib.request.Request(url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page)
    icon_link = soup.find("link", rel=re.compile("shortcut icon", re.I))['href']

    def is_absolute(url):
        return bool(urlparse(url).netloc)
    if not is_absolute(icon_link):
        icon_link = urljoin(url, icon_link)
    return grab_favicon_from_file(icon_link)


def try_grab_favicon_from_website(url: str) -> GrabResult:
    try:
        return grab_favicon_from_website(url)
    except Exception:
        return GrabResult(Status.STATUS_NOT_FOUND, '')
