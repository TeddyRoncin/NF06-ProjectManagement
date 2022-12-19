from enum import IntEnum, unique


@unique
class TaskStatus(IntEnum):

    """
    Represents the status of a Task. These are the possible values :
    - LOCKED : The task is locked, upstream tasks need to be completed first.
    - NOT_STARTED : The task is not started yet, but can be started.
    - IN_PROGRESS : The task has been started, but is not finished yet.
    - VERIFYING : The task is finished, and is being verified.
    - DONE : The task is finished and verified. Downstream tasks can be started.
    """

    LOCKED = 0
    NOT_STARTED = 1
    IN_PROGRESS = 2
    VERIFYING = 3
    FINISHED = 4

    def __str__(self):
        """
        Returns the string representation of the TaskStatus.
        :return: The string representation of the TaskStatus.
        """
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
        """
        Returns the next status of the TaskStatus.
        :return: A TaskStatus representing the next status.
        """
        return TaskStatus(self.value + 1)
