import click
from .app import Notes


@click.option('-m', '--message', type=click.STRING, help="A short message to store, similar to a git commit message.")
@click.option('-cb', '--clipboard', type=click.BOOL, default=False, is_flag=True, help="Paste a large message from the clipboard.")
@click.option('-t', '--tag', type=click.STRING, help="Add a tag to keep things organized.")
@click.option('-rm', '--delete', type=click.INT, help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', type=click.BOOL, default=False, is_flag=True, help="Reset DB.")
@click.option('-dbe', '--export', type=click.BOOL, default=False, is_flag=True, help="Export DB.")
@click.command()
def nt(*args, **kwargs):
    Notes(*args, **kwargs)
