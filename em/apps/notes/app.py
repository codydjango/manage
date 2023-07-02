from em.app import App
from typing import List

from rich.console import Console
from rich.table import Table

from .storage import NoteStorage

console = Console()

APPNAME = 'notes'


def get_clipboard():
    import pyperclip
    return pyperclip.paste()


def output(content: List):
    table = Table(title=APPNAME.capitalize())
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Note", style="magenta")

    for item in content:
        table.add_row(str(item['id']), item['note'])

    console.print(table)

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
