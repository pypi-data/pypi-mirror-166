import argparse
from os import path
import sys
from .database import show_database, database
from .utils import database_location, handle_response
from .grabbers import grab_favicon_from_data
from .grabbers import grab_favicon_from_file
from .grabbers import grab_favicon_from_website
from .grabbers import grab_favicon_from_md5
from framework_favicon.utils import update_hashes_database


parser = argparse.ArgumentParser(description="Framework Guesser from favicon")
parser.add_argument(
    '-u',
    '--url',
    action='append',
    help='website url from which to get favicon'
)
parser.add_argument(
    '-f',
    '--file',
    action='append',
    help='faveicon file, could be local or url'
)
parser.add_argument(
    '-d',
    '--data',
    action='append',
    help='faveicon file data, not recommended to use, but what the hell'
)
parser.add_argument(
    '-m',
    '--md5',
    action='append',
    help='faveicon md5 hash'
)
parser.add_argument(
    '--update',
    action='store_true',
    help='update the hashes database'
)
parser.add_argument(
    "--show_database",
    action='store_true',
    help='show the current database'
)


def main_cli():
    """
    Main function. Expected to be run from CLI.
    """
    try:
        args = parser.parse_args()
    except Exception:
        parser.print_help()
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    if args.update or not path.exists(database_location):
        update_hashes_database()
    # make sure data is up to date
    database.update_frameworks()
    if args.show_database:
        show_database()

    if args.url:
        for url in args.url:
            handle_response(url, grab_favicon_from_website)
    if args.file:
        for file in args.file:
            handle_response(file, grab_favicon_from_file)
    if args.data:
        for data in args.data:
            handle_response(data, grab_favicon_from_data)
    if args.md5:
        for md5 in args.md5:
            handle_response(md5, grab_favicon_from_md5)


if __name__ == "__main__":
    main_cli()
