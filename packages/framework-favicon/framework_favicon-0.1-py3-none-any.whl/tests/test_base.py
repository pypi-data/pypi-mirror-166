import unittest
from framework_favicon.utils import update_hashes_database
from framework_favicon.database import database


class TestBase(unittest.TestCase):
    def setUp(self):
        # make sure that the database is up to date
        update_hashes_database()
        database.update_frameworks()
