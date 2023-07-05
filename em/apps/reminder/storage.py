from em.storage import Storage, StorageInterface


class ReminderStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__(table_name='reminder')

    def reset(self):
        self.engine.execute(f'DROP TABLE IF EXISTS {self.engine.table_name}')
        self.engine.execute(f'CREATE TABLE IF NOT EXISTS {self.engine.table_name} '
                            f'('
                            f'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                            f'message TEXT, '                                 
                            f'reminder_timestamp TEXT, '
                            f'timestamp TEXT'
                            f')')

    def add(self, message: str, date: str):
        self.engine.execute(f'INSERT INTO {self.engine.table_name} (message, reminder_timestamp, timestamp) '
                            f'VALUES (?, ?, CURRENT_TIMESTAMP)', (message, date))

    def remove(self, pk: str):
        self.engine.execute(f'DELETE FROM {self.engine.table_name} WHERE id=(?)', (pk,))

    def get(self, complete: bool = False):
        data = []
        for r in self.engine.execute(f'SELECT id, message, reminder_timestamp FROM {self.engine.table_name} '
                                     f'ORDER BY reminder_timestamp DESC', ()):
            data.append(dict(r))
        return data
