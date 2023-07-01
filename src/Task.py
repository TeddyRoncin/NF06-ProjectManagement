from TaskStatus import TaskStatus


class Task:

    """
    Represents a task in a project. A Task is a unit of work that can be done by a small amount of people.
    It is the building block of a Project. A Task can have upstream (resp. downstream) Tasks,
    which are tasks that should be completed before (resp. after) the Task.
    This tree-like structure is what creates a Project.

    These are the fields of a Task :
    - id : The id of the Task. It is unique in the Project. It is used to identify the Task.
    - name : The name of the Task.
    - description : The description of the Task.
    - upstream_tasks : A list of Tasks that should be completed before this Task can start.
    - downstream_tasks : A list of Tasks that can start only once this Task is completed.
    - estimated_time : The estimated time that will be necessary to complete the Task.
    - status : The TaskStatus of the Task, this is used to know what has been done on the Task.
    - downstream_tasks_count : The length of the longest path we can take from this Task to the last one
                               (by only going downstream).
    - upstream_tasks_count : The length of the longest path we can take from this Task to the first one
                             (by only going upstream).
    - earliest_start : The earliest estimated number of days at which the Task can start.
    - latest_start : The latest estimated number of days at which the Task can start.
    - is_beginning_task : Whether the Task is the beginning Task (meaning the first Task) of the Project.
    - is_project_task : Whether the Task is the project Task (meaning the last Task) of the Project.
    - is_critical : Whether the Task is critical or not. A Task is critical if there is no margin for its starting date.
    - max_downstream_tasks_depth : The maximum depth a downstream Task can have relative to this Task.
                                   (here, downstream is in the larger sense of the definition).
                                   It needs to be at least 1.
    - max_upstream_tasks_depth : The maximum depth an upstream Task can have relative to this Task.
                                 (here, upstream is in the larger sense of the definition).
                                 It needs to be at least 1.
    """

    def __init__(self, id_, name="", description="", estimated_time=0):
        """
        Creates a new Task
        :param id_: The id of the Task
        :param name: The name of the Task. By default, it is an empty string
        :param description: The description of the Task. By default, it is an empty string
        :param estimated_time: The estimated number of days that will be necessary to complete the Task.
                               By default, it is 0.
        """
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
        self.is_critical = False
        # This task counts as a depth level, so max_downstream_tasks_depth (resp. upstream_task_count)
        # should always be at least 1
        self.max_downstream_tasks_depth = 1
        self.max_upstream_tasks_depth = 1
        self.update_upstream_info()
        self.update_downstream_info()

    def update_status(self):
        """
        Updates changes the status of the Task to the next status
        :return: None
        """
        self.status = self.status.next_status()

    def add_upstream_task(self, task, index=None):
        """
        Adds an upstream Task to the Task. The Task will be inserted at the given index.
        If no index is given, it will be inserted at the end of the list.
        It also adds this Task to the downstream_tasks of the given Task
        :param task: The Task to add
        :param index: The index at which to insert the Task. This is optional
        :return: None
        """
        if index is None:
            self.upstream_tasks.append(task)
        else:
            self.upstream_tasks.insert(index, task)
        task.downstream_tasks.append(self)
        self.update_upstream_info()
        task.update_downstream_info()

    def remove_upstream_task(self, task):
        """
        Removes an upstream Task. It also removes this Task from the downstream_tasks of the given Task.
        :param task:
        :return:
        """
        self.upstream_tasks.remove(task)
        task.downstream_tasks.remove(self)
        self.update_upstream_info()
        task.update_downstream_info()

    def replace_upstream_task(self, old_task, new_task):
        """
        Replaces an upstream Task by another one. It also modifies the downstream_tasks of the old and new Tasks
        :param old_task: The Task to replace
        :param new_task: The Task that will replace the old one
        :return: None
        """
        index = self.upstream_tasks.index(old_task)
        self.upstream_tasks[index] = new_task
        old_task.downstream_tasks.remove(self)
        new_task.downstream_tasks.append(self)
        self.update_upstream_info()
        new_task.update_downstream_info()

    def update_upstream_info(self):
        """
        Updates the upstream_tasks_count and max_upstream_tasks_depth of the Task.
        This calls the same method recursively on all the downstream Tasks.
        :return: None
        """
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
        """
        Updates the downstream_tasks_count and max_downstream_tasks_depth of the Task.
        This calls the same method recursively on all the upstream Tasks.
        :return:
        """
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
