#!/usr/bin/env python3

import click

from em.apps import td, rm, nt, qz, all_apps
from em.settings import set_debug


@click.group()
@click.option('-db', '--debug', default=False, is_flag=True, help="Enable debug mode.")
def cli(*args, **kwargs):
    """EM: Flywheel for engineering management."""

    set_debug(kwargs.get('debug'))

@click.command()
@click.option('-x', '--export', default=False, is_flag=True, help="Export all.")
def all(*args, **kwargs):
    if kwargs.get('export'):
        for app in all_apps:
            try:
                app(export=True)
            except:
                pass

def main():
    cli.add_command(nt)
    cli.add_command(td)
    cli.add_command(rm)
    cli.add_command(qz)
    cli.add_command(all)
    cli()

if __name__ == '__main__':
    main()
