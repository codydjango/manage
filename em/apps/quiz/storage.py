from em.storage import Storage, StorageInterface


class NoteStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__(table_name='notes')

    def reset(self):
        self.engine.execute(f'DROP TABLE IF EXISTS {self.engine.table_name}')
        self.engine.execute(f'CREATE TABLE IF NOT EXISTS {self.engine.table_name} '
                            f'(id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT, timestamp TEXT)')

    def add(self, note: str):
        self.engine.execute(f'INSERT INTO {self.engine.table_name} (note, timestamp) '
                            f'VALUES (?, CURRENT_TIMESTAMP)', (note,))

    def remove(self, pk: str):
        self.engine.execute(f'DELETE FROM {self.engine.table_name} WHERE id=(?)', (pk,))

    def get(self):
        data = []
        for r in self.engine.execute(f'SELECT * FROM {self.engine.table_name}'):
            data.append(dict(r))
        return data
