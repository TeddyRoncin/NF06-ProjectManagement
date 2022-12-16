from TaskStatus import TaskStatus


class Task:

    def __init__(self, id_, name="", description="", estimated_time=0):
        super().__init__()
        self.id = id_
        self.index = 0
        self.name = name
        self.description = description
        self.upstream_tasks = []
        self.downstream_tasks = []
        self.estimated_time = estimated_time
        self.status = TaskStatus.NOT_STARTED
        self.downstream_tasks_count = 0
        self.upstream_tasks_count = 0
        self.earliest_start = 0
        self.latest_start = 0
        self.is_beginning_task = self.id == 0
        self.is_project_task = self.id == 1
        self.is_critical = True
        # This task counts as a depth level, so max_downstream_tasks_depth (resp. upstream_task_count)
        # should always be at least 1
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

    def replace_upstream_task(self, old_task, new_task):
        index = self.upstream_tasks.index(old_task)
        self.upstream_tasks[index] = new_task
        old_task.downstream_tasks.remove(self)
        new_task.downstream_tasks.append(self)
        self.update_upstream_info()
        new_task.update_downstream_info()

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
        return f"<Task name={self.name} index={self.index}>"

    __repr__ = __str__
