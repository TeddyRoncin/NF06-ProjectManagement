import pygame

from Project import Project
from render.Window import Window
from render.screen.CreateProjectScreen import CreateProjectScreen
from render.screen.ProjectScreen import ProjectScreen
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.LabelWidget import LabelWidget
from render.widget.ProjectListWidget import ProjectListWidget


class HomeScreen(Screen):

    """
    The Screen that is displayed when the user wants to choose what he wants to do.
    The user can choose a project to launch, create a new project, or quit the application.

    These are the fields of a HomeScreen :
    - project_list : The ListWidget of all the projects that were loaded
    """

    def __init__(self):
        """
        Creates a new HomeScreen
        """
        self.projects = Project.projects
        self.label = LabelWidget((0, 30), "Liste des projets", font_size=30, bold=True, color=(0, 0, 0))
        self.label.bb.left = (1920 - self.label.bb.width) / 2
        self.project_list = ProjectListWidget(pygame.Rect(460, 100, 1000, 700),
                                              self.projects,
                                              on_item_clicked=self.on_select_project)
        self.create_project_button = ButtonWidget((810, 900), (300, 100), "Créer un projet", self.on_create_project,
                                                  font_size=30, bold=True)

    def get_widgets(self):
        """
        Returns the list of widgets we should be displaying on this frame.
        :return: A generator returning the widgets that should be displayed.
        """
        yield self.label
        yield self.project_list
        yield self.create_project_button

    def set_projects(self, projects):
        """
        Modifies the list of projects
        :param projects: The new list of projects
        :return: None
        """
        self.projects = projects
        self.project_list.set_projects(projects)

    @staticmethod
    def on_select_project(project):
        """
        Callback from self.project_list. It is called when the user clicks on a project
        It redirects the user to the ProjectScreen of the clicked Project
        :param project: The Project that was clicked
        :return: None
        """
        Window.instance.set_screen(ProjectScreen(project))

    @staticmethod
    def on_create_project():
        """
        Callback from self.create_project_button. It is called when the user wants to create a new project.
        It redirects the user to the CreateProjectScreen
        :return: None
        """
        Window.instance.set_screen(CreateProjectScreen())
