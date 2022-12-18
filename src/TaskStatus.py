from enum import IntEnum, unique


@unique
class TaskStatus(IntEnum):
    LOCKED = 0
    NOT_STARTED = 1
    IN_PROGRESS = 2
    VERIFYING = 3
    FINISHED = 4

    def __str__(self):
        if self == TaskStatus.LOCKED:
            return "Bloquée"
        if self == TaskStatus.NOT_STARTED:
            return "Non commencée"
        if self == TaskStatus.IN_PROGRESS:
            return "En cours"
        if self == TaskStatus.VERIFYING:
            return "En vérification"
        return "Terminée"

    def next_status(self):
        return TaskStatus(self.value + 1)
