from render.screen.ModifyLayoutScreen import ModifyLayoutScreen
from render.widget.GanttWidget import GanttWidget
from render.Window import Window
from render.screen.AddTaskScreen import AddTaskScreen
from render.screen.ProjectSettingsScreen import ProjectSettingsScreen
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.TaskInformationWidget import TaskInformationWidget
from render.widget.tasks_tree.show_tasks.ShowTasksTreeWidget import ShowTasksTreeWidget


class ProjectScreen(Screen):

    def __init__(self, project):
        self.project = project
        self.project.load()

        self.task_information_widget = TaskInformationWidget((100, 500), self.delete_task)
        self.tree_widget = ShowTasksTreeWidget((100, 100),
                                               project,
                                               self.task_information_widget.set_task)
        self.add_task_widget = ButtonWidget((500, 500), (30, 15), "Ajouter une tâche", self.on_add_widget)
        self.save_project_widget = ButtonWidget((700, 700), (100, 30), "Sauvegarder le projet", self.project.save)
        self.project_settings_widget = ButtonWidget((700, 750), (100, 30), "Paramètres du projet", self.go_to_settings)
        self.modify_layout_widget = ButtonWidget((700, 800), (100, 30), "Modifier la disposition", self.modify_layout)
        self.gantt_widget = GanttWidget(project)

    def get_widgets(self):
        yield self.tree_widget
        yield self.add_task_widget
        yield self.save_project_widget
        yield self.project_settings_widget
        yield self.modify_layout_widget
        if self.tree_widget.selected_task is not None:
            yield self.task_information_widget
        yield self.gantt_widget

    def reload(self):
        self.tree_widget.reload()
        self.gantt_widget.reload()

    def on_add_widget(self):
        Window.instance.set_screen(AddTaskScreen(self.project, self))

    def go_to_settings(self):
        Window.instance.set_screen(ProjectSettingsScreen(self.project, self))

    def delete_task(self, task):
        self.project.remove_task(task)
        self.reload()

    def modify_layout(self):
        Window.instance.set_screen(ModifyLayoutScreen(self.project))



