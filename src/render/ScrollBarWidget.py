import pygame

from src.render.Widget import Widget
from src.utils.mathutils import clamp


class ScrollBarWidget(Widget):

    def __init__(self, bb, is_vertical, ratio=1):
        super().__init__()
        # A number between 0 and 1 reprensenting the scroll. 0 is the left or right, 1 is the bottom or top
        self.scroll = 0
        self.bb = bb
        # 0 is axis is X (horizontal), 1 if axis is Y (vertical)
        self.axis = int(is_vertical)
        # The ratio between the displayed size and the total size
        self.ratio = ratio
        self.scrolling = False

    def draw(self, surface):
        # Draw nothing if no scrollbar is needed
        if self.ratio >= 1:
            #surface.fill(pygame.Color(275, 275, 275))
            return
        surface.fill((125, 125, 125))
        scroll_bar_size = self.bb[2+self.axis] * self.ratio
        rect = pygame.Rect((self.bb.width - scroll_bar_size) * self.scroll, 0, scroll_bar_size, self.bb.height)
        if self.axis == 1:
            rect = pygame.Rect(0, (self.bb.height - scroll_bar_size) * self.scroll, self.bb.width, scroll_bar_size)
        pygame.draw.rect(surface,
                         pygame.Color(175, 175, 175),
                         rect)

    def on_left_click_bb(self, pos):
        self.scrolling = True

    def on_left_button_release(self):
        self.scrolling = False

    def on_mouse_motion(self, pos, motion, buttons):
        if self.ratio >= 1 or not self.scrolling:
            return
        if not buttons[pygame.BUTTON_LEFT-1]:
            self.scrolling = False
            return
        scroll_bar_size = self.bb[2+self.axis] * self.ratio
        scroll_bar_pos = clamp(pos[self.axis] - (scroll_bar_size / 2), 0, self.bb[2+self.axis] - scroll_bar_size + 1)
        self.scroll = scroll_bar_pos / (self.bb[2+self.axis] - scroll_bar_size)


__all__ = ["ScrollBarWidget"]
