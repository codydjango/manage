import click
from .app import Quiz

@click.command()
@click.option('-t', '--tags', type=click.STRING, help='filter for tag')
@click.option('-l', '--limit', type=click.INT, help='limit to')
def qz(*args, **kwargs):
    Quiz(*args, **kwargs)
