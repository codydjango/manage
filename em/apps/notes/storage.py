from em.storage import Storage, StorageInterface, ConnectionException


class NoteStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__()
        self.table_name = 'notes'

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
                data.append(dict(r))
            return data
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)
