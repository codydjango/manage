from abc import ABC

from rich.console import Console

console = Console()

class App(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def _log(self, message):
        console.log(message)

    def log(self, message):
        self._log(message)