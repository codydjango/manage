from typing import List
import click

from rich import print as rprint
from rich.pretty import pprint
from rich.console import Console

from storage import NoteStorage

console = Console()

def get_clipboard():
    import pyperclip
    return pyperclip.paste()



class TableOutput:
    def output_all(self, content: List):
        from rich.table import Table
        table = Table(title="Notes")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Note", style="magenta")
        table.add_column("Tags", style="green")
        table.add_column("Timestamp", justify="right", style="blue")

        for item in content:
            table.add_row(str(item[0]), item[1], item[2], item[3])

        console.print(table)

class App:
    def __init__(self, *args, **kwargs):
        self.output_engine = TableOutput()
    def output_all(self, content):
        # click.echo(message)
        # pprint(message, expand_all=True)
        self.output_engine.output_all(content)
        # console.log(message)

    def _log(self, message):
        console.log(message)

    def log(self, message):
        self._log(message)

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
        if not click.confirm('Are you sure you want to reset the note table?'):
            return

        with NoteStorage() as store:
            self.log(f'resetting the note table...')
            store.reset()
            self.log(f'note table reset.')

    def add(self, note: str):
        with NoteStorage() as store:
            store.add(note)

    def output(self):
        with NoteStorage() as store:
            self.output_all(store.get())

    def remove(self, pk: str):
        with NoteStorage() as store:
            store.remove(pk)
