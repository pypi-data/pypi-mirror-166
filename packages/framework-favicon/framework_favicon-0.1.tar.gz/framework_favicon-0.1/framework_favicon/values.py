# the website url from where to grab the favicon hashes.
hashes_url = "https://wiki.owasp.org/index.php/OWASP_favicon_database"

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
                  AppleWebKit/537.11 (KHTML, like Gecko) \
                  Chrome/23.0.1271.64 \
                  Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}


def get_error(resource: str) -> str:
    return f'could not determine framework for {resource} based on favicon provided' \
        "please try other ways to determine the framework, "\
        "if you do manage to determine the favicon, update the OWASP database if possible\n" \
        'database can be found in {hashes_url}'


def get_info(resource: str, name: str) -> str:
    return f'framework {name} found for resource {resource}'
