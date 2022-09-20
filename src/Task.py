import enum

from src.TaskStatus import TaskStatus


class Task:

    def __init__(self, name, description="", upstream_tasks=[], downstream_tasks=[], estimated_time=0):
        self.upstream_tasks = upstream_tasks
        self.downstream_tasks = downstream_tasks
        self.estimated_time = estimated_time
        self.status = TaskStatus.NOT_STARTED
        for task in upstream_tasks:
            if task.status != TaskStatus.FINISHED:
                self.status = TaskStatus.NOT_STARTED

    def update_status(self):
        self.status += 1
