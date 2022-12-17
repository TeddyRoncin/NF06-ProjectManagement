import pygame

from TaskStatus import TaskStatus
from render.widget.ButtonWithConfirmationWidget import ButtonWithConfirmationWidget
from render.widget.Widget import Widget


class TaskInformationWidget(Widget):

    def __init__(self, pos, on_delete_task):
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
        self.delete_button = ButtonWithConfirmationWidget((self.bb.x + 1590, self.bb.y + 100), (300, 80), "Supprimer", lambda: on_delete_task(self.task), font_size=30)

    def get_children(self):
        if self.task is not None and self.can_change_status:
            yield self.change_status_button
        if self.task is not None and self.can_delete:
            yield self.delete_button

    def draw(self, surface):
        if self.task is None:
            return
        surface.blit(self.render, (0, 0))

    def generate_render(self):
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
        self.task.status = self.task.status.next_status()
        self.change_status_button.rerender(text="Prochain statut : " + str(self.task.status))
        self.generate_render()
        if self.task.status == TaskStatus.FINISHED:
            for task in self.task.downstream_tasks:
                task.status = TaskStatus.NOT_STARTED
            self.can_change_status = False

    def set_task(self, task):
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

