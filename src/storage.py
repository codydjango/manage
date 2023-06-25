import sqlite3
import os
from abc import ABC, abstractmethod
from pathlib import Path

DATABASE_PATH = os.path.join(Path(__file__).resolve().parent, 'database.db')

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

class ConnectionException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

class SqliteAdapter:
    def __init__(self):
        try:
            self.conn = get_connection()
        except Exception as e:
            raise ConnectionException(*e.args, **e.kwargs)
        self._complete = False

    def execute(self, sql):
        self.conn.cursor().execute(sql)

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

class NoteStorage(StorageInterface):
    def __init__(self):
        self.engine = SqliteAdapter()
        self.table_name = 'notes'

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.engine.close()

    def reset(self):
        try:
            self.engine.execute(f'DROP TABLE IF EXISTS {self.table_name}')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error creating notes table', *e.args)

        try:
            self.engine.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT, timestamp TEXT)')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException(f'error creating {self.table_name} table', *e.args)

    def add(self, note: str):
        try:
            self.engine.execute(f'INSERT INTO {self.table_name} (note, timestamp) VALUES (?, CURRENT_TIMESTAMP)', (note,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error storing note', *e.args)

    def remove(self, pk: str):
        try:
            self.engine.execute(f'DELETE FROM {self.table_name} WHERE id=(?)', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error removing note', *e.args)

    def get(self):
        data = []
        try:
            for r in self.engine.execute(f'SELECT * FROM {self.table_name}'):
                data.append(r)
            return data
        except Exception as e:
            raise ConnectionException('error getting notes', *e.args)