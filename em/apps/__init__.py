from .notes.command import nt
from .notes.app import Notes
from .todo.command import td
from .todo.app import Todo
from .reminder.command import rm
from .reminder.app import Reminder
from .quiz.command import qz
from .quiz.app import Quiz

all_apps = [Notes, Todo, Reminder, Quiz]

__all__ = ['nt', 'td', 'rm', 'qz', 'all_apps']