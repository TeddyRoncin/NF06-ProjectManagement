from render.Window import Window
from render.screen.AddTaskScreen import AddTaskScreen
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.tasks_tree.TreeWidget import TreeWidget


class ProjectScreen(Screen):

    def __init__(self, project):
        self.project = project
        self.gantt_widget = TreeWidget((100, 100), project.beginning_task)
        self.add_task_widget = ButtonWidget((500, 500), (30, 15), "Ajouter une tâche", self.on_add_widget)
        self.save_project_widget = ButtonWidget((700, 700), (100, 30), "Sauvegarder le projet", self.project.save)

    def get_widgets(self):
        yield self.gantt_widget
        yield self.add_task_widget
        yield self.save_project_widget

    def reload(self):
        self.gantt_widget.reload()

    def on_add_widget(self):
        Window.instance.set_screen(AddTaskScreen(self.project, self))

