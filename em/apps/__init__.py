from .notes.command import nt
from .notes.app import Notes
from .todo.command import td
from .todo.app import Todo
from .reminder.command import rm
from .reminder.app import Reminder

all_apps = [Notes, Todo, Reminder]

__all__ = ['nt', 'td', 'rm', 'all_apps']