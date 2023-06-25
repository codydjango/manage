#!/usr/bin/env python3

import click

from rich import print as rprint
from rich.pretty import pprint
from rich.console import Console

from notes import Notes

console = Console()



@click.command()
@click.argument('app')
@click.option('-m', '--message', help="A message to store, similar to a git commit message.")
@click.option('-cb', '--clipboard', default=False, is_flag=True, help="Paste from clipboard.")
@click.option('-d', '--delete', help="delete an entity by it's primary key.")
@click.option('-t', '--tag', help="Add a tag to the note to keep things organized.")
@click.option('-p', '--person', help="A specialized tag for people.")
@click.option('-db', '--debug', default=False, is_flag=True, help="Enable debug mode.")
@click.option('-r', '--reset', default=False, is_flag=True, help="Reset DB.")
def mng(app, *args, **kwargs):
    """Entrypoint for the application."""

    if app == 'nt':
        Notes(*args, **kwargs)
    else:
        click.echo('Invalid app: {}'.format(app))

if __name__ == '__main__':
    mng()
