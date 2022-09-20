import string

import pygame

from src.render.Widget import Widget
from src.render.ScrollBarWidget import ScrollBarWidget


class EntryWidget(Widget):

    def __init__(self, pos, min_size, max_size, max_chars, multiple_lines):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 16)
        self.font_height = self.font.size(string.printable)[1] + 4
        self.min_size = (min_size[0], max(min_size[1], self.font_height))
        self.bb = pygame.Rect(pos, min_size)
        self.max_size = max_size
        self.max_chars = max_chars
        self.multiple_lines = multiple_lines
        self.focus = False
        self.content = ""
        self.horizontal_scroll_bar = ScrollBarWidget(
            pygame.Rect(self.bb.x, self.bb.y + self.bb.height - 5, self.bb.width, 5), False)
        self.vertical_scroll_bar = ScrollBarWidget(
            pygame.Rect(self.bb.x + self.bb.width - 5, self.bb.y, 5, self.bb.height), True)

    def get_children(self):
        yield self.horizontal_scroll_bar
        yield self.vertical_scroll_bar

    def draw(self, surface):
        text_surfaces = []
        width = 0
        for text in self.content.split("\n"):
            text_surface = self.font.render(text, True, pygame.Color(255, 255, 255))
            # The first element is the surface and the second is the y coordinate the text should be drawn to
            text_surfaces.append(text_surface)
            width = max(width, text_surface.get_width() + 4)
        requested_size = (max(self.min_size[0], width), max(self.min_size[1], len(text_surfaces) * self.font_height))
        self.bb.width = min(self.max_size[0], requested_size[0])
        self.bb.height = min(self.max_size[1], requested_size[1])
        self.horizontal_scroll_bar.bb = pygame.Rect(self.bb.x, self.bb.y + self.bb.height - 5, self.bb.width, 5)
        self.vertical_scroll_bar.bb = pygame.Rect(self.bb.x + self.bb.width - 5, self.bb.y, 5, self.bb.height)
        self.horizontal_scroll_bar.ratio = self.bb.width / requested_size[0]
        self.vertical_scroll_bar.ratio = self.bb.height / requested_size[1]
        background_color = pygame.Color(150, 150, 150)
        if self.focus:
            background_color = pygame.Color(200, 200, 200)
        surface.fill(background_color)
        for i, text_surface in enumerate(text_surfaces):
            surface.blit(text_surface, (
                2 - (requested_size[0] - self.bb.width) * self.horizontal_scroll_bar.scroll,
                i * self.font_height + 2 - (requested_size[1] - self.bb.height) * self.vertical_scroll_bar.scroll))

    def on_left_click(self, pos):
        self.focus = self.is_in_relative_bb(pos)

    def on_key_press(self, event):
        if self.focus:
            if event.key == pygame.K_BACKSPACE:
                self.content = self.content[:-1]
            elif event.key == pygame.K_RETURN:
                if self.multiple_lines:
                    self.content += "\n"
            elif len(self.content) < self.max_chars:
                self.content += event.unicode


__all__ = [EntryWidget]
