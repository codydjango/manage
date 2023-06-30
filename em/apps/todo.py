import click
from typing import List
from rich.console import Console

from em.app import App
from em.storage import Storage, StorageInterface, ConnectionException

console = Console()

APPNAME = 'todo'


@click.option('-m', '--message', type=click.STRING, help="A message describing the task.")
@click.option('-tw', '--weight', default=10, type=click.INT, help="Task weight.")
@click.option('-tp', '--points', default=1, type=click.INT, help="Task points.")
@click.option('-tc', '--complete', type=click.INT, help="Mark a task as complete.")
@click.option('-sc', '--completed', type=click.BOOL, default=False, is_flag=True, help="Show completed tasks.")
@click.option('-rm', '--delete', type=click.INT, help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', default=False, is_flag=True, help="Reset DB.")
@click.command()
def td(*args, **kwargs):
    click.echo('todo')
    Todo(*args, **kwargs)


def output(content: List):
    from rich.table import Table

    table = Table(title=APPNAME.capitalize())
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Weight", justify="left", style="blue", no_wrap=True)
    table.add_column("Points", justify="left", style="blue", no_wrap=True)
    table.add_column("Task", style="magenta")

    for item in content:
        table.add_row(str(item['id']), str(item['weight']), str(item['points']), item['task'])

    console.print(table)


class TodoStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__()
        self.table_name = APPNAME.lower()


    def reset(self):
        try:
            self.engine.execute(f'DROP TABLE IF EXISTS {self.table_name}')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting table', *e.args)

        try:
            self.engine.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} '
                                f'('
                                f'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                f'task TEXT, '
                                f'weight INTEGER, '
                                f'points INTEGER, '
                                f'completed INTEGER DEFAULT 0, '                                   
                                f'timestamp TEXT, '
                                f'timestamp_complete TEXT '
                                f')')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException(f'error creating table', *e.args)

    def add(self, task: str, weight: int, points: int):
        try:
            self.engine.execute(f'INSERT INTO {self.table_name} (task, weight, points, timestamp) VALUES ('
                                f'?, '
                                f'?, '
                                f'?, '
                                f'CURRENT_TIMESTAMP)', (task, weight, points))
            self.engine.commit()
        except Exception as e:
            print(e)
            raise ConnectionException('error storing item', *e.args)

    def complete(self, pk: str):
        try:
            self.engine.execute(f'UPDATE {self.table_name} set completed = 1, timestamp_complete = CURRENT_TIMESTAMP WHERE id = ?', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error completing item', *e.args)

    def remove(self, pk: str):
        try:
            self.engine.execute(f'DELETE FROM {self.table_name} WHERE id=(?)', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting item', *e.args)

    def get(self, complete: bool = False):
        data = []
        try:
            for r in self.engine.execute(f'SELECT id, weight, points, task, timestamp, timestamp_complete FROM {self.table_name} WHERE completed = ? ORDER BY weight DESC', (1 if complete else 0,)):
                data.append(dict(r))
            return data
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)

class Todo(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        reset = kwargs.get('reset')
        delete = kwargs.get('delete')
        complete = kwargs.get('complete')
        completed = kwargs.get('completed')
        weight = kwargs.get('weight', 10)
        points = kwargs.get('points', 1)
        message = kwargs.get('message')

        self.storage_cls = TodoStorage

        if reset:
            self.reset()
        elif message:
            self.add(note=message, weight=weight, points=points)
        elif delete:
            self.remove(pk=delete)
        elif complete:
            self.complete(pk=complete)
        else:
            self.output(completed=completed)

    def add(self, note: str, weight: int = 0, points: int = 0):
        with self.storage_cls() as store:
            store.add(note, weight, points)

    def complete(self, pk: str):
        with self.storage_cls() as store:
            store.complete(pk)

    def output(self, completed: bool):
        with self.storage_cls() as store:
            output(store.get(completed))
