import pygame

from src.render.widget.Widget import Widget
from src.render.widget.ScrollBarWidget import ScrollBarWidget
from src.utils.pygame_utils import get_font_height


class ListWidget(Widget):

    def __init__(self, bb, items):
        super().__init__()
        self.bb = bb
        self.items = items
        self.font = pygame.font.SysFont("Arial", 16)
        self.item_height = get_font_height(self.font)
        self.total_height = len(self.items) * self.item_height
        self.scrollbar = ScrollBarWidget(self.get_bb, lambda: self.total_height)

    def get_children(self):
        yield self.scrollbar

    def draw(self, surface):
        surface.fill(pygame.Color(100, 100, 0))
        scroll = self.get_scroll_in_pixel()
        for i, item in enumerate(self.items):
            surface.blit(self.font.render(item, True, pygame.Color(255, 255, 255)), (0, i * self.item_height - scroll))

    def on_left_click_bb(self, pos):
        item_clicked = int((pos[1] + self.get_scroll_in_pixel()) / self.item_height)

    def get_scroll_in_pixel(self):
        return self.scrollbar.get_scroll_in_pixel()
