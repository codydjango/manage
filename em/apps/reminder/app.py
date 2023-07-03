from typing import List

from rich.console import Console
from rich.table import Table

from em.app import App
from em.parsers import parse_date
from .storage import ReminderStorage

APPNAME = 'reminder'
console = Console()


def output(content: List):
    table = Table(title=APPNAME.capitalize())
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Message", justify="left", style="blue")
    table.add_column("Date", justify="left", style="green", no_wrap=True)

    for item in content:
        table.add_row(str(item['id']), str(item['message']), str(item['reminder_timestamp']))

    console.print(table)


class Reminder(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        reset = kwargs.get('reset')
        delete = kwargs.get('delete')
        message = kwargs.get('message')
        date = kwargs.get('date')
        export = kwargs.get('export')

        self.storage_cls = ReminderStorage

        if reset:
            self.reset()
        elif message and date:
            self.add(message=message, date=parse_date(date).isoformat())
        elif delete:
            self.remove(pk=delete)
        elif export:
            self.export()
        else:
            self.output()

    def add(self, message: str, date: str):
        with self.storage_cls() as store:
            store.add(message=message, date=date)

    def output(self):
        with self.storage_cls() as store:
            output(store.get())
