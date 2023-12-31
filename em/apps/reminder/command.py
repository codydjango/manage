import click
from em.exceptions import NotFoundException
from .app import Reminder


@click.command()
@click.option('-m', '--message', type=click.STRING, help="A short message to store, similar to a git commit message.")
@click.option('-d', '--date', type=click.STRING, help="Describe a date.")
@click.option('-t', '--tag', type=click.STRING, help="Add a tag to keep things organized.")
@click.option('-rm', '--delete', type=click.INT, help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', type=click.BOOL, default=False, is_flag=True, help="Reset DB.")
@click.option('-dbe', '--export', type=click.BOOL, default=False, is_flag=True, help="Export DB.")
def rm(*args, **kwargs):
    try:
        Reminder(*args, **kwargs)
    except NotFoundException as e:
        click.echo(str(e))
