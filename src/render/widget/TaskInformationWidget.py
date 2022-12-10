import pygame

from render.widget.Widget import Widget


class TaskInformationWidget(Widget):

    def __init__(self, pos):
        super().__init__()
        self.bb = pygame.Rect(pos, (600, 200))
        self.task = None
        self.font = pygame.font.SysFont("Arial", 20)
        self.render = None

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
        self.render.blit(self.font.render("Durée estimée : " + str(self.task.estimated_time), True, (0, 0, 0)), (3, 43))
        self.render.blit(self.font.render("Statut : " + str(self.task.status), True, (0, 0, 0)), (3, 63))

    def set_task(self, task):
        self.task = task
        self.generate_render()
