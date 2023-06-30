#!/usr/bin/env python3

import click

from em.apps import nt, td, rm
from em.settings import set_debug


@click.group()
@click.option('-db', '--debug', default=False, is_flag=True, help="Enable debug mode.")
def cli(*args, **kwargs):
    """Entrypoint for the commandline application."""

    set_debug(kwargs.get('debug'))


def main():
    cli.add_command(nt)
    cli.add_command(td)
    cli.add_command(rm)
    cli()

if __name__ == '__main__':
    main()
