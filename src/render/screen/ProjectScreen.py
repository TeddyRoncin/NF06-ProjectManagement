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

    """
    This is the main Screen for managing a project. It is divided in 4 parts:
    - The tree view of the tasks.
    - The Gantt diagram of the project, displaying the earliest possible dates for starting and finishing each task.
    - The Gantt diagram of the project, displaying the latest possible dates for starting and finishing each task.
    - The actions we can do on the project
      (add a Task, modify the layout of the tasks, access the project settings, save the project, close the project)

    These are the fields of a ProjectScreen:
    - project: The Project that the user is consulting.
    - menu: The id of the menu that the user is currently viewing.
    - menu_buttons: A list of 4 buttons that allow the user to switch between the 4 different menus.
    - task_information_widget: The TaskInformationWidget that displays the information of the selected task.
                               If no task is selected, this widget is not displayed.
    - tree_widget: The ShowTasksTreeWidget that displays the tree view of the tasks.
    - add_task_widget: The ButtonWidget that allows the user to add a task to the project.
    - modify_layout_widget: The ButtonWidget that allows the user to modify the layout of the tasks.
    - project_settings_widget: The ButtonWidget that allows the user to access the project settings.
    - save_project_widget: The ButtonWidget that allows the user to save the project.
    - go_back_widget: The ButtonWidget that allows the user to close the project.
    - earliest_gantt_widget: The GanttWidget that displays the earliest possible dates
                             for starting and finishing each task.
    - latest_gantt_widget: The GanttWidget that displays the latest possible dates for starting and finishing each task.
    """

    def __init__(self, project):
        """
        Creates a new ProjectScreen
        :param project: The Project that the user is consulting.
        """
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
        self.task_information_widget = TaskInformationWidget((10, 870), self.delete_task)
        self.tree_widget = ShowTasksTreeWidget((0, 100),
                                               (1920, 980),
                                               project,
                                               self.task_information_widget.set_task)
        self.add_task_widget = ButtonWidget((710, 200), (500, 100), "Ajouter une tâche", self.on_add_widget, font_size=30, bold=True)
        self.modify_layout_widget = ButtonWidget((710, 310), (500, 100), "Modifier la disposition", self.modify_layout, font_size=30, bold=True)
        self.project_settings_widget = ButtonWidget((710, 420), (500, 100), "Paramètres du projet", self.go_to_settings, font_size=30, bold=True)
        self.save_project_widget = ButtonWidget((710, 530), (500, 100), "Sauvegarder le projet", self.project.save, font_size=30, bold=True)
        self.go_back_widget = ButtonWidget((710, 640), (500, 100), "Fermer le projet", self.on_close_project, font_size=30, bold=True)
        self.earliest_gantt_widget = GanttWidget(pygame.Rect(0, 100, 1920, 980), project, True)
        self.latest_gantt_widget = GanttWidget(pygame.Rect(0, 100, 1920, 980), project, False)

    def get_widgets(self):
        """
        Returns the list of Widgets that are displayed on the Screen
        :return: A generator returning the Widgets that are displayed on the screen.
        """
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
        """
        Reloads the Screen. It reloads the TreeWidget and the GanttWidgets
        :return: None
        """
        self.tree_widget.reload()
        self.earliest_gantt_widget.reload()
        self.latest_gantt_widget.reload()

    def on_add_widget(self):
        """
        Callback from self.add_task_widget. It is called when the user wants to add a new Task.
        It opens the AddTaskScreen
        :return: None
        """
        Window.instance.set_screen(AddTaskScreen(self.project, self))

    def go_to_settings(self):
        """
        Callback from self.project_settings_widget. It is called when the user wants to access the project settings
        :return: None
        """
        Window.instance.set_screen(ProjectSettingsScreen(self.project, self))

    def delete_task(self):
        """
        Callback from self.task_information_widget. It is called when the user wants to delete the selected task.
        Deletes the given task from the project
        :return: None
        """
        self.project.remove_task(self.tree_widget.selected_task)
        self.reload()

    def modify_layout(self):
        """
        Callback from self.modify_layout_widget. It is called when the user wants to modify the layout of the Project.
        It sets the screen to a ModifyLayoutScreen
        :return: None
        """
        Window.instance.set_screen(ModifyLayoutScreen(self.project, self))

    def change_menu(self, menu):
        """
        Changes the menu that is currently displayed
        :param menu: The id of the menu to display
        :return: None
        """
        self.menu = menu
        for i, btn in enumerate(self.menu_buttons):
            btn.rerender(bold=(i == self.menu))

    @staticmethod
    def on_close_project():
        """
        Callback from self.go_back_widget. It is called when the user wants to close the Project.
        It sets the Screen to a ProjectListScreen
        :return: None
        """
        from render.screen.HomeScreen import HomeScreen
        Window.instance.set_screen(HomeScreen())



