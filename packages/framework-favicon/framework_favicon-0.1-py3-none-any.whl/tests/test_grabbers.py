import unittest
from framework_favicon.grab_result import Status
from framework_favicon.grabbers import grab_favicon_from_file, grab_favicon_from_md5
from .test_base import TestBase
from .values import favicon_md5_test, favicon_url_test, favicon_file_location_test


class TestGrabbers(TestBase):
    def test_local_file_grabber(self):
        result = grab_favicon_from_file(favicon_file_location_test)
        self.assertEqual(result.status, Status.STATUS_OK)
        self.assertEqual(result.data, 'cgiirc (0.5.9)')

    def test_remote_file_grabber(self):
        result = grab_favicon_from_file(favicon_url_test)
        self.assertEqual(result.status, Status.STATUS_OK)
        self.assertEqual(result.data, 'cgiirc (0.5.9)')

    def test_md5_grabber(self):
        result = grab_favicon_from_md5(favicon_md5_test)
        self.assertEqual(result.status, Status.STATUS_OK)
        self.assertEqual(result.data, 'cgiirc (0.5.9)')


if __name__ == "__main__":
    unittest.main()
