import pygame

from render.widget.Widget import Widget


class GanttTaskWidget(Widget):

    def __init__(self, task, position):
        super().__init__()
        self.task = task
        self.bb = pygame.Rect(position[0] - 20, position[1] - 20, 40, 40)

    def draw(self, surface):
        pygame.draw.circle(surface, pygame.Color(255, 0, 0), (20, 20), 20)
        font = pygame.font.SysFont("Arial", 10)
        surface.blit(font.render(self.task.name, False, pygame.Color(0, 255, 0)), (10, 10))
