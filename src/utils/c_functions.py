import os
import sys
from ctypes import CDLL, POINTER, c_int, Structure, c_char_p, cast, pointer, byref

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
        :param first_task: The first task of the project
        :param task_count: The number of tasks in the project
        :return: None
        """
        # Initialize the list of Task_Struct
        Task_Struct._tasks = [None] * task_count
        # Create the first task (which will create all the others in a recursive way)
        Task_Struct(first_task)
        # Load data into the Task_Struct
        for i, task in enumerate(Task_Struct._tasks):
            # There should not be any, but we still check, just in case
            # If this occurs, code may not continue working properly
            if task is None:
                print(f"Task with id {i} doesn't seem to exist. "
                      f"This error occured while converting tasks to task structures", file=sys.stderr)
                continue
            task.load()

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
        self.earlier = 0
        self.later = 0
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
        self.ancestors = cast(upstream_tasks_array_type(*upstream_tasks_pointers), POINTER(POINTER(Task_Struct)))
        self.id = c_int(self._task.id)
        self.successors_count = len(self._task.downstream_tasks)
        self.ancestors_count = len(self._task.upstream_tasks)
        self.index = c_int(self._task.index)
        self.duration = self._task.estimated_time
        self.earlier = self._task.earliest_start
        self.later = self._task.latest_start

    @staticmethod
    def save_indices():
        """
        Save the index of every Task_Struct into its corresponding Task.
        This method does not save other data.
        :return: None
        """
        for task_struct in Task_Struct._tasks:
            task_struct._task.index = task_struct.index

    @staticmethod
    def save_earliest_start():
        """
        Saves the earlist_start and earliest_end of every Task_Struct into its corresponding Task.
        This method does not save other data.
        :return: None
        """
        for task_struct in Task_Struct._tasks:
            task_struct._task.earliest_start = task_struct.earlier

    @staticmethod
    def save_latest_start():
        """
        Saves the earlist_start and earliest_end of every Task_Struct into its corresponding Task.
        This method does not save other data.
        :return: None
        """
        for task_struct in Task_Struct._tasks:
            task_struct._task.latest_start = task_struct.later

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
    ('earlier', c_int),
    ('later', c_int),
    ('marge', c_int),
]

# Functions of the dll
_fill_indices = dll.fill_indice
_fill_indices.argtypes = [POINTER(Task_Struct), POINTER(Task_Struct), POINTER(c_int), POINTER(c_int)]
_fill_indices.restype = None

_task_earlier = dll.task_earlier
_task_earlier.argtypes = [POINTER(Task_Struct)]

_task_later = dll.task_later
_task_later.argtypes = [POINTER(Task_Struct)]


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
    print(Task_Struct._tasks)
    _fill_indices(byref(first_task), byref(last_task), byref(first_index), byref(last_index))
    Task_Struct.save_indices()


def compute_earliest_start(project):
    """
    Compute the earliest_start of each task of the project
    :param project: The project
    :return: None
    """
    Task_Struct.convert_tasks(project.beginning_task, project.tasks_count)
    first_task = Task_Struct.get_converted_task(project.beginning_task)
    _task_earlier(byref(first_task))
    Task_Struct.save_earliest_start()


def compute_latest_start(project):
    """
    Compute the earliest_start of each task of the project
    :param project: The project
    :return: None
    """
    Task_Struct.convert_tasks(project.beginning_task, project.tasks_count)
    last_task = Task_Struct.get_converted_task(project.project_task)
    _task_later(byref(last_task))
    Task_Struct.save_latest_start()
