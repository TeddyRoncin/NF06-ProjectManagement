import pygame

from render.animation.Animation import Animation
from render.animation.AppearEffect import AppearEffect
from render.widget.Widget import Widget
from render.widget.ScrollBarWidget import ScrollBarWidget
from utils import timing_functions


class EntryWidget(Widget):

    def __init__(self, pos, min_size, max_size, max_chars, multiple_lines, default_content=""):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 16)
        self.font_height = self.font.get_height() + 4
        self.min_size = (min_size[0], max(min_size[1], self.font_height))
        self.bb = pygame.Rect(pos, min_size)
        self.max_size = max_size
        self.max_chars = max_chars
        self.multiple_lines = multiple_lines
        self.focus = False
        self.content = [""]
        self.total_size = self.min_size
        self.horizontal_scroll_bar = ScrollBarWidget(self.get_bb, lambda: self.total_size[0], is_vertical=False)
        self.vertical_scroll_bar = ScrollBarWidget(self.get_bb, lambda: self.total_size[1], is_vertical=True)
        self.cursor_position = [0, 0]
        self.cursor_surface = pygame.Surface((2, self.font.get_height()))
        self.cursor_animation = self._generate_cursor_animation()
        self.set_content(default_content)

    def _generate_cursor_animation(self):
        animation_effect = AppearEffect(timing_functions.cursor)
        animation = Animation([animation_effect], 1)
        animation.render_no_update(self.cursor_surface)
        return animation

    def get_children(self):
        yield self.horizontal_scroll_bar
        yield self.vertical_scroll_bar

    def draw(self, surface):
        text_surfaces = []
        width = 0
        for text in self.content:
            text_surface = self.font.render(text, True, pygame.Color(255, 255, 255))
            # The first element is the surface and the second is the y coordinate the text should be drawn to
            text_surfaces.append(text_surface)
            width = max(width, text_surface.get_width() + 4)
        self.total_size = (max(self.min_size[0], width), max(self.min_size[1], len(text_surfaces) * self.font_height))
        self.bb.width = min(self.max_size[0], self.total_size[0])
        self.bb.height = min(self.max_size[1], self.total_size[1])
        background_color = pygame.Color(150, 150, 150)
        if self.focus:
            background_color = pygame.Color(200, 200, 200)
        surface.fill(background_color)
        for i, text_surface in enumerate(text_surfaces):
            surface.blit(text_surface, (
                2 - (self.total_size[0] - self.bb.width) * self.horizontal_scroll_bar.scroll,
                i * self.font_height + 2 - (self.total_size[1] - self.bb.height) * self.vertical_scroll_bar.scroll))
        self.cursor_animation.render(self.cursor_surface)
        # Raw x and y positions of the cursor
        x = self.font.size(self.content[self.cursor_position[0]][:self.cursor_position[1]])[0] + 1
        y = self.cursor_position[0] * self.font_height + 2
        # Apply scrolling
        x -= (self.total_size[0] - self.bb.width) * self.horizontal_scroll_bar.scroll
        y -= (self.total_size[1] - self.bb.height) * self.vertical_scroll_bar.scroll
        surface.blit(self.cursor_surface, (x, y))

    def on_left_click(self, pos):
        gained_focus = self.is_in_relative_bb(pos)
        if not self.focus and gained_focus:
            self.cursor_animation.start()
        elif self.focus and not gained_focus:
            self.cursor_animation.stop()
            self.cursor_animation.render_no_update(self.cursor_surface)
        self.focus = gained_focus

    def on_key_press(self, event):
        if self.focus:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_position[1] != 0:
                    self.content[self.cursor_position[0]] = \
                        self.content[self.cursor_position[0]][:self.cursor_position[1]-1] + \
                        self.content[self.cursor_position[0]][self.cursor_position[1]:]
                    self.cursor_position[1] -= 1
                # If it is the first character of the first line, we don't want to delete anything
                elif self.cursor_position[0] > 0:
                    line = self.content[self.cursor_position[0]]
                    del self.content[self.cursor_position[0]]
                    self.cursor_position[0] -= 1
                    self.cursor_position[1] = len(self.content[self.cursor_position[0]])
                    self.content[self.cursor_position[0]] += line
            elif event.key == pygame.K_RETURN:
                if self.multiple_lines:
                    end_of_line = self.content[self.cursor_position[0]][self.cursor_position[1]:]
                    self.content[self.cursor_position[0]] = \
                        self.content[self.cursor_position[0]][:self.cursor_position[1]]
                    self.cursor_position[0] += 1
                    self.cursor_position[1] = 0
                    self.content.insert(self.cursor_position[0], end_of_line)
            elif event.key == pygame.K_LEFT:
                if self.cursor_position[1] != 0:
                    self.cursor_position[1] -= 1
                elif self.cursor_position[0] != 0:
                    self.cursor_position[0] -= 1
                    self.cursor_position[1] = len(self.content[self.cursor_position[0]])
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position[1] != len(self.content[self.cursor_position[0]]):
                    self.cursor_position[1] += 1
                elif self.cursor_position[0] != len(self.content) - 1:
                    self.cursor_position[0] += 1
                    self.cursor_position[1] = 0
            elif len(self.content) < self.max_chars or self.max_chars == -1:
                self.content[self.cursor_position[0]] = \
                    self.content[self.cursor_position[0]][:self.cursor_position[1]] + \
                    event.unicode + \
                    self.content[self.cursor_position[0]][self.cursor_position[1]:]
                self.cursor_position[1] += 1

    def get_content(self):
        return "\n".join(self.content)

    def set_content(self, content):
        self.content = content.split("\n")
        self.cursor_position = [0, 0]


__all__ = [EntryWidget]
