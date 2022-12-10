import enum

from TaskStatus import TaskStatus


class Task:

    next_id = 0

    def __init__(self, id_=None, name="", description="", estimated_time=0):
        if id_ is None:
            id_ = Task.next_id
        Task.next_id = max(Task.next_id, id_ + 1)
        self.id = id_
        self.name = name
        self.description = description
        self.upstream_tasks = []
        self.downstream_tasks = []
        self.estimated_time = estimated_time
        self.status = TaskStatus.NOT_STARTED
        self.downstream_tasks_count = 0
        self.upstream_tasks_count = 0
        # This task counts as a depth level, so max_downstream_tasks_depth (resp. upstream_task_count) should always be at least 1
        self.max_downstream_tasks_depth = 1
        self.max_upstream_tasks_depth = 1
        self.update_upstream_info()
        self.update_downstream_info()

    def update_status(self):
        self.status += 1

    def add_upstream_task(self, task):
        self.upstream_tasks.append(task)
        task.downstream_tasks.append(self)
        self.update_upstream_info()
        task.update_downstream_info()

    def remove_upstream_task(self, task):
        self.upstream_tasks.remove(task)
        task.downstream_tasks.remove(self)
        self.update_upstream_info()
        task.update_downstream_info()

    def replace_upstream_task(self, oldTask, newTask):
        index = self.upstream_tasks.index(oldTask)
        self.upstream_tasks[index] = newTask
        oldTask.downstream_tasks.remove(self)
        newTask.downstream_tasks.append(self)
        self.update_upstream_info()
        newTask.update_downstream_info()
        #oldTask.update_downstream_info()

    def update_upstream_info(self):
        self.upstream_tasks_count = 0
        self.max_upstream_tasks_depth = 0
        if len(self.upstream_tasks) == 0:
            self.max_upstream_tasks_depth = 1
        for upstream_task in self.upstream_tasks:
            if upstream_task.upstream_tasks_count >= self.upstream_tasks_count:
                self.upstream_tasks_count = upstream_task.upstream_tasks_count + 1
            self.max_upstream_tasks_depth += upstream_task.max_upstream_tasks_depth
        # Propagate changes to downstream tasks
        for downstream_task in self.downstream_tasks:
            downstream_task.update_upstream_info()

    def update_downstream_info(self):
        self.downstream_tasks_count = 0
        self.max_downstream_tasks_depth = 0
        if len(self.downstream_tasks) == 0:
            self.max_downstream_tasks_depth = 1
        for downstream_task in self.downstream_tasks:
            if downstream_task.downstream_tasks_count >= self.downstream_tasks_count:
                self.downstream_tasks_count = downstream_task.downstream_tasks_count + 1
            self.max_downstream_tasks_depth += downstream_task.max_downstream_tasks_depth
        # Propagate changes to upstream tasks
        for upstream_task in self.upstream_tasks:
            upstream_task.update_downstream_info()

    def __str__(self):
        return f"<Task name={self.name}>"

    def __repr__(self):
        return str(self)
