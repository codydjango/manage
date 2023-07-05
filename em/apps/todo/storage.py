import json
import click

from typing import Optional

from datetime import datetime
from dateutil.tz import tzlocal

from em.storage import Storage, StorageInterface
from .enums import TaskStatus

class TodoStorage(Storage, StorageInterface):
    def __init__(self):
        super().__init__(table_name='todo')

    def reset(self):
        self.engine.execute(f'DROP TABLE IF EXISTS {self.engine.table_name}')

        self.engine.execute(
            f'CREATE TABLE IF NOT EXISTS {self.engine.table_name} ('
            f'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            f'task TEXT, '
            f'weight INTEGER, '
            f'points INTEGER, '
            f'status TEXT DEFAULT \'{TaskStatus.READY}\','                               
            f'timestamp TEXT, '
            f'logged_time TEXT)')

    def add(self, task: str, weight: int, points: int):
        self.engine.execute(
            f'INSERT INTO {self.engine.table_name} (task, status, weight, points, timestamp) '
            f'VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)', (task, TaskStatus.READY, weight, points,))

    def start_timer(self, pk: int):
        row = self.get_single(pk=pk)
        print(row)
        logged_time = json.loads(row['logged_time'] or '[]')

        if len(logged_time):
            try:
                for t in logged_time:
                    assert t['start']
                    assert t['end']
            except AssertionError:
                click.echo('A timer for this task is already running.')
                return

        logged_time.append({'start': str(datetime.now(tzlocal())), 'end': None})
        row['logged_time'] = json.dumps(logged_time)
        self.put(pk=pk, dct=row)

    def stop_timer(self, pk: int):
        row = self.get_single(pk=pk)
        logged_time = json.loads(row['logged_time'] or '[]')

        if logged_time and not logged_time[-1]['end']:
            logged_time[-1]['end'] = str(datetime.now(tzlocal()))

        row['logged_time'] = json.dumps(logged_time)
        self.put(pk=pk, dct=row)

    def mark_status(self, pk: int, status: TaskStatus):
        self.engine.execute(f'UPDATE {self.engine.table_name} set status = ?'
                            f'WHERE id = ?', (status, pk))

    def remove(self, pk: int):
        self.engine.execute(f'DELETE FROM {self.engine.table_name} WHERE id=(?)', (pk,))

    def get_incomplete(self):
        data = []
        for r in self.engine.execute(
                f'SELECT * '
                f'FROM {self.engine.table_name} '
                f'WHERE not (status = ?) '
                f'ORDER BY weight DESC', (TaskStatus.COMPLETED,)):
            data.append(dict(r))
        return data

    def get_completed(self):
        data = []
        for r in self.engine.execute(
                f'SELECT * '
                f'FROM {self.engine.table_name} '
                f'WHERE status = ? '
                f'ORDER BY weight DESC', (TaskStatus.COMPLETED,)):
            data.append(dict(r))
        return data

    def get(self, pk: Optional[int] = None):
        if pk:
            return self.get_single(pk=pk)
        return self.get_incomplete()

    def get_time_logs_for_item(self, pk: int):
        row = self.get_single(pk=pk)
        return json.loads(row['logged_time'] or '[]')

    def get_points(self):
        row = self.engine.execute(f'SELECT SUM(points) '
                                  f'FROM {self.engine.table_name} '
                                  f'WHERE status = {TaskStatus.COMPLETED}', ()).fetchone()
        return row[0]
