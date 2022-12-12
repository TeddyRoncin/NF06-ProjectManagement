import os
import sys

from Task import Task
import json

from TaskStatus import TaskStatus
from utils import c_functions


class Project:
    """
    Represents a project. A project is a list of tasks, which should be completed before it is over.
    This class also contains a method to load all the projects.

    These are the fields of a Project :
    - name : The name of the project
    - file : The name of the file in which the project is stored
    - description : A description of the project
    - tasks_count : The number of tasks of the project
    - project_task : The task representing the end of the project. This task should be present on EVERY projects
    - beginning_task : The task representing the start of the project. This task should be present on EVERY projects
    """

    projects = []
    non_loadable_projects = []

    @staticmethod
    def load_projects():
        """
        Loads the projects. Each project is a JSON file stored in the data/projects directory
        :return: A tuple. The first value is the list of projects,
                 and the second value is the list of non-loadable projects
        """
        projects = []
        non_loadable_projects = []
        for project_file_name in os.listdir("data/projects"):
            try:
                print(f"Loading {project_file_name}")
                with open("data/projects/" + project_file_name, "r") as file:
                    project_data = json.load(file)
                    tasks = [Task(i) for i in range(len(project_data["tasks"]))]
                    for i, task in enumerate(project_data["tasks"]):
                        tasks[i].name = task["name"]
                        tasks[i].description = task["description"]
                        tasks[i].status = TaskStatus(int(task["status"]))
                        # Just sharing this random fact : there are actually many convention
                        # about using snake_case or camelCase in JSON, depending on what languages you use.
                        # You can find a list there :
                        # https://stackoverflow.com/questions/5543490/json-naming-convention-snake-case-camelcase-or-pascalcase#answer-25368854
                        tasks[i].estimated_time = task["estimated_time"]
                        for upstream_task in task["upstream"]:
                            print(f"\tLinking {tasks[i].id} and {upstream_task}")
                            tasks[i].add_upstream_task(tasks[upstream_task])
                    # The first task of the list is the beginning task, and the second one is the project task
                    projects.append(Project(project_data["name"],
                                            project_file_name,
                                            project_data["description"],
                                            len(project_data["tasks"]),
                                            tasks[0],
                                            tasks[1]))
            except Exception as e:
                non_loadable_projects.append(project_file_name)
                print("An exception occurred while loading the project", file=sys.stderr)
                print(e, file=sys.stderr)
        Project.projects = projects
        Project.non_loadable_projects = non_loadable_projects
        return projects, non_loadable_projects

    @staticmethod
    def create_project(name, description, file_name):
        """
        Creates a new project. It also creates the JSON file
        :param name: The name of the project
        :param description: The description of the project
        :param file_name: The name of the file in which the project will be saved
        :return: The newly created project
        """
        project = Project(name, file_name, description)
        Project.projects.append(project)
        project.save()
        return project

    @staticmethod
    def delete_project(project):
        """
        Deletes a project. The deletion is permanent, because the file is also deleted.
        :param project: The project to delete
        :return: None
        """
        Project.projects.remove(project)
        os.remove("data/projects/" + project.file)

    def __init__(self, name, file, description="", tasks_count=2, beginning_task=None, project_task=None):
        """
        Represents a project. A project has a name, a file name, a description.
        A project must have at least 2 tasks :
            * the beginning_task (represents the beginning of the project)
            * the project_task (represents the project ending).
        """
        self.name = name
        self.file = file
        self.description = description
        self.tasks_count = tasks_count
        self.project_task = Task(1, name) if project_task is None else project_task
        self.beginning_task = Task(0, name) if beginning_task is None else beginning_task
        # If we created the tasks, then we need to link them
        if project_task is None or beginning_task is None:
            self.project_task.add_upstream_task(self.beginning_task)

    def save(self):
        """
        Saves the project in a JSON file. The file is saved in data/projects/{self.file}
        :return: None
        """
        project_data = {"name": self.name,
                        "description": self.description,
                        "tasks": [
                            {"name": "", "description": "", "status": 0, "estimated_time": 0, "upstream": []} for _ in range(self.tasks_count)
                        ]}
        self.add_tasks_to_data(project_data, self.project_task)
        with open("data/projects/" + self.file, "w") as file:
            json.dump(project_data, file)

    def add_tasks_to_data(self, project_data, current_task):
        """
        Used by self.save() to add all tasks to the tasks list.
        It adds tasks info on a line to the project_data list.
        This is a recursive algorithm, which propagates upwards
        :param project_data: The dictionary containing info about the project.
        It's what is going to be saved in the JSON file.
        The project_data dictionary will be modified at the end of the function
        :param current_task: The task we should start this algorithm at
        :return: None
        """
        while len(current_task.upstream_tasks) == 1 and project_data["tasks"][current_task.id]["name"] == "":
            next_task = current_task.upstream_tasks[0]
            # Adding the current task to the next task's upstream_tasks list
            project_data["tasks"][current_task.id]["upstream"].append(next_task.id)
            self.load_task_to_data(project_data, current_task)
            current_task = next_task
        if project_data["tasks"][current_task.id]["name"] != "":
            return
        self.load_task_to_data(project_data, current_task)
        for task in current_task.upstream_tasks:
            project_data["tasks"][current_task.id]["upstream"].append(task.id)
            # We skip tasks that have already been managed
            if project_data["tasks"][task.id]["name"] == "":
                self.add_tasks_to_data(project_data, task)

    def load_task_to_data(self, project_data, task):
        """
        Loads a single task to the JSON data (excluding the upstream field)
        :param project_data: The dictionary representing the JSON root object
        :param task: The task to load
        :return: None
        """
        project_data["tasks"][task.id]["name"] = task.name
        project_data["tasks"][task.id]["description"] = task.description
        project_data["tasks"][task.id]["status"] = task.status.value
        project_data["tasks"][task.id]["estimated_time"] = task.estimated_time

    def load(self):
        """
        This function is called when the project is loaded.
        It sets the index value of each task
        :return: None
        """
        c_functions.fix_indices(self)
        c_functions.compute_earliest_start(self)
        c_functions.compute_latest_start(self)
