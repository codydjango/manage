import sqlite3
import json

from abc import ABC, abstractmethod
from em.settings import DEBUG, get_database_path, get_export_path


def get_connection():
    pth = get_database_path()
    try:
        conn = sqlite3.connect(pth)
    except sqlite3.OperationalError as e:
        raise ConnectionException(f'Unable to connect to database using path: {pth}', e.args)
    return conn

class ConnectionException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

class SqliteAdapter:
    def __init__(self):
        self.conn = get_connection()
        self.conn.row_factory = sqlite3.Row
        self._complete = False

    def execute(self, sql, params=()):
        if DEBUG:
            print(sql, params)
        return self.conn.cursor().execute(sql, params)

    def commit(self):
        self._complete = True

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise ConnectionException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise ConnectionException(*e.args)


class StorageInterface(ABC):
    @abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def remove(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def reset(self, *args, **kwargs):
        raise NotImplementedError()

class Storage:
    def __init__(self):
        self.engine = SqliteAdapter()
        self.table_name = None

    @property
    def export_path(self):
        return get_export_path(f'{self.table_name}.json')

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.engine.close()

    def export(self):
        rows = self.engine.execute(f'SELECT * FROM {self.table_name}', ()).fetchall()
        with open(self.export_path, 'w') as the_file:
            for row in rows:
                the_file.write(json.dumps(dict(row)))
                the_file.write('\n')



























