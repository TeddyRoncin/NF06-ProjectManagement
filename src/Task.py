import enum

from TaskStatus import TaskStatus


class Task:

    def __init__(self, name="", description="", upstream_tasks=None, downstream_tasks=None, estimated_time=0):
        if downstream_tasks is None:
            downstream_tasks = []
        if upstream_tasks is None:
            upstream_tasks = []
        self.name = name
        self.description = description
        self.upstream_tasks = upstream_tasks
        self.downstream_tasks = downstream_tasks
        self.estimated_time = estimated_time
        self.status = TaskStatus.NOT_STARTED
        for task in upstream_tasks:
            if task.status != TaskStatus.FINISHED:
                self.status = TaskStatus.LOCKED
        # We have to give max at least 2 arguments, so we give it -1 twice, in case there are no downstream_tasks
        self.downstream_tasks_count = max(-1, -1, *(task.downstream_tasks_count for task in self.downstream_tasks)) + 1
        # This task counts as a depth level, so max_downstream_tasks_depth should be at least 1
        self.max_downstream_tasks_depth = max(1, sum((task.max_downstream_tasks_depth for task in self.downstream_tasks)))

        self.upstream_tasks_count = max(-1, -1, *(task.upstream_tasks_count for task in self.upstream_tasks)) + 1
        self.max_upstream_tasks_depth = max(1, sum((task.max_upstream_tasks_depth for task in self.upstream_tasks)))

    def update_status(self):
        self.status += 1

    def add_upstream_task(self, task):
        self.upstream_tasks.append(task)
        task.downstream_tasks.append(self)
        if task.upstream_tasks_count >= self.upstream_tasks_count:
            self.upstream_tasks_count = task.upstream_tasks_count + 1
        if len(self.upstream_tasks) == 1:
            self.max_upstream_tasks_depth = task.max_upstream_tasks_depth
        else:
            self.max_upstream_tasks_depth += task.max_upstream_tasks_depth
        if self.downstream_tasks_count >= task.downstream_tasks_count:
            task.downstream_tasks_count = self.downstream_tasks_count + 1
        if len(task.downstream_tasks) == 1:
            task.max_downstream_tasks_depth = self.max_downstream_tasks_depth
        else:
            task.max_downstream_tasks_depth += self.max_downstream_tasks_depth

    def __str__(self):
        return f"<Task name={self.name}>"

    def __repr__(self):
        return str(self)
