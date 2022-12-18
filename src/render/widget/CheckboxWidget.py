import pygame.font

from render.widget.Widget import Widget


class CheckboxWidget(Widget):

    """
    A Widget that represents a checkbox on the Window. It can be clicked switch it on or off.
    A CheckboxWidget is rendered as a square (black if disabled, grey if not checked, green otherwise)
    with a text on the right of it.

    These are the fields of a CheckboxWidget :
    - font : The font used to render the text.
    - on_value_changed : The callback function called when the CheckboxWidget is enabled or disabled.
                         It takes a boolean as parameter, which is True if the checkbox is now checked, False otherwise.
    - label_surface : The Surface containing the rendered text.
                      This field is used to avoid to recreate the Surface at each frame.
    - enabled : Whether the CheckboxWidget is enabled or not. If the CheckboxWidget is disabled, it cannot be clicked.
    - activated : Whether the CheckboxWidget is checked or not.
    """

    def __init__(self, pos, label, on_value_changed=None):
        """
        Creates a new CheckboxWidget
        :param pos: The absolute position of the CheckboxWidget
        :param label: The text displayed next to the checkbox
        :param on_value_changed: The callback function called when the CheckboxWidget is enabled or disabled.
                                 It takes a boolean as parameter, which is True if the checkbox is checked,
                                 False otherwise.
                                 It may not be specified. If it is not, no callback will be done
        """
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 20)
        self.on_value_changed = on_value_changed
        label = label.split("\n")
        text_renders = [self.font.render(line, False, (0, 0, 0)) for line in label]
        width = max(text_renders, key=lambda text_render: text_render.get_width()).get_width()
        self.label_surface = pygame.Surface((width, len(label) * (self.font.get_height() + 4) - 4))
        # Make the background transparent
        self.label_surface.fill((255, 255, 255))
        self.label_surface.set_colorkey((255, 255, 255))
        for i, render in enumerate(text_renders):
            self.label_surface.blit(render, (0, (self.font.get_height() + 4) * i))
        self.bb = pygame.Rect(pos, (self.label_surface.get_width() + 20, max(self.label_surface.get_height() + 4, 15)))
        self.enabled = True
        self.activated = False

    def draw(self, surface):
        """
        Draws the CheckboxWidget on the given surface. It should be called at each frame
        :param surface: The Surface on which the CheckboxWidget is drawn
        :return: None
        """
        color = (0, 255, 0)
        if not self.enabled and not self.activated:
            color = (50, 50, 50)
        elif not self.enabled and self.activated:
            color = (50, 150, 50)
        elif self.enabled and not self.activated:
            color = (0, 0, 0)
        pygame.draw.rect(surface, color, pygame.Rect(0, (self.bb.height - 15) / 2, 15, 15))
        surface.blit(self.label_surface, (20, (self.bb.height - self.label_surface.get_height()) / 2))

    def on_left_click_bb(self, pos):
        """
        Called when the CheckboxWidget is clicked. It switches the CheckboxWidget on or off if it is enabled,
        and calls the callback function (self.on_value_changed).
        :param pos: The position of the click (relative to the CheckboxWidget)
        :return: None
        """
        if self.enabled:
            self.activated = not self.activated
            if self.on_value_changed:
                self.on_value_changed(self.activated)
