#!/usr/bin/env python3

import click
import rich

from rich import print as rprint
from rich.pretty import pprint
from rich.console import Console

# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name', help='The person to greet.')
# def mng(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo(f"Hello {name}!")

from storage import NoteStorage

console = Console()

class App:
    def _output(self: str, message):
        # click.echo(message)
        pprint(message, expand_all=True)
        # console.log(message)

    def _log(self, message):
        console.log(message)

class Notes(App):
    def __init__(self, *args, **kwargs):
        self._log(args)
        self._log(kwargs)

        delete = kwargs.get('delete')
        message = kwargs.get('message')

        if message:
            self.add(note=message)
        elif delete:
            self.remove(pk=delete)
        else:
            self.output()

    def init(self):
        with NoteStorage() as store:
            store.create_table()
            store.commit()
    def add(self, note: str):
        with NoteStorage() as store:
            store.add(note)
            store.commit()

    def output(self):
        with NoteStorage() as store:
            self._output(store.get())

    def remove(self, pk: str):
        with NoteStorage() as store:
            store.remove(pk)
            store.commit()


@click.command()
@click.argument('app')
@click.option('-m', '--message')
@click.option('-d', '--delete')
def mng(app, *args, **kwargs):
    """entrypoint"""

    if app == 'nt':
        Notes(*args, **kwargs)

if __name__ == '__main__':
    mng()
