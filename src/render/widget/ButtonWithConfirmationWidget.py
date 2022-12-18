import time

from render.widget.ButtonWidget import ButtonWidget


class ButtonWithConfirmationWidget(ButtonWidget):

    """
    This is an extension of the classic ButtonWidget. When the user presses it, it displays a confirmation message.
    This may be useful when the ButtonWidget controls an undoable action, for example.

    These are the fields of a ButtonWithConfirmationWidget :
    - last_click : The timestamp of the last click on the ButtonWithConfirmationWidget.
                   This is used to know if user clicked twice on the ButtonWithConfirmationWidget twice
                   in a time interval of 3 seconds.
    - confirmation_surface : The Surface containing the rendered confirmation message.
                             This is useful to avoid drawing it multiple times as it is static.
    """

    def __init__(self, pos, size, text, on_click, font_size=16, bold=False):
        """
        Creates a new ButtonWithConfirmationWidget
        :param pos: The absolute position of the ButtonWithConfirmationWidget
        :param size: The size of the ButtonWithConfirmationWidget
        :param text: The text displayed on the ButtonWithConfirmationWidget.
                     Note that this text will be changed if user clicked on the ButtonWithConfirmationWidget
                     in the last 3 seconds
        :param on_click: A callback function that is called when the user presses the ButtonWithConfirmationWidget
        :param font_size: The size of the font used to render the text. By default, its value is 16
        :param bold: Whether the font is bold or not. By default, its value is False
        """
        super().__init__(pos, size, text, on_click, font_size, bold)
        self.last_click = 0
        self.confirmation_surface = self.font.render("Confirmer ?", True, (0, 0, 0))

    def draw(self, surface):
        """
        Draws the widget on the given surface. It should be called at each frame.
        If the user clicked on the ButtonWithConfirmationWidget in the last 3 seconds,
        it displays the confirmation message (self.confirmation_surface). If not, it displays the text normally
        :param surface: The Surface on which the widget is drawn
        :return: None
        """
        if time.time() - self.last_click < 3:
            surface.fill((255, 0, 0))
            surface.blit(self.confirmation_surface,
                         ((self.bb.width - self.surface.get_width()) / 2,
                          (self.bb.height - self.surface.get_height()) / 2))
        else:
            super().draw(surface)

    def on_left_click_bb(self, pos):
        """
        Called when the user presses the left mouse button in the bounding box of the Widget.
        If the user clicked on the ButtonWithConfirmationWidget in the last 3 seconds,
        it calls the callback function (self.on_click).
        If not, it simply remembers the current timestamp. The rendered surface will then be changed to be
        self.confirmation_surface on the next frame
        :param pos: The relative position of the mouse when the event occurred
        :return: None
        """
        current_time = time.time()
        if current_time - self.last_click < 3:
            self.on_click()
            self.last_click = 0
        else:
            self.last_click = current_time
