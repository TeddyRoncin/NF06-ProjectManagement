from render.screen.Screen import Screen
from render.widget.tasks_tree.modify_layout.ModifyLayoutTreeWidget import ModifyLayoutTreeWidget


class ModifyLayoutScreen(Screen):

    def __init__(self, project):
        self.project = project
        self.tree_widget = ModifyLayoutTreeWidget((0, 0), project)

    def get_widgets(self):
        yield self.tree_widget
