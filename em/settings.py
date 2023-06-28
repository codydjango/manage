import os
from appdirs import user_data_dir, site_data_dir, user_cache_dir, user_log_dir

APPNAME = 'EM'
APPAUTHOR = 'codydjango'

DEBUG = False

DATABASE_PATH = os.path.join('/home/codydjango/work/manage/em', 'database.db')

def get_database_path():
    pth = user_data_dir(APPNAME, APPAUTHOR)
    print(pth)
    return DATABASE_PATH
    # return pth

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