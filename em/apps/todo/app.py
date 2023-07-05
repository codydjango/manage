import json

from datetime import datetime
from dateutil import parser
from dateutil.tz import tzlocal
from typing import List, Optional

from rich.console import Console
from rich.table import Table

from .storage import TodoStorage
from .enums import TaskStatus

from em.app import App

console = Console()

APPNAME = 'todo'
def output(content: List, points: int):
    table = Table(title=f'{APPNAME.capitalize()} ({points})')
    table.add_column("ID", justify="left", style="cyan", no_wrap=True)
    table.add_column("Weight", justify="left", style="blue", no_wrap=True)
    table.add_column("Points", justify="left", style="blue", no_wrap=True)
    table.add_column("Status", justify="left", style="blue", no_wrap=True)
    table.add_column("Logged Time", justify="left", style="blue", no_wrap=True)
    table.add_column("Task", style="magenta")

    for item in content:
        status_name = TaskStatus(item['status']).name
        total_logged_time = calculate_total_logged_time(item['logged_time'])
        row = map(str, [item['id'], item['weight'], item['points'], status_name, total_logged_time, item['task']])
        table.add_row(*row)

    console.print(table)


def output_time_logs(pk: int, content: List):
    table = Table(title=f'Logged time for item: {pk}')

    table.add_column("Start", justify="left", style="cyan", no_wrap=True)
    table.add_column("End", justify="left", style="blue", no_wrap=True)

    for item in content:
        row = map(str, [item['start'], item['end']])
        table.add_row(*row)

    console.print(table)


def calculate_total_logged_time(logged_time: Optional[str] = None):
    if not logged_time:
        return '0h 0m 0s'

    logged_time = json.loads(logged_time or '[]')
    total_logged_time = 0

    for time_period in logged_time:
        start_time = parser.parse(time_period['start'])

        if not time_period['end']:
            end_time = parser.parse(str(datetime.now(tzlocal())))
        else:
            end_time = parser.parse(time_period['end'])

        total_logged_time += (end_time - start_time).total_seconds()

    hours, remainder = divmod(total_logged_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{int(hours)}h {int(minutes)}m {int(seconds)}s'


class Todo(App):
    storage_cls = TodoStorage

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        reset = kwargs.get('reset')
        remove = kwargs.get('remove')
        start_timer = kwargs.get('start_timer')
        pause_timer = kwargs.get('pause_timer')
        complete = kwargs.get('complete')
        show_completed = kwargs.get('show_completed')
        show_time_logs = kwargs.get('show_time_logs', None)
        weight = kwargs.get('weight', 10)
        points = kwargs.get('points', 1)
        message = kwargs.get('message')
        export = kwargs.get('export')

        if reset:
            self.reset()
        elif message:
            self.add(note=message, weight=weight, points=points)
        elif start_timer:
            self.start(pk=start_timer)
        elif pause_timer:
            self.pause(pk=pause_timer)
        elif complete:
            self.end(pk=complete)
        elif remove:
            self.remove(pk=remove)
        elif export:
            self.export()
        elif show_time_logs:
            self.output_time_logs(pk=show_time_logs)
        else:
            self.output(completed=show_completed)

    def add(self, note: str, weight: int = 0, points: int = 0):
        with self.storage_cls() as store:
            store.add(note, weight, points)
            store.commit()

    def start(self, pk: int):
        with self.storage_cls() as store:
            store.start_timer(pk=pk)
            store.mark_status(pk=pk, status=TaskStatus.IN_PROGRESS)
            store.commit()

    def pause(self, pk: int):
        with self.storage_cls() as store:
            store.stop_timer(pk=pk)
            store.mark_status(pk=pk, status=TaskStatus.PAUSED)
            store.commit()

    def end(self, pk: int):
        with self.storage_cls() as store:
            store.stop_timer(pk=pk)
            store.mark_status(pk=pk, status=TaskStatus.COMPLETED)
            store.commit()

    def output(self, pk: int = None, completed: bool = False):
        with self.storage_cls() as store:
            if pk:
                content = [store.get_single(pk=pk)]
            elif completed:
                content = store.get_completed()
            else:
                content = store.get_incomplete()
            points = store.get_points()

        output(content=content, points=points)

    def output_time_logs(self, pk: int):
        with self.storage_cls() as store:
            content = store.get_time_logs_for_item(pk=pk)

        output_time_logs(pk=pk, content=content)
