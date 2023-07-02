from em.storage import Storage, StorageInterface, ConnectionException


class ReminderStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__()
        self.table_name = 'reminder'

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
                                f'message TEXT, '                                 
                                f'reminder_timestamp TEXT, '
                                f'timestamp TEXT'
                                f')')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException(f'error creating table', *e.args)

    def add(self, message: str, date: str):
        try:
            self.engine.execute(f'INSERT INTO {self.table_name} (message, reminder_timestamp, timestamp) VALUES ('
                                f'?, '
                                f'?, '
                                f'CURRENT_TIMESTAMP)', (message, date))
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

    def get(self, complete: bool = False):
        data = []
        try:
            for r in self.engine.execute(f'SELECT id, message, reminder_timestamp FROM {self.table_name} ORDER BY reminder_timestamp DESC', ()):
                data.append(dict(r))
            return data
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)
