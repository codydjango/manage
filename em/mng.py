#!/usr/bin/env python3

import click

from em.apps import Notes, Todo, Reminder
from em.settings import set_debug


@click.group()
@click.option('-db', '--debug', default=False, is_flag=True, help="Enable debug mode.")
def cli(*args, **kwargs):
    """Entrypoint for the commandline application."""

    set_debug(kwargs.get('debug'))

@click.option('-m', '--message', help="A message describing the task.")
@click.option('-tw', '--weight', help="Task weight.")
@click.option('-tp', '--points', help="Task points.")
@click.option('-tc', '--complete', help="Mark a task as complete.")
@click.option('-rm', '--delete', help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', default=False, is_flag=True, help="Reset DB.")
@click.command()
def td(*args, **kwargs):
    click.echo('todo')
    Todo(*args, **kwargs)

@click.option('-m', '--message', help="A short message to store, similar to a git commit message.")
@click.option('-cb', '--clipboard', default=False, is_flag=True, help="Paste a large message from the clipboard.")
@click.option('-t', '--tag', help="Add a tag to keep things organized.")
@click.option('-rm', '--delete', help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', default=False, is_flag=True, help="Reset DB.")
@click.command()
def nt(*args, **kwargs):
    click.echo('note')
    Notes(*args, **kwargs)

@click.command()
@click.option('-m', '--message', help="A short message to store, similar to a git commit message.")
@click.option('-d', '--date', help="Describe a date.")
@click.option('-t', '--tag', help="Add a tag to keep things organized.")
@click.option('-rm', '--delete', help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', default=False, is_flag=True, help="Reset DB.")
def rm(*args, **kwargs):
    click.echo('remind me')
    Reminder(*args, **kwargs)


def main():
    cli.add_command(nt)
    cli.add_command(td)
    cli.add_command(rm)
    cli()

if __name__ == '__main__':
    main()
