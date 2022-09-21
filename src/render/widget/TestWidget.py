import pygame

from render.animation.Animation import Animation
from render.animation.AppearEffect import AppearEffect
from render.widget.Widget import Widget
from utils import timing_functions


class TestWidget(Widget):

    def __init__(self):
        super().__init__()
        self.animation_surface = pygame.Surface((50, 50), flags=pygame.SRCALPHA)
        self.animation_surface.fill(pygame.Color(255, 0, 0))
        self.animation = Animation([AppearEffect(timing_functions.cursor)], 1)
        self.animation.start()

    def get_bb(self):
        return pygame.Rect(100, 100, 100, 100)

    def draw(self, surface):
        surface.fill(pygame.Color(255, 255, 255))
        self.animation.render(self.animation_surface)
        surface.blit(self.animation_surface, (0, 0))
