from enum import IntEnum, unique


@unique
class TaskStatus(IntEnum):
    LOCKED = 0
    NOT_STARTED = 1
    IN_PROGRESS = 2
    VERIFYING = 3
    FINISHED = 4


__all__ = [TaskStatus]
