import click
from em.exceptions import NotFoundException
from .app import Todo

@click.option('-m', '--message', type=click.STRING, help='A message describing the Task.')
@click.option('-w', '--weight', default=10, type=click.INT, help='Assign a Task weight.')
@click.option('-p', '--points', default=1, type=click.INT, help='Assign Task points.')
@click.option('-st', '--start-timer', type=click.INT, help='Mark a Task as started.')
@click.option('-pt', '--pause-timer', type=click.INT, help='Mark a Task as paused.')
@click.option('-c', '--complete', type=click.INT, help='Mark a Task as completed.')
@click.option('-stl', '--show-time-logs', type=click.INT, help='Show logged time for Task.')
@click.option('-sc', '--show-completed', type=click.BOOL, default=False, is_flag=True, help='Show completed tasks.')
@click.option('-rm', '--remove', type=click.INT, help='Remove a Task.')
@click.option('-dbr', '--reset', default=False, is_flag=True, help='Reset DB.')
@click.option('-dbe', '--export', type=click.BOOL, default=False, is_flag=True, help='Export DB.')
@click.command()
def td(*args, **kwargs):
    try:
        Todo(*args, **kwargs)
    except NotFoundException as e:
        click.echo(str(e))
