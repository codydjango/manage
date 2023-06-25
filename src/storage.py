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

    def execute(self, sql, params=()):
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
    def __enter__(self):
        raise NotImplementedError()

    @abstractmethod
    def __exit__(self, type_, value, traceback):
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
            raise ConnectionException('error dropping table', *e.args)

        try:
            self.engine.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT, timestamp TEXT)')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException(f'error creating table', *e.args)

    def add(self, note: str):
        try:
            self.engine.execute(f'INSERT INTO {self.table_name} (note, timestamp) VALUES (?, CURRENT_TIMESTAMP)', (note,))
            self.engine.commit()
        except Exception as e:
            print(e)
            raise ConnectionException('error storing item', *e.args)

    def remove(self, pk: str):
        try:
            self.engine.execute(f'DELETE FROM {self.table_name} WHERE id=(?)', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting item', *e.args)

    def get(self):
        data = []
        try:
            for r in self.engine.execute(f'SELECT * FROM {self.table_name}'):
                data.append(r)
            return data
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)


class TodoStorage(StorageInterface):
    def __init__(self):
        self.engine = SqliteAdapter()
        self.table_name = 'todo'

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.engine.close()

    def reset(self):
        try:
            self.engine.execute(f'DROP TABLE IF EXISTS {self.table_name}')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting table', *e.args)

        try:
            self.engine.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                                f'('
                                f'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                f'task TEXT, '
                                f'weight INTEGER, '
                                f'points INTEGER, '
                                f'completed INTEGER DEFAULT 0, '                                   
                                f'timestamp TEXT '
                                f'timestamp_complete TEXT '
                                f')')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException(f'error creating table', *e.args)

    def add(self, task: str, weight: int, points: int):
        try:
            self.engine.execute(f'INSERT INTO {self.table_name} (task, weight, points, timestamp) VALUES ('
                                f'?, '
                                f'?, '
                                f'?, '
                                f'CURRENT_TIMESTAMP)', (task, weight, points))
            self.engine.commit()
        except Exception as e:
            print(e)
            raise ConnectionException('error storing item', *e.args)

    def complete(self, pk: str):
        try:
            self.engine.execute(f'UPDATE {self.table_name} set completed = 1 and timestamp_complete = CURRENT_TIMESTAMP WHERE id = ?', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting item', *e.args)

    def remove(self, pk: str):
        try:
            self.engine.execute(f'DELETE FROM {self.table_name} WHERE id=(?)', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting item', *e.args)

    def get(self, complete: bool = False):
        data = []
        try:
            for r in self.engine.execute(f'SELECT id, weight, points, task FROM {self.table_name} WHERE completed = ? ORDER BY weight DESC', (1 if complete else 0,)):
                data.append(r)
            return data
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)