import pygame

from render.widget.Widget import Widget
from src.utils.mathutils import clamp


class ScrollBarWidget(Widget):

    def __init__(self, get_parent_bb, get_total_size, is_vertical=True, mouse_scroll_amount=3):
        """
        Creates a new ScrollBarWidget element
        :param get_parent_bb: The bounding box of the parent widget
        :param get_total_size: The total height of the parent widget
        :param is_vertical: Whether this is a vertical or a horizontal scroll bar
        :param mouse_scroll_amount: How many pixels are scrolled when the mouse wheel is used
        """
        super().__init__()
        # A number between 0 and 1 reprensenting the scroll. 0 is the left or right, 1 is the bottom or top
        self.scroll = 0
        self.get_parent_bb = get_parent_bb
        self.get_total_size = get_total_size
        # 0 is axis is X (horizontal), 1 if axis is Y (vertical)
        self.axis = int(is_vertical)
        # The amount of pixel which will be scrolled
        self.mouse_scroll_amount = mouse_scroll_amount
        # self.ratio is the ratio between the displayed size and the total size
        self.bb = pygame.Rect(0, 0, 0, 0)
        self.ratio = 0
        self.refresh_values()
        # If the user is currently dragging the scroll bar
        self.is_scrolling = False

    def get_scroll_in_pixel(self):
        """
        Returns the amount that has been scrolled, in pixels.
        This is useful to compute offsets to draw a widget or find which portion of it has been clicked.
        :return: The amount that was scrolled, in pixels
        """
        return (1 - self.ratio) * self.get_total_size() * self.scroll

    def refresh_values(self):
        if self.axis == 0:
            self.bb = pygame.Rect(self.get_parent_bb().x, self.get_parent_bb().y + self.get_parent_bb().height - 5,
                                  self.get_parent_bb().width, 5)
            self.ratio = self.get_parent_bb().width / self.get_total_size()
        else:
            self.bb = pygame.Rect(self.get_parent_bb().x + self.get_parent_bb().width - 5, self.get_parent_bb().y,
                                  5, self.get_parent_bb().height)
            self.ratio = self.get_parent_bb().height / self.get_total_size()

    def draw(self, surface):
        # Draw nothing if no scrollbar is needed
        if self.ratio >= 1:
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
        self.is_scrolling = True

    def on_left_button_release(self):
        self.is_scrolling = False

    def on_mouse_motion(self, pos, motion, buttons):
        if self.ratio >= 1 or not self.is_scrolling:
            return
        if not buttons[pygame.BUTTON_LEFT-1]:
            self.is_scrolling = False
            return
        scroll_bar_size = self.bb[2+self.axis] * self.ratio
        scroll_bar_pos = clamp(pos[self.axis] - (scroll_bar_size / 2), 0, self.bb[2+self.axis] - scroll_bar_size + 1)
        self.scroll = scroll_bar_pos / (self.bb[2+self.axis] - scroll_bar_size)

    def on_scroll_up(self):
        parent_bb = self.get_parent_bb()
        is_shifting = pygame.key.get_mods() & pygame.KMOD_SHIFT != 0
        can_scroll = (self.axis == 0) == is_shifting
        if can_scroll and self.is_in_relative_bb(self.get_relative_pos(pygame.mouse.get_pos(), bb=parent_bb), bb=parent_bb):
            self.scroll = max(self.scroll - self.mouse_scroll_amount / ((1 - self.ratio) * self.get_total_size()), 0)

    def on_scroll_down(self):
        parent_bb = self.get_parent_bb()
        is_shifting = pygame.key.get_mods() & pygame.KMOD_SHIFT != 0
        can_scroll = (self.axis == 0) == is_shifting
        if can_scroll and self.is_in_relative_bb(self.get_relative_pos(pygame.mouse.get_pos(), bb=parent_bb), bb=parent_bb):
            self.scroll = min(self.scroll + self.mouse_scroll_amount / ((1 - self.ratio) * self.get_total_size()), 1)


__all__ = ["ScrollBarWidget"]
