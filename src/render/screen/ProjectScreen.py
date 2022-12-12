from render.GanttWidget import GanttWidget
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
                                               project.beginning_task,
                                               self.task_information_widget.set_task)
        self.add_task_widget = ButtonWidget((500, 500), (30, 15), "Ajouter une tâche", self.on_add_widget)
        self.save_project_widget = ButtonWidget((700, 700), (100, 30), "Sauvegarder le projet", self.project.save)
        self.project_settings_widget = ButtonWidget((700, 750), (100, 30), "Paramètres du projet", self.go_to_settings)
        self.gantt_widget = GanttWidget(project)

    def get_widgets(self):
        yield self.tree_widget
        yield self.add_task_widget
        yield self.save_project_widget
        yield self.project_settings_widget
        if self.tree_widget.selected_task is not None:
            yield self.task_information_widget
        yield self.gantt_widget

    def reload(self):
        self.tree_widget.reload()

    def on_add_widget(self):
        Window.instance.set_screen(AddTaskScreen(self.project, self))

    def go_to_settings(self):
        Window.instance.set_screen(ProjectSettingsScreen(self.project, self))

    def delete_task(self, task):
        # This is a branch with a length of 1, so we simply need to remove it
        if len(task.upstream_tasks[0].downstream_tasks) > 1 and len(task.downstream_tasks[0].upstream_tasks) > 1:
            # The task cannot have multiple upstream and downstream tasks
            task.remove_upstream_task(task.upstream_tasks[0])
            task.downstream_tasks[0].remove_upstream_task(task)
        elif len(task.upstream_tasks) > 1:
            upstream_tasks = list(task.upstream_tasks)
            for upstream_task in upstream_tasks:
                print(upstream_task)
                print(upstream_task.downstream_tasks)
                task.remove_upstream_task(upstream_task)
                task.downstream_tasks[0].add_upstream_task(upstream_task)
                print(upstream_task.downstream_tasks)
            task.downstream_tasks[0].remove_upstream_task(task)
        elif len(task.downstream_tasks) > 1:
            downstream_tasks = list(task.downstream_tasks)
            for downstream_task in downstream_tasks:
                downstream_task.remove_upstream_task(task)
                downstream_task.add_upstream_task(task.upstream_tasks[0])
            task.remove_upstream_task(task.upstream_tasks[0])
        else:
            task.downstream_tasks[0].add_upstream_task(task.upstream_tasks[0])
            task.remove_upstream_task(task.upstream_tasks[0])
            task.downstream_tasks[0].remove_upstream_task(task)
        self.reload()



