import click
from .app import Quiz

@click.command()
def qz(*args, **kwargs):
    Quiz(*args, **kwargs)
