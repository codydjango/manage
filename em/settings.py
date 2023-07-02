import os
from appdirs import user_data_dir, site_data_dir, user_cache_dir, user_log_dir

APPNAME = 'EM'
APPAUTHOR = 'codydjango'
DB_NAME = 'database.db'
DEBUG = False

def get_database_path():
    pth = os.path.join(user_data_dir(APPNAME, APPAUTHOR), DB_NAME)
    print(pth)

    if not os.path.exists(pth):
        os.makedirs(pth)

    return pth

def get_fixture_path():
    pth = site_data_dir(APPNAME, APPAUTHOR)
    print(pth)
    return pth

def get_log_path():
    pth = user_log_dir(APPNAME, APPAUTHOR)
    print(pth)
    return pth

def set_debug(debug: bool):
    global DEBUG
    DEBUG = debug