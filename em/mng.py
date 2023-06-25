#!/usr/bin/env python3

import click

from em.notes import Notes
from em.todo import Todo

@click.command()
@click.argument('app')
@click.option('-m', '--message', help="A message to store, similar to a git commit message.")
@click.option('-cb', '--clipboard', default=False, is_flag=True, help="Paste from clipboard.")
@click.option('-d', '--delete', help="delete an entity by it's primary key.")
@click.option('-t', '--tag', help="Add a tag to the note to keep things organized.")
@click.option('-p', '--person', help="A specialized tag for people.")
@click.option('-db', '--debug', default=False, is_flag=True, help="Enable debug mode.")
@click.option('-r', '--reset', default=False, is_flag=True, help="Reset DB.")
@click.option('-tw', '--weight', help="Task weight.")
@click.option('-tp', '--points', help="Task points.")
@click.option('-tc', '--complete', help="Mark a task as complete.")
def main(app, *args, **kwargs):
    """Entrypoint for the commandline application."""

    try:
        {'nt': Notes, 'td': Todo}[app](*args, **kwargs)
    except KeyError:
        click.echo('Invalid app: {}'.format(app))


if __name__ == '__main__':
    main()
