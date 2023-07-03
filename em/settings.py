import os
from appdirs import user_data_dir, site_data_dir, user_cache_dir, user_log_dir

APPNAME = 'EM'
APPAUTHOR = 'codydjango'
DB_NAME = 'database.db'
DEBUG = False

def get_database_path() -> str:
    dir_path = user_data_dir(APPNAME, APPAUTHOR)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return os.path.join(dir_path, DB_NAME)

def get_fixture_path() -> str:
    return site_data_dir(APPNAME, APPAUTHOR)

def get_log_path() -> str:
    return user_log_dir(APPNAME, APPAUTHOR)

def set_debug(debug: bool) -> None:
    global DEBUG
    DEBUG = debug