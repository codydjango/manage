import click

from rich.console import Console

from em.app import App
from em.storage import NoteStorage

console = Console()

def get_clipboard():
    import pyperclip
    return pyperclip.paste()


from abc import ABC

from typing import List

from rich.console import Console

console = Console()


def output(content: List):
    from rich.table import Table

    table = Table(title="Notes")
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Note", style="magenta")

    for item in content:
        table.add_row(str(item[0]), item[1])

    console.print(table)


class Notes(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('debug'):
            self._log(args)
            self._log(kwargs)

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

    def reset(self):
        if not click.confirm(f'Are you sure you want to reset the {self.__class__} table?'):
            return

        with self.storage_cls() as store:
            self.log(f'resetting the {self.__class__} table...')
            store.reset()
            self.log(f'{self.__class__} table reset.')

    def add(self, note: str):
        with self.storage_cls() as store:
            store.add(note)

    def remove(self, pk: str):
        if not click.confirm(f'Are you sure you want to delete the item?'):
            return

        with self.storage_cls() as store:
            store.remove(pk)

    def output(self):
        with self.storage_cls() as store:
            output(store.get())
