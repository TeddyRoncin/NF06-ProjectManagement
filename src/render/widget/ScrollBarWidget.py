import pygame

from render.widget.Widget import Widget
from utils.mathutils import clamp


class ScrollBarWidget(Widget):

    """
    Represents a scroll bar. A ScrollBarWidget is used to display hidden parts of a Widget
    if it is too big to fit on the screen.
    It is always positioned on the right or the bottom of the parent Widget,
    depending on if it is a horizontal or a vertical ScrollBarWidget.
    In this Widget, when we say size, we mean width or height, depending on the orientation of the ScrollBatWidget

    These are the fields of the class :
    - scroll : A number between 0 and 1 representing the amount scrolled. 0 is the left or top, 1 is the right or bottom
    - get_parent_bb : A function that returns the parent bounding box
    - get_total_size : A function that returns the total size of the parent.
                       It is the size it would like to have on the screen
    - axis : 0 if the ScrollBarWidget is horizontal (X axis), 1 if it is vertical (Y axis)
    - mouse_scroll_amount : The amount of pixels which will be scrolled when the user turns the mouse wheel
    - bb : The bounding box of the ScrollBarWidget.
    - ratio : The ratio between the displayed size and desired size of the parent Widget
    - is_scrolling : If the user is currently dragging the ScrollBarWidget. It is set to True when the user clicks
                     on the ScrollBarWidget, and set back to False when he releases the click
    """

    def __init__(self, get_parent_bb, get_total_size, is_vertical=True, mouse_scroll_amount=3):
        """
        Creates a new ScrollBarWidget
        :param get_parent_bb: A function that returns the bounding box of the parent widget
        :param get_total_size: A function that returns the total width/height of the parent widget
        :param is_vertical: Whether this is a vertical or a horizontal scroll bar
        :param mouse_scroll_amount: How many pixels are scrolled when the mouse wheel is used
        """
        super().__init__()
        self.scroll = 0
        self.get_parent_bb = get_parent_bb
        self.get_total_size = get_total_size
        self.axis = int(is_vertical)
        self.mouse_scroll_amount = mouse_scroll_amount
        self.bb = pygame.Rect(0, 0, 0, 0)
        self.ratio = 0
        # If the user is currently dragging the scroll bar
        self.is_scrolling = False
        self.refresh_values()

    def get_scroll_in_pixel(self):
        """
        Returns the amount that has been scrolled, in pixels.
        This is useful to compute offsets to draw a widget or find which portion of it has been clicked.
        :return: The amount that was scrolled, in pixels
        """
        return (1 - self.ratio) * self.get_total_size() * self.scroll

    def refresh_values(self):
        """
        Refreshes the values of bb and ratio. This should be called each time the parent Widget changes
        his bounding box or his total size. This is also called in the ScrollBarWidget.__init__(...) method
        to initialize the fields.
        :return: None
        """
        if self.axis == 0:
            self.bb = pygame.Rect(self.get_parent_bb().x, self.get_parent_bb().y + self.get_parent_bb().height - 5,
                                  self.get_parent_bb().width, 5)
            self.ratio = 1 if self.get_total_size() == 0 else self.get_parent_bb().width / self.get_total_size()
        else:
            self.bb = pygame.Rect(self.get_parent_bb().x + self.get_parent_bb().width - 5, self.get_parent_bb().y,
                                  5, self.get_parent_bb().height)
            self.ratio = 1 if self.get_total_size() == 0 else self.get_parent_bb().height / self.get_total_size()

    def draw(self, surface):
        """
        Draws the ScrollBarWidget on the surface. It is not drawn if the ratio is greater than 1,
        because that means that the parent Widget have enough space to be displayed entirely
        :param surface: The surface we should draw the ScrollBarWidget to
        :return: None
        """
        self.refresh_values()
        # Draw nothing if no scrollbar is needed
        if self.ratio >= 1:
            return
        surface.fill((125, 125, 125))
        scroll_bar_size = self.bb[2+self.axis] * self.ratio
        if self.axis == 0:
            rect = pygame.Rect((self.bb.width - scroll_bar_size) * self.scroll, 0, scroll_bar_size, self.bb.height)
        else:
            rect = pygame.Rect(0, (self.bb.height - scroll_bar_size) * self.scroll, self.bb.width, scroll_bar_size)
        pygame.draw.rect(surface,
                         pygame.Color(175, 175, 175),
                         rect)

    def on_left_click_bb(self, pos):
        """
        Called when the user performs a left click on the ScrollBarWidget.
        If this happens, then the user is starting to drag the ScrollBarWidget
        :param pos: The position of the click, relative to the bounding box of the ScrollBarWidget.
                    This parameter is not used there
        :return: None
        """
        self.is_scrolling = True

    def on_left_button_release(self):
        """
        Called when the user releases the left click button.
        If this happens, then the user stops dragging the ScrollBarWidget
        :return: None
        """
        self.is_scrolling = False

    def on_mouse_motion(self, pos, motion, buttons):
        """
        When the user moves the mouse. If the ratio is greater than 1, then we can't scroll and do nothing.
        If he was not scrolling, we do nothing either.
        :param pos: The position of the mouse
        :param motion: The change in X and Y coordinates.
                       For example, if the user moved the mouse to the right by 1 pixel, then motion is (1, 0)
        :param buttons: The buttons pressed by the user during the motion
        :return: None
        """
        if self.ratio >= 1 or not self.is_scrolling:
            return
        scroll_bar_size = self.bb[2+self.axis] * self.ratio
        scroll_bar_pos = clamp(pos[self.axis] - (scroll_bar_size / 2), 0, self.bb[2+self.axis] - scroll_bar_size + 1)
        self.scroll = scroll_bar_pos / (self.bb[2+self.axis] - scroll_bar_size)

    def on_scroll_up(self):
        """
        Called when the user scrolls up with his mouse wheel. If the ratio is greater than 1,
        then we can't scroll and do nothing.
        If the scroll bar is horizontal, we only scroll if user presses a shift key.
        If the scroll bar is vertical, we don't scroll if user presses a shift key
        :return: None
        """
        if self.ratio >= 1:
            return
        parent_bb = self.get_parent_bb()
        is_shifting = pygame.key.get_mods() & pygame.KMOD_SHIFT != 0
        can_scroll = (self.axis == 0) == is_shifting
        if can_scroll and self.is_in_relative_bb(self.get_relative_pos(pygame.mouse.get_pos(), bb=parent_bb), bb=parent_bb):
            self.scroll = max(self.scroll - self.mouse_scroll_amount / ((1 - self.ratio) * self.get_total_size()), 0)

    def on_scroll_down(self):
        if self.ratio >= 1:
            return
        parent_bb = self.get_parent_bb()
        is_shifting = pygame.key.get_mods() & pygame.KMOD_SHIFT != 0
        can_scroll = (self.axis == 0) == is_shifting
        if can_scroll and self.is_in_relative_bb(self.get_relative_pos(pygame.mouse.get_pos(), bb=parent_bb), bb=parent_bb):
            self.scroll = min(self.scroll + self.mouse_scroll_amount / ((1 - self.ratio) * self.get_total_size()), 1)


__all__ = ["ScrollBarWidget"]
