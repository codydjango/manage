import sqlite3
import json

from abc import ABC, abstractmethod
from em.settings import DEBUG, get_database_path, get_export_path
from em.exceptions import NotFoundException


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
    def __init__(self, *args, **kwargs):
        self.table_name = kwargs.get('table_name', None)
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
    def __init__(self, *args, **kwargs):
        self.engine = SqliteAdapter(table_name=kwargs.get('table_name', None))

    @property
    def export_path(self):
        return get_export_path(f'{self.engine.table_name}.json')

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.engine.close()

    def get_all(self):
        data = []
        for r in self.engine.execute(
                f'SELECT * '
                f'FROM {self.engine.table_name} '
                f'ORDER BY id', ()):
            data.append(dict(r))
        return data

    def get_single(self, pk: int):
        if (row := self.engine.execute(
            f'SELECT * '
            f'FROM {self.engine.table_name} '
            f'WHERE (id = ?) ', (pk,)).fetchone()):
            return dict(row)
        raise NotFoundException(f'No {self.engine.table_name} found with id: {pk}')

    def put(self, pk: int, dct: dict):
        update_columns = ', '.join([f'{k} = ?' for k in dct.keys()])
        self.engine.execute(
            f'UPDATE {self.engine.table_name} SET {update_columns} WHERE id = ?', list(dct.values()) + [pk])

    def commit(self):
        self.engine.commit()

    def export(self):
        rows = self.engine.execute(f'SELECT * FROM {self.engine.table_name}', ()).fetchall()
        with open(self.export_path, 'w') as the_file:
            for row in rows:
                the_file.write(json.dumps(dict(row)))
                the_file.write('\n')
