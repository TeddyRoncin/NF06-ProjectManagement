import pygame

from TaskStatus import TaskStatus
from render.widget.ButtonWithConfirmationWidget import ButtonWithConfirmationWidget
from render.widget.Widget import Widget


class TaskInformationWidget(Widget):

    """
    Represents a Widget that displays information about a Task. There are also be two buttons to update the TaskStatus
    of the Task or delete it. They may not be displayed depending on if each action is or is not possible on the Task.

    These are the fields of a TaskInformationWidget :
    - bb : The bounding box of the widget.
    - task : The Task that is being displayed.
    - font : The font used to display the information.
    - render : The surface that is drawn on the screen.
               It is generated before the render to avoid generating it on every frame.
    - can_delete : Whether the Task can be deleted, resulting in the delete button being displayed or not.
    - can_change_status : Whether the Task can have its TaskStatus changed,
                          resulting in the change TaskStatus button being displayed or not.
    - change_status_button : The ButtonWithConfirmationWidget that changes the TaskStatus of the Task.
                             This action is not possible to undo, that is why a confirmation is required.
    - delete_button : The ButtonWithConfirmationWidget that deletes the Task.
                      This action is not possible to undo, that is why a confirmation is required.
    """

    def __init__(self, pos, on_delete_task):
        """
        Creates a new TaskInformationWidget
        :param pos: The position of the TaskInformationWidget
        :param on_delete_task: The function to call when the user asks the deletion of the Task
        """
        super().__init__()
        self.bb = pygame.Rect(pos, (1900, 200))
        self.task = None
        self.font = pygame.font.SysFont("Arial", 20)
        self.render = None
        self.can_delete = True
        self.can_change_status = False
        self.change_status_button = ButtonWithConfirmationWidget((self.bb.x + 1590, self.bb.y + 10),
                                                                 (300, 80),
                                                                 "Prochain statut : (Vide)",
                                                                 self.update_status,
                                                                 font_size=20)
        self.delete_button = ButtonWithConfirmationWidget((self.bb.x + 1590, self.bb.y + 100), (300, 80), "Supprimer", on_delete_task, font_size=30)

    def get_children(self):
        """
        Returns the children of the TaskInformationWidget that should be displayed
        :return: A generator returning the children of the TaskInformationWidget
        """
        if self.task is not None and self.can_change_status:
            yield self.change_status_button
        if self.task is not None and self.can_delete:
            yield self.delete_button

    def draw(self, surface):
        """
        Draws the TaskInformationWidget on the given Surface
        :param surface: The Surface to draw the TaskInformationWidget on
        :return: None
        """
        if self.task is None:
            return
        surface.blit(self.render, (0, 0))

    def generate_render(self):
        """
        Generates the render of the TaskInformationWidget. This is done to avoid generating it on every frame.
        It is called when the TaskInformationWidget is created or when the task field is changed
        (by setting it to another Task, or by modifying the TaskStatus of the Task)
        :return: None
        """
        self.render = pygame.Surface((1900, 200))
        self.render.fill((255, 255, 255))
        self.render.blit(self.font.render(self.task.name, True, (0, 0, 0)), (3, 3))
        self.render.blit(self.font.render(self.task.description, True, (0, 0, 0)), (3, 23))
        self.render.blit(self.font.render("Index de la tâche : " + str(self.task.index), True, (0, 0, 0)), (3, 43))
        self.render.blit(self.font.render("Durée estimée : " + str(self.task.estimated_time), True, (0, 0, 0)), (3, 63))
        self.render.blit(self.font.render("Peut démarrer à partir de : " + str(self.task.earliest_start), True, (0, 0, 0)), (3, 83))
        self.render.blit(self.font.render("Peut démarrer jusqu'au : " + str(self.task.latest_start), True, (0, 0, 0)), (3, 103))
        self.render.blit(self.font.render("Statut : " + str(self.task.status), True, (0, 0, 0)), (3, 123))
        self.render.blit(self.font.render("Id de la tâche : " + str(self.task.id), True, (0, 0, 0)), (3, 143))

    def update_status(self):
        """
        Updates the TaskStatus of the Task and, if needed, the TaskStatus of the downstream tasks.
        This also updates the change_status_button and regenerates the render.
        If needed, can_change_status is set to False.
        :return: None
        """
        self.task.update_status()
        self.change_status_button.rerender(text="Prochain statut : " + str(self.task.status))
        self.generate_render()
        if self.task.status == TaskStatus.FINISHED:
            for task in self.task.downstream_tasks:
                if sum(t.status == TaskStatus.FINISHED for t in task.upstream_tasks) == len(task.upstream_tasks):
                    task.status = TaskStatus.NOT_STARTED
            self.can_change_status = False

    def set_task(self, task):
        """
        Modifies the Task to display
        :param task: The new Task to display
        :return: None
        """
        self.task = task
        if self.task is None:
            return
        self.change_status_button.rerender(text="Prochain statut : " + str(self.task.status))
        self.generate_render()
        if self.task.is_beginning_task:
            self.can_delete = False
        elif self.task.is_project_task:
            self.can_delete = False
        elif len(self.task.upstream_tasks) > 1 and len(self.task.downstream_tasks[0].upstream_tasks) > 1:
            self.can_delete = False
        elif len(self.task.downstream_tasks) > 1 and len(self.task.upstream_tasks[0].downstream_tasks) > 1:
            self.can_delete = False
        else:
            self.can_delete = True
        if self.task.status == TaskStatus.FINISHED:
            self.can_change_status = False
        elif self.task.status == TaskStatus.LOCKED:
            self.can_change_status = False
        else:
            self.can_change_status = True
