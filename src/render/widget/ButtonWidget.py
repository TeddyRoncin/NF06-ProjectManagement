import pygame

from render.widget.Widget import Widget


class ButtonWidget(Widget):

    def __init__(self, pos, size, text, on_click, font_size=16, bold=False):
        super().__init__()
        self.on_click = on_click
        self.bb = pygame.Rect(pos, size)
        self.font = pygame.font.SysFont("Arial", font_size, bold=bold)
        self.surface = self.font.render(text, True, (255, 255, 255))

    def draw(self, surface):
        surface.fill(0x555555)
        surface.blit(self.surface,
                     ((self.bb.width - self.surface.get_width()) / 2,
                      (self.bb.height - self.surface.get_height()) / 2))

    def on_left_click_bb(self, pos):
        self.on_click()
