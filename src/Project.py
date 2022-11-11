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
                with open("data/projects/" + project_file_name, "r") as file:
                    project_data = json.load(file)
                    print(project_data)
                    tasks = [Task() for _ in range(len(project_data["tasks"]))]
                    print(len(tasks))
                    for i, task in enumerate(project_data["tasks"]):
                        tasks[i].name = task["name"]
                        tasks[i].description = task["description"]
                        for upstream_task in task["upstream"]:
                            print(f"adding link between {tasks[i]} and {upstream_task}")
                            tasks[i].add_upstream_task(tasks[upstream_task])
                            print("done !")
                    # The first task of the list is the beginning task, and the second one is the project task
                    projects.append(Project(project_data["name"], project_data["description"], tasks[0], tasks[1]))
            #except Exception as e:
            except IOError as e:
                non_loadable_projects.append(project_file_name)
                print("An exception occured while loading the project")
                print(e)
        return projects, non_loadable_projects

    """
    Represents a project. A project has a name, a description. The goal of the project is a task : complete the project.
    """
    def __init__(self, name, description="", beginning_task=None, project_task=None):
        self.name = name
        self.description = description
        self.project_task = Task(name) if project_task is None else project_task
        self.beginning_task = Task(name) if beginning_task is None else beginning_task
