import click
from .app import Todo


@click.option('-m', '--message', type=click.STRING, help="A message describing the task.")
@click.option('-tw', '--weight', default=10, type=click.INT, help="Task weight.")
@click.option('-tp', '--points', default=1, type=click.INT, help="Task points.")
@click.option('-tc', '--complete', type=click.INT, help="Mark a task as complete.")
@click.option('-sc', '--completed', type=click.BOOL, default=False, is_flag=True, help="Show completed tasks.")
@click.option('-rm', '--delete', type=click.INT, help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', default=False, is_flag=True, help="Reset DB.")
@click.option('-dbe', '--export', type=click.BOOL, default=False, is_flag=True, help="Export DB.")
@click.command()
def td(*args, **kwargs):
    Todo(*args, **kwargs)
