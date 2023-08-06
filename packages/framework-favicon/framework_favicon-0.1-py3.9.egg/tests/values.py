import os
favicon_url_test = "https://static-labs.tryhackme.cloud/sites/favicon/images/favicon.ico"
favicon_md5_test = 'f276b19aabcb4ae8cda4d22625c6735f'

dir_path = os.path.dirname(os.path.realpath(__file__))
assets_path = os.path.join(dir_path, "assets")
favicon_file_location_test = os.path.join(assets_path, "favicon_test.ico")
