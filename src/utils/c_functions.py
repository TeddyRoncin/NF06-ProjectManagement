import os
import sys
from ctypes import CDLL, POINTER, c_int, Structure, c_char_p, cast, pointer, byref
from enum import Enum

if os.name == "windows":
    dll = CDLL("Core.dll")
else:
    dll = CDLL(f"{os.path.abspath(os.curdir)}/Core.so")


class Task_Struct(Structure):

    _tasks = []

    @staticmethod
    def convert_tasks(first_task, task_count):
        """
        Convert a list of tasks into a list of Task_Struct
        :param first_task:
        :return:
        """
        # Initialize the list of Task_Struct
        Task_Struct._tasks = [None] * task_count
        # Create the first task (which will create all the others in a recursive way)
        Task_Struct(first_task)
        # Load data into the Task_Struct
        print(Task_Struct._tasks)
        for i, task in enumerate(Task_Struct._tasks):
            # There should not be any, but we still check, just in case
            # If this occurs, code may not continue working properly
            if task is None:
                print(f"Task with id {id} doesn't seem to exist. This error occured while converting tasks to task structures", file=sys.stderr)
                continue
            task.load()
        # Return the first task
        return Task_Struct._tasks[0]

    @staticmethod
    def get_converted_task(task):
        return Task_Struct._tasks[task.id]

    def __init__(self, task):
        """
        Initialize a Task_Struct. This will also initialize non-initialized downstream structures.
        Values will not be initialized until the load() method is called.
        :param task: The task this structure represents
        """
        super().__init__()
        Task_Struct._tasks[task.id] = self
        self._task = task
        self._downstream_tasks_id = [task.id for task in self._task.downstream_tasks]
        # Create downstream Task_Struct if they are not already created
        for task in self._task.downstream_tasks:
            if Task_Struct._tasks[task.id] is None:
                Task_Struct(task)
        self._upstream_tasks_id = [task.id for task in self._task.upstream_tasks]
        self.name = b""
        self.successors = POINTER(POINTER(Task_Struct))()
        self.ancestors = POINTER(POINTER(Task_Struct))()
        self.id = 0
        self.successors_count = 0
        self.ancestors_count = 0
        self.index = 0
        self.duration = 0
        self.earliest_start = 0
        self.latest_start = 0
        self.duration = 0

    def load(self):
        """
        Load data from the Task into the Task_Struct
        :return: None
        """
        self.name = self._task.name.encode("utf-8")
        downstream_tasks_array_type = POINTER(Task_Struct) * len(self._downstream_tasks_id)
        downstream_tasks_pointers = [pointer(Task_Struct._tasks[i]) for i in self._downstream_tasks_id]
        self.successors = cast(downstream_tasks_array_type(*downstream_tasks_pointers), POINTER(POINTER(Task_Struct)))
        upstream_tasks_array_type = POINTER(Task_Struct) * len(self._upstream_tasks_id)
        upstream_tasks_pointers = [pointer(Task_Struct._tasks[i]) for i in self._upstream_tasks_id]
        self. ancestors= cast(upstream_tasks_array_type(*upstream_tasks_pointers), POINTER(POINTER(Task_Struct)))
        self.id = c_int(self._task.id)
        self.successors_count = len(self._task.downstream_tasks)
        self.ancestors_count = len(self._task.upstream_tasks)
        self.index = c_int(self._task.index)
        self.duration = self._task.estimated_time
        self.earliest_start = self._task.earliest_start
        self.latest_start = self._task.latest_start
        self.duration = self._task.latest_start - self._task.earliest_start

    def save_indices(self):
        """
        Save the indices of the Task_Struct into the Task.
        This method does not save other data
        This is done for every tasks that are afterwards this one. If there is an intersection, it is called recursively
        :return: None
        """
        self._task.index = self.index
        task_struct = self
        while len(task_struct._downstream_tasks_id) == 1:
            task_struct = Task_Struct._tasks[task_struct._downstream_tasks_id[0]]
            task_struct._task.index = task_struct.index
        if len(task_struct._downstream_tasks_id) > 1:
            for i in task_struct._downstream_tasks_id:
                Task_Struct._tasks[i].save_indices()

    def __str__(self):
        return f"Task_Struct({self._task})"

    __repr__ = __str__


# Fields of the struct
Task_Struct._fields_ = [
    ('name', c_char_p),
    ('successors', POINTER(POINTER(Task_Struct))),
    ('ancestors', POINTER(POINTER(Task_Struct))),
    ('id', c_int),
    ('successors_count', c_int),
    ('ancestors_count', c_int),
    ('index', c_int),
    ('duration', c_int),
    ('earliest_start', c_int),
    ('latest_start', c_int),
    ('marge', c_int),
]

# Functions of the dll
_fill_indices = dll.fill_indice
_fill_indices.argtypes = [POINTER(Task_Struct), POINTER(Task_Struct), POINTER(c_int), POINTER(c_int)]
_fill_indices.restype = None


def fix_indices(project):
    """
    Fixes indices of the tasks in the project
    :param project: The project
    :return: None
    """
    first_index = c_int(1)
    last_index = c_int(project.tasks_count)
    Task_Struct.convert_tasks(project.beginning_task, project.tasks_count)
    first_task = Task_Struct.get_converted_task(project.beginning_task)
    last_task = Task_Struct.get_converted_task(project.project_task)
    _fill_indices(byref(first_task), byref(last_task), byref(first_index), byref(last_index))
    first_task.save_indices()

