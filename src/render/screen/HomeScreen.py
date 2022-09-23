import pygame

from src.render.screen.Screen import Screen
from src.render.widget.ListWidget import ListWidget


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
        self.project_list = ListWidget(pygame.Rect(100, 100, 300, 50), ["Hello", "World", "Hope", "You're", "Fine"])

    def get_widgets(self):
        """
        Returns the list of widgets we should be displaying on this frame.
        :return: A generator returning the widgets that should be displayed.
                 There, the only element in the generator is the widget project_list
        """
        yield self.project_list
