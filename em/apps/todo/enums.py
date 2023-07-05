from enum import StrEnum

class TaskStatus(StrEnum):
    READY = 'ready'
    IN_PROGRESS = 'in-progress'
    PAUSED = 'paused'
    COMPLETED = 'completed'