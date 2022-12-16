import pygame

from render.widget.Widget import Widget


class LabelWidget(Widget):

    def __init__(self, pos, text, font_size=16, bold=False, color=(255, 255, 255)):
        super().__init__()
        self.color = color
        self.font = pygame.font.SysFont("Arial", font_size, bold=bold)
        self.text_render = None
        self.bb = pygame.Rect(pos, (0, 0))
        self.set_text(text)

    def draw(self, surface):
        surface.blit(self.text_render, (0, 0))

    def set_text(self, text):
        self.text_render = self.font.render(text, False, self.color)
        self.bb = pygame.Rect(self.bb.topleft, (self.text_render.get_width(), self.text_render.get_height()))
