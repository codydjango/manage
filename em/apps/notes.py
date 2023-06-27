from typing import List
from rich.console import Console

from em.app import App
from em.storage import StorageInterface, Storage, ConnectionException

console = Console()

APPNAME = 'notes'

def get_clipboard():
    import pyperclip
    return pyperclip.paste()


def output(content: List):
    from rich.table import Table

    table = Table(title=APPNAME.capitalize())
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Note", style="magenta")

    for item in content:
        table.add_row(str(item['id']), item['note'])

    console.print(table)



class NoteStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__()
        self.table_name = APPNAME.lower()

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


class Notes(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        reset = kwargs.get('reset')
        delete = kwargs.get('delete')
        message = kwargs.get('message')
        clipboard = kwargs.get('clipboard')

        self.storage_cls = NoteStorage

        if reset:
            self.reset()
        elif message:
            self.add(note=message)
        elif clipboard:
            self.add(note=get_clipboard())
        elif delete:
            self.remove(pk=delete)
        else:
            self.output()

    def add(self, note: str):
        with self.storage_cls() as store:
            store.add(note)

    def output(self):
        with self.storage_cls() as store:
            output(store.get())
