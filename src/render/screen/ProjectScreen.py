import pygame

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
        self.menu = 0
        self.menu_buttons = [ButtonWidget((0, 0), (479, 100), "Vue générale du projet", lambda: self.change_menu(0),
                                          font_size=24, bold=True),
                             ButtonWidget((480, 0), (479, 100), "Diagramme de Gantt (dates au plus tôt)",
                                          lambda: self.change_menu(1), font_size=24),
                             ButtonWidget((960, 0), (479, 100), "Diagramme de Gantt (dates au plus tard)",
                                          lambda: self.change_menu(2), font_size=24),
                             ButtonWidget((1440, 0), (479, 100), "Actions", lambda: self.change_menu(3), font_size=24)]
        self.task_information_widget = TaskInformationWidget((100, 500), self.delete_task)
        self.tree_widget = ShowTasksTreeWidget((0, 100),
                                               (1920, 980),
                                               project,
                                               self.task_information_widget.set_task)
        self.go_back_widget = ButtonWidget((20, 120), (150, 70), "Retour", self.on_going_back, font_size=30, bold=True)
        self.add_task_widget = ButtonWidget((710, 200), (500, 100), "Ajouter une tâche", self.on_add_widget, font_size=30, bold=True)
        self.modify_layout_widget = ButtonWidget((710, 310), (500, 100), "Modifier la disposition", self.modify_layout, font_size=30, bold=True)
        self.project_settings_widget = ButtonWidget((710, 420), (500, 100), "Paramètres du projet", self.go_to_settings, font_size=30, bold=True)
        self.save_project_widget = ButtonWidget((710, 530), (500, 100), "Sauvegarder le projet", self.project.save, font_size=30, bold=True)
        self.earliest_gantt_widget = GanttWidget(pygame.Rect(0, 100, 1920, 980), project, True)
        self.latest_gantt_widget = GanttWidget(pygame.Rect(0, 100, 1920, 980), project, False)

    def get_widgets(self):
        yield from self.menu_buttons
        if self.menu == 0:
            yield self.tree_widget
            if self.tree_widget.selected_task is not None:
                yield self.task_information_widget
        elif self.menu == 1:
            yield self.earliest_gantt_widget
        elif self.menu == 2:
            yield self.latest_gantt_widget
        else:
            yield self.go_back_widget
            yield self.add_task_widget
            yield self.save_project_widget
            yield self.project_settings_widget
            yield self.modify_layout_widget

    def reload(self):
        self.tree_widget.reload()
        self.earliest_gantt_widget.reload()
        self.latest_gantt_widget.reload()

    def on_add_widget(self):
        Window.instance.set_screen(AddTaskScreen(self.project, self))

    def go_to_settings(self):
        Window.instance.set_screen(ProjectSettingsScreen(self.project, self))

    def delete_task(self, task):
        self.project.remove_task(task)
        self.reload()

    def modify_layout(self):
        Window.instance.set_screen(ModifyLayoutScreen(self.project))

    def change_menu(self, menu):
        self.menu = menu
        for i, btn in enumerate(self.menu_buttons):
            btn.rerender(bold=(i == self.menu))

    def on_going_back(self):
        from render.screen.HomeScreen import HomeScreen
        Window.instance.set_screen(HomeScreen())



