import click
from typing import List
from rich.console import Console

from em.app import App
from em.storage import Storage, StorageInterface, ConnectionException
from em.parsers import parse_date

console = Console()

APPNAME = 'reminder'


@click.command()
@click.option('-m', '--message', type=click.STRING, help="A short message to store, similar to a git commit message.")
@click.option('-d', '--date', type=click.STRING, help="Describe a date.")
@click.option('-t', '--tag', type=click.STRING, help="Add a tag to keep things organized.")
@click.option('-rm', '--delete', type=click.INT, help="delete an entity by it's primary key.")
@click.option('-dbr', '--reset', type=click.BOOL, default=False, is_flag=True, help="Reset DB.")
def rm(*args, **kwargs):
    click.echo('remind me')
    Reminder(*args, **kwargs)


def output(content: List):
    from rich.table import Table

    table = Table(title=APPNAME.capitalize())
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Message", justify="left", style="blue")
    table.add_column("Date", justify="left", style="green", no_wrap=True)

    for item in content:
        table.add_row(str(item['id']), str(item['message']), str(item['reminder_timestamp']))

    console.print(table)


class ReminderStorage(Storage, StorageInterface):
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
                                f'message TEXT, '                                 
                                f'reminder_timestamp TEXT, '
                                f'timestamp TEXT'
                                f')')
            self.engine.commit()
        except Exception as e:
            raise ConnectionException(f'error creating table', *e.args)

    def add(self, message: str, date: str):
        try:
            self.engine.execute(f'INSERT INTO {self.table_name} (message, reminder_timestamp, timestamp) VALUES ('
                                f'?, '
                                f'?, '
                                f'CURRENT_TIMESTAMP)', (message, date))
            self.engine.commit()
        except Exception as e:
            print(e)
            raise ConnectionException('error storing item', *e.args)

    def remove(self, pk: str):
        try:
            self.engine.execute(f'DELETE FROM {self.table_name} WHERE id=(?)', (pk,))
            self.engine.commit()
        except Exception as e:
            raise ConnectionException('error deleting item', *e.args)

    def get(self, complete: bool = False):
        data = []
        try:
            for r in self.engine.execute(f'SELECT id, message, reminder_timestamp FROM {self.table_name} ORDER BY reminder_timestamp DESC', ()):
                data.append(dict(r))
            return data
        except Exception as e:
            raise ConnectionException('error retrieving items', *e.args)


class Reminder(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        reset = kwargs.get('reset')
        delete = kwargs.get('delete')
        message = kwargs.get('message')
        date = kwargs.get('date')

        self.storage_cls = ReminderStorage

        if reset:
            self.reset()
        elif message and date:
            self.add(message=message, date=parse_date(date).isoformat())
        elif delete:
            self.remove(pk=delete)
        else:
            self.output()

    def add(self, message: str, date: str):
        with self.storage_cls() as store:
            store.add(message=message, date=date)

    def output(self):
        with self.storage_cls() as store:
            output(store.get())
