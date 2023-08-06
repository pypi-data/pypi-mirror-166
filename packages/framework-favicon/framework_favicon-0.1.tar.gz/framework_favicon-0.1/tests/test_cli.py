import unittest
from framework_favicon.main import parser
import sys
try:
    # python 3.4+ should use builtin unittest.mock not mock package
    from unittest.mock import patch
except ImportError:
    from mock import patch


class TestCli(unittest.TestCase):
    def test_cli_update(self):
        testargs = ["framework_favicon", "--update"]
        with patch.object(sys, 'argv', testargs):
            args = parser.parse_args()
            self.assertTrue(args.update)
            self.assertFalse(args.show_database)
            self.assertIsNone(args.md5)
            self.assertIsNone(args.data)
            self.assertIsNone(args.file)
            self.assertIsNone(args.url)

    def test_cli_show_database(self):
        testargs = ["framework_favicon", "--show_database"]
        with patch.object(sys, 'argv', testargs):
            args = parser.parse_args()
            self.assertFalse(args.update)
            self.assertTrue(args.show_database)
            self.assertIsNone(args.md5)
            self.assertIsNone(args.data)
            self.assertIsNone(args.file)
            self.assertIsNone(args.url)

    def test_cli_urls(self):
        command = "--url"
        urls = ['website_one', 'website_two']
        testargs = ["framework_favicon"] + [f'{command}={x}' for x in urls]
        with patch.object(sys, 'argv', testargs):
            args = parser.parse_args()
            self.assertFalse(args.update)
            self.assertFalse(args.show_database)
            self.assertIsNone(args.md5)
            self.assertIsNone(args.data)
            self.assertIsNone(args.file)
            self.assertEqual(args.url, urls)

    def test_cli_md5(self):
        command = "--md5"
        md5 = ['md5_one', 'md5_two']
        testargs = ["framework_favicon"] + [f'{command}={x}' for x in md5]
        with patch.object(sys, 'argv', testargs):
            args = parser.parse_args()
            self.assertFalse(args.update)
            self.assertFalse(args.show_database)
            self.assertIsNone(args.url)
            self.assertIsNone(args.data)
            self.assertIsNone(args.file)
            self.assertEqual(args.md5, md5)

    def test_cli_data(self):
        command = "--data"
        datas = ['data_one', 'data_two']
        testargs = ["framework_favicon"] + [f'{command}={x}' for x in datas]
        with patch.object(sys, 'argv', testargs):
            args = parser.parse_args()
            self.assertFalse(args.update)
            self.assertFalse(args.show_database)
            self.assertIsNone(args.md5)
            self.assertIsNone(args.url)
            self.assertIsNone(args.file)
            self.assertEqual(args.data, datas)

    def test_cli_file(self):
        command = "--file"
        files = ['file_one', 'file_two']
        testargs = ["framework_favicon"] + [f'{command}={x}' for x in files]
        with patch.object(sys, 'argv', testargs):
            args = parser.parse_args()
            self.assertFalse(args.update)
            self.assertFalse(args.show_database)
            self.assertIsNone(args.md5)
            self.assertIsNone(args.data)
            self.assertIsNone(args.url)
            self.assertEqual(args.file, files)


if __name__ == "__main__":
    unittest.main()
