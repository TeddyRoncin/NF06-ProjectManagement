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
        self.new_branch_checkbox = CheckboxWidget((1500, 750), "Créer sur une nouvelle branche ?")
        self.new_branch_checkbox.enabled = False
        self.tree_widget = AddTaskTreeWidget((0, 0), (1920, 1080), project, self.new_branch_checkbox)
        self.go_back_button = ButtonWidget((20, 20), (150, 70), "Retour", self.go_back, font_size=30, bold=True)
        self.name_label = LabelWidget((1500, 50), "Nom de la tâche :", font_size=30)
        self.name_widget = EntryWidget((1500, 100), (400, 30), (400, 30), 100, False)
        self.name_error_widget = LabelWidget((1500, 130), "", color=(255, 0, 0), font_size=20)
        self.description_label = LabelWidget((1500, 200), "Description :", font_size=30)
        self.description_widget = EntryWidget((1500, 250), (400, 300), (400, 300), -1, True)
        self.duration_label = LabelWidget((1500, 600), "Durée estimée (en jours) :", font_size=30)
        self.duration_widget = EntryWidget((1500, 650), (400, 30), (400, 30), 2, False)
        self.duration_error_widget = LabelWidget((1500, 680), "", color=(255, 0, 0), font_size=20)
        self.add_task_button = ButtonWidget((1500, 800), (400, 50), "Ajouter", self.on_add_task)
        self.upstream_tasks_error = LabelWidget((1500, 850), "", color=(255, 0, 0), font_size=20)
        self.last_screen = last_screen

    def get_widgets(self):
        yield self.tree_widget
        yield self.go_back_button
        yield self.name_label
        yield self.name_widget
        yield self.name_error_widget
        yield self.description_label
        yield self.description_widget
        yield self.duration_label
        yield self.duration_widget
        yield self.duration_error_widget
        yield self.new_branch_checkbox
        yield self.add_task_button
        yield self.upstream_tasks_error

    def on_add_task(self):
        is_valid = True
        if self.name_widget.get_content() == "":
            self.name_error_widget.set_text("Le nom de la tâche ne peut pas être vide")
            is_valid = False
        else:
            self.name_error_widget.set_text("")
        estimated_time = self.duration_widget.get_content()
        try:
            estimated_time = int(estimated_time)
        except ValueError:
            self.duration_error_widget.set_text("Vous devez entrer un nombre valide de jours")
            is_valid = False
        else:
            self.duration_error_widget.set_text("")
        upstream_tasks = self.tree_widget.selected_tasks
        if len(upstream_tasks) == 0:
            self.upstream_tasks_error.set_text("Vous devez sélectionner au moins une tâche")
            is_valid = False
        else:
            self.upstream_tasks_error.set_text("")
        if not is_valid:
            return
        self.project.add_task(self.name_widget.get_content(),
                              self.description_widget.get_content(),
                              estimated_time,
                              upstream_tasks,
                              self.new_branch_checkbox.activated)
        Window.instance.set_screen(self.last_screen)

    def go_back(self):
        Window.instance.set_screen(self.last_screen)

