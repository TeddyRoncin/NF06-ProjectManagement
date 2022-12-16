from Task import Task
from render.Window import Window
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.CheckboxWidget import CheckboxWidget
from render.widget.EntryWidget import EntryWidget
from render.widget.LabelWidget import LabelWidget
from render.widget.tasks_tree.add_task.AddTaskTreeWidget import AddTaskTreeWidget
from utils import c_functions


class AddTaskScreen(Screen):

    def __init__(self, project, last_screen):
        self.project = project
        self.new_branch_checkbox = CheckboxWidget((200, 200), "Créer sur une nouvelle branche ?")
        self.new_branch_checkbox.enabled = False
        self.tree_widget = AddTaskTreeWidget((100, 100), project, self.new_branch_checkbox)
        self.name_widget = EntryWidget((10, 50), (100, 30), (100, 30), 100, False)
        self.error_widget = LabelWidget((10, 10), "")
        self.description_widget = EntryWidget((10, 90), (200, 100), (200, 100), -1, True)
        self.add_task_button = ButtonWidget((300, 300), (100, 25), "Ajouter", self.on_add_task)
        self.last_screen = last_screen

    def get_widgets(self):
        yield self.tree_widget
        yield self.name_widget
        yield self.error_widget
        yield self.description_widget
        yield self.add_task_button
        yield self.new_branch_checkbox

    def on_add_task(self):
        if self.name_widget.get_content() == "":
            self.error_widget.set_text("Le nom de la tâche ne peut pas être vide")
            return
        upstream_tasks = self.tree_widget.selected_tasks
        if len(upstream_tasks) == 0:
            self.error_widget.set_text("Vous devez sélectionner au moins une tâche parente")
            return
        self.project.add_task(self.name_widget.get_content(),
                              self.description_widget.get_content(),
                              upstream_tasks,
                              self.new_branch_checkbox.activated)
        Window.instance.set_screen(self.last_screen)

