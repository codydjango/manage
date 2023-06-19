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

class SqliteEngine:
    def __init__(self):
        try:
            self.conn = get_connection()
        except Exception as e:
            raise ConnectionException(*e.args, **e.kwargs)
        self._complete = False

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
        self.engine = SqliteEngine()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.engine.close()

    def setup(self):
        try:
            self.engine.conn.cursor().execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT)')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error creating notes table', *e.args)

    def add(self, note: str):
        try:
            self.engine.conn.cursor().execute('INSERT INTO notes (note) VALUES (?)', (note,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error storing note', *e.args)

    def remove(self, pk: str):
        try:
            self.engine.conn.cursor().execute('DELETE FROM notes WHERE id=(?)', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error removing note', *e.args)

    def get(self):
        data = []
        try:
            for r in self.engine.conn.cursor().execute('SELECT * FROM notes'):
                data.append((r[0], r[1]))
            return data
        except Exception as e:
            raise ConnectionException('error getting notes', *e.args)