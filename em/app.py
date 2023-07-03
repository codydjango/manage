import click

from abc import ABC
from rich.console import Console

from em.settings import DEBUG

console = Console()


class App(ABC):
    storage_cls = None

    def __init__(self, *args, **kwargs):
        if DEBUG:
            self.log(args)
            self.log(kwargs)

    def log(self, message):
        console.log(message)

    def remove(self, pk: str):
        if not click.confirm(f'Are you sure you want to remove this item?'):
            return

        with self.storage_cls() as store:
            store.remove(pk)

    def reset(self):
        if not click.confirm(f'Are you sure you want to reset the {self.__class__} table?'):
            return

        with self.storage_cls() as store:
            self.log(f'resetting the {self.__class__} table...')
            store.reset()
            self.log(f'{self.__class__} table reset.')
