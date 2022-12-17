from render.Window import Window
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.tasks_tree.modify_layout.ModifyLayoutTreeWidget import ModifyLayoutTreeWidget


class ModifyLayoutScreen(Screen):

    def __init__(self, project, last_screen):
        self.project = project
        self.tree_widget = ModifyLayoutTreeWidget((0, 0), (1920, 1080), project)
        self.confirm_button = ButtonWidget((20, 20), (150, 70), "Retour", lambda: Window.instance.set_screen(last_screen), font_size=30, bold=True)

    def get_widgets(self):
        yield self.tree_widget
        yield self.confirm_button
