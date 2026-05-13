import click
from .app import Quiz

@click.command()
@click.option('-t', '--tags', type=click.STRING, help='filter by tags (space-separated)')
@click.option('-l', '--limit', type=click.INT, help='max questions per session')
@click.option('--list', 'list_mode', is_flag=True, help='list questions and their spaced repetition state')
def qz(*args, **kwargs):
    Quiz(*args, **kwargs)
