import ctypes
import os

from Task import Task
import json


class Project:

    """
    Loads the projects. Each project is a JSON file stored in the data/projects directory
    :return: A tuple. The first value is the list of projects, and the second value is the list of non-loadable projects
    """
    @classmethod
    def load_projects(cls):
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
                        for upstream_task in task["upstream"]:
                            print(f"Linking {tasks[i].id} and {upstream_task}")
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
                print("An exception occured while loading the project")
                print(e)
        return projects, non_loadable_projects

    """
    Represents a project. A project has a name, a file name, a description. The goal of the project is a task : complete the project.
    """
    def __init__(self, name, file, description="", tasks_count=2, beginning_task=None, project_task=None):
        self.name = name
        self.file = file
        self.description = description
        self.tasks_count = tasks_count
        self.project_task = Task(1, name) if project_task is None else project_task
        self.beginning_task = Task(0, name) if beginning_task is None else beginning_task

    def save(self):
        """
        Saves the project in a JSON file. The file is saved in data/projects/{self.file}
        :return: None
        """
        project_data = {"name": self.name,
                        "description": self.description,
                        "tasks": [{"name": "", "description": "", "upstream": []} for i in range(self.tasks_count)]}
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
            project_data["tasks"][current_task.id]["name"] = current_task.name
            project_data["tasks"][current_task.id]["description"] = current_task.description
            current_task = next_task
        if project_data["tasks"][current_task.id]["name"] != "":
            return
        project_data["tasks"][current_task.id]["name"] = current_task.name
        project_data["tasks"][current_task.id]["description"] = current_task.description
        for task in current_task.upstream_tasks:
            project_data["tasks"][current_task.id]["upstream"].append(task.id)
            # We skip tasks that have already been managed
            if project_data["tasks"][task.id]["name"] == "":
                self.add_tasks_to_data(project_data, task)
