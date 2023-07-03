from typing import List

from rich.console import Console
from rich.table import Table
from .storage import TodoStorage

from em.app import App

console = Console()

APPNAME = 'todo'
def output(content: List, points: int):
    table = Table(title=f'{APPNAME.capitalize()} ({points})')
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Weight", justify="left", style="blue", no_wrap=True)
    table.add_column("Points", justify="left", style="blue", no_wrap=True)
    table.add_column("Task", style="magenta")

    for item in content:
        table.add_row(str(item['id']), str(item['weight']), str(item['points']), item['task'])

    console.print(table)


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
        export = kwargs.get('export')

        self.storage_cls = TodoStorage

        if reset:
            self.reset()
        elif message:
            self.add(note=message, weight=weight, points=points)
        elif delete:
            self.remove(pk=delete)
        elif complete:
            self.complete(pk=complete)
        elif export:
            self.export()
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
            output(content=store.get(completed), points=store.get_points())
