from em.storage import Storage, StorageInterface, ConnectionException


class TodoStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__()
        self.table_name = 'todo'


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
                                f'timestamp TEXT, '
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
            self.engine.execute(f'UPDATE {self.table_name} set completed = 1, timestamp_complete = CURRENT_TIMESTAMP WHERE id = ?', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error completing item', *e.args)

    def remove(self, pk: str):
        try:
            self.engine.execute(f'DELETE FROM {self.table_name} WHERE id=(?)', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting item', *e.args)

    def get(self, complete: bool = False):
        data = []
        try:
            for r in self.engine.execute(f'SELECT id, weight, points, task, timestamp, timestamp_complete FROM {self.table_name} WHERE completed = ? ORDER BY weight DESC', (1 if complete else 0,)):
                data.append(dict(r))
            return data
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)

    def get_points(self):
        try:
            row = self.engine.execute(f'SELECT SUM(points) FROM {self.table_name} WHERE completed = 1', ()).fetchone()
            return row[0]
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)
