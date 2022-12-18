from render.Window import Window
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.tasks_tree.modify_layout.ModifyLayoutTreeWidget import ModifyLayoutTreeWidget


class ModifyLayoutScreen(Screen):

    """
    This represents the screen that is displayed when the user wants to modify the layout of a project.
    The user can modify the layout of the project by moving links around.

    These are the fields of a ModifyLayoutScreen :
    - project : The Project we are modifying the layout of.
    - tree_widget : The TreeWidget that displays the layout of the Project and allows the user to modify it.
    - confirm_button : The ButtonWidget that allows the user to go back to the previous Screen.
    """

    def __init__(self, project, last_screen):
        """
        Creates a new ModifyLayoutScreen
        :param project: The Project we are modifying the layout of
        :param last_screen: The screen we should go back to when we are done modifying the layout
        """
        self.project = project
        self.tree_widget = ModifyLayoutTreeWidget((0, 0), (1920, 1080), project)
        self.confirm_button = ButtonWidget((20, 20), (150, 70), "Retour",
                                           lambda: Window.instance.set_screen(last_screen), font_size=30, bold=True)

    def get_widgets(self):
        """
        Returns the list of widgets we should be displaying on this frame.
        :return: A generator returning the widgets that should be displayed.
        """
        yield self.tree_widget
        yield self.confirm_button
