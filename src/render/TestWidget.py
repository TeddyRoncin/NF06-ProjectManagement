import pygame

from src.render.Widget import Widget


class TestWidget(Widget):

    def get_bb(self):
        return pygame.Rect(100, 100, 100, 100)

    def draw(self, surface):
        surface.fill(pygame.Color(255, 255, 255))

    """def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            print("appuyé !!")
"""