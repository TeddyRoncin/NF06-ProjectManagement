import pygame

from Project import Project
from render.Window import Window
from render.screen.CreateProjectScreen import CreateProjectScreen
from render.screen.ProjectScreen import ProjectScreen
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.ListWidget import ListWidget


class HomeScreen(Screen):

    """
    The Screen that is displayed when the user wants to choose what he wants to do.
    The user can choose a project to launch, create a new project, or quit the application.

    These are the fields of a HomeScreen :
    - project_list : The ListWidget of all the projects that were loaded
    """

    def __init__(self, projects=None):
        """
        Creates a new HomeScreen
        """
        if projects is None:
            projects = Project.projects
        self.projects = projects
        self.project_list = ListWidget(pygame.Rect(100, 100, 300, 50),
                                       [project.name for project in self.projects],
                                       on_item_clicked=self.on_select_project)
        self.create_project_button = ButtonWidget((100, 200), (100, 30), "Créer un projet", self.on_create_project)

    def get_widgets(self):
        """
        Returns the list of widgets we should be displaying on this frame.
        :return: A generator returning the widgets that should be displayed.
                 There, the only element in the generator is the widget project_list
        """
        yield self.project_list
        yield self.create_project_button

    def set_projects(self, projects):
        """
        Modifies the list of projects
        :param projects: The new list of projects
        :return: None
        """
        self.projects = projects
        self.project_list.set_items(projects)

    def on_select_project(self, project_name):
        """
        Callback from self.project_list. It is called when the user clicks on a project
        :param project_name: The name of the project that was clicked
        :return: None
        """
        Window.instance.set_screen(ProjectScreen(
            [project for project in self.projects if project.name == project_name][0]))

    def on_create_project(self):
        """
        Callback from self.create_project_button. It is called when the user wants to create a new project.
        :return: None
        """
        Window.instance.set_screen(CreateProjectScreen())
