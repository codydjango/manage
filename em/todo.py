import click
from typing import List
from rich.console import Console

from em.app import App
from em.storage import TodoStorage

console = Console()

def output(content: List):
    from rich.table import Table

    table = Table(title="Todo")
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Weight", justify="left", style="blue", no_wrap=True)
    table.add_column("Points", justify="left", style="blue", no_wrap=True)
    table.add_column("Task", style="magenta")

    for item in content:
        table.add_row(str(item[0]), str(item[1]), str(item[2]), item[3])

    console.print(table)


class Todo(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get('debug'):
            self._log(args)
            self._log(kwargs)

        reset = kwargs.get('reset')
        delete = kwargs.get('delete')
        complete = kwargs.get('complete')
        weight = kwargs.get('weight')
        points = kwargs.get('points')
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
            self.output()

    def reset(self):
        if not click.confirm(f'Are you sure you want to reset the {self.__class__} table?'):
            return

        with self.storage_cls() as store:
            self.log(f'resetting the {self.__class__} table...')
            store.reset()
            self.log(f'{self.__class__} table reset.')

    def add(self, note: str, weight: int = 0, points: int = 0):
        with self.storage_cls() as store:
            store.add(note, weight, points)

    def complete(self, pk: str):
        with self.storage_cls() as store:
            store.complete(pk)

    def remove(self, pk: str):
        if not click.confirm(f'Are you sure you want to delete the item?'):
            return

        with self.storage_cls() as store:
            store.remove(pk)

    def output(self):
        with self.storage_cls() as store:
            output(store.get())
