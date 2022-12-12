import pygame

from render.widget.ButtonWithConfirmationWidget import ButtonWithConfirmationWidget
from render.widget.Widget import Widget


class TaskInformationWidget(Widget):

    def __init__(self, pos, on_delete_task):
        super().__init__()
        self.bb = pygame.Rect(pos, (600, 200))
        self.task = None
        self.font = pygame.font.SysFont("Arial", 20)
        self.render = None
        self.can_delete = True
        self.delete_button = ButtonWithConfirmationWidget((self.bb.x + 300, self.bb.y + 10), (100, 50), "Supprimer", lambda: on_delete_task(self.task))

    def get_children(self):
        if self.task is not None and self.can_delete:
            yield self.delete_button

    def draw(self, surface):
        if self.task is None:
            return
        surface.blit(self.render, (0, 0))

    def generate_render(self):
        if self.task is None:
            return
        self.render = pygame.Surface((600, 200))
        self.render.fill((255, 255, 255))
        self.render.blit(self.font.render(self.task.name, True, (0, 0, 0)), (3, 3))
        self.render.blit(self.font.render(self.task.description, True, (0, 0, 0)), (3, 23))
        self.render.blit(self.font.render("Index de la tâche : " + str(self.task.index), True, (0, 0, 0)), (3, 43))
        self.render.blit(self.font.render("Durée estimée : " + str(self.task.estimated_time), True, (0, 0, 0)), (3, 63))
        self.render.blit(self.font.render("Peut démarrer à partir de : " + str(self.task.earliest_start), True, (0, 0, 0)), (3, 83))
        self.render.blit(self.font.render("Peut démarrer jusqu'au : " + str(self.task.latest_start), True, (0, 0, 0)), (3, 103))
        self.render.blit(self.font.render("Statut : " + str(self.task.status), True, (0, 0, 0)), (3, 123))

    def set_task(self, task):
        self.task = task
        self.generate_render()
        if self.task is None:
            return
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

