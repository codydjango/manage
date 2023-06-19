import sqlite3
import os
from pathlib import Path

DATABASE_PATH = os.path.join(Path(__file__).resolve().parent, 'database.db')

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

class ConnectionException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

class Storage:
    def __init__(self):
        try:
            self.conn = get_connection()
        except Exception as e:
            raise ConnectionException(*e.args, **e.kwargs)
        self._complete = False

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

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

class NoteStorage(Storage):
    def create_table(self):
        try:
            self.conn.cursor().execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT)')
        except Exception as e:
            print(*e.args)
            raise ConnectionException('error creating notes table')
    def add(self, note: str):
        try:
            self.conn.cursor().execute('INSERT INTO notes (note) VALUES (?)', (note,))
        except Exception as e:
            print(*e.args)
            raise ConnectionException('error storing note')

    def remove(self, pk: str):
        try:
            self.conn.cursor().execute('DELETE FROM notes WHERE id=(?)', (pk,))
        except Exception as e:
            print(*e.args)
            raise ConnectionException('error removing note')

    def get(self):
        data = []
        try:
            for r in self.conn.cursor().execute('SELECT * FROM notes'):
                data.append((r[0], r[1]))
            return data
        except Exception as e:
            print(*e.args)
            raise ConnectionException('error getting notes')