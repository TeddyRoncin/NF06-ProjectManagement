import pygame

from src.render.Widget import Widget
from src.utils.mathutils import clamp


class ScrollBarWidget(Widget):

    def __init__(self, bb, ratio=1):
        super().__init__()
        # A number between 0 and 1 reprensenting the scroll. 0 is the left or right, 1 is the bottom or top
        self.scroll = 0
        self.bb = bb
        # The ratio between the displayed size and the total size
        self.ratio = ratio
        self.scrolling = False

    def draw(self, surface):
        # Draw nothing if no scrollbar is needed
        if self.ratio >= 1:
            #surface.fill(pygame.Color(275, 275, 275))
            return
        surface.fill((125, 125, 125))
        scroll_bar_height = self.bb.height * self.ratio
        pygame.draw.rect(surface,
                         pygame.Color(175, 175, 175),
                         pygame.Rect(0, (self.bb.height - scroll_bar_height) * self.scroll, self.bb.width, scroll_bar_height))

    def on_mouse_motion_bb(self, pos, motion, buttons):
        if self.ratio >= 1 or not buttons[pygame.BUTTON_LEFT - 1]:
            return
        scroll_bar_height = self.bb.height * self.ratio
        new_pos = clamp(pos[1] - (scroll_bar_height / 2), 0, self.bb.height - scroll_bar_height + 1)
        self.scroll = new_pos / (self.bb.height - scroll_bar_height)
