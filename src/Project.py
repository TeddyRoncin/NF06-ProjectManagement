from Task import Task
import pygame


class Project:
    """
    Represents a project. A project has a name, a description. The goal of the project is a task : complete the project.
    """
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.project_task = Task(name)
