#!/usr/bin/env python3

import click

from rich import print as rprint
from rich.pretty import pprint
from rich.console import Console

from storage import NoteStorage

console = Console()

DEBUG = False

class App:
    def _output(self: str, message):
        # click.echo(message)
        pprint(message, expand_all=True)
        # console.log(message)

    def _log(self, message):
        console.log(message)

class Notes(App):
    def __init__(self, *args, **kwargs):
        if DEBUG:
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

    def setup(self):
        with NoteStorage() as store:
            store.setup()

    def add(self, note: str):
        with NoteStorage() as store:
            store.add(note)

    def output(self):
        with NoteStorage() as store:
            self._output(store.get())

    def remove(self, pk: str):
        with NoteStorage() as store:
            store.remove(pk)


@click.command()
@click.argument('app')
@click.option('-m', '--message')
@click.option('-d', '--delete')
@click.option('-db', '--debug', default=False, is_flag=True, help="Enable debug mode.")
def mng(app, *args, **kwargs):
    """entrypoint"""

    global DEBUG

    if kwargs.get('debug'):
        DEBUG = True

    if app == 'nt':
        Notes(*args, **kwargs)

if __name__ == '__main__':
    mng()
