import sqlite3
import json

from abc import ABC, abstractmethod
from em.settings import get_database_path


def get_connection():
    return sqlite3.connect(get_database_path())

class ConnectionException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

class SqliteAdapter:
    def __init__(self):
        try:
            self.conn = get_connection()
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            raise ConnectionException(*e.args, **e.kwargs)
        self._complete = False

    def execute(self, sql, params=()):
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

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.engine.close()

    def export(self):
        data = json.dumps(self.engine.execute(f'SELECT * FROM {self.table_name}', ()).fetchall())
        with open(f'./data/{self.table_name}.json', 'w') as the_file:
            the_file.write(data)


























