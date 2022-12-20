import pygame

from render.widget.Widget import Widget


class ButtonWidget(Widget):

    """
    Represents a button on the screen. It calls a callback function when the user presses it.
    It is rendered as a rectangle with a text in the middle.

    These are the fields of a ButtonWidget :
    - on_click : A callback function that is called when the user presses the button.
    - text : The text displayed on the button.
    - font : The font used to render the text.
    - font_size : The font size.
    - surface : The surface containing the rendered text.
                We use this field to avoid to recreate it at each frame, as this surface is static.
    """

    def __init__(self, pos, size, text, on_click, font_size=16, bold=False):
        """
        Creates a new ButtonWidget
        :param pos: The absolute position of the ButtonWidget
        :param size: The size of the ButtonWidget
        :param text: The text displayed on the ButtonWidget
        :param on_click: A callback function that is called when the user presses the ButtonWidget
        :param font_size: The size of the font used to render the text. By default, its value is 16
        :param bold: Whether the font is bold or not. By default, its value is False
        """
        super().__init__()
        self.on_click = on_click
        self.bb = pygame.Rect(pos, size)
        self.text = text
        self.font = pygame.font.SysFont("Arial", font_size, bold=bold)
        self.font_size = font_size
        self.surface = self.font.render(text, True, (255, 255, 255))

    def draw(self, surface):
        """
        Draws the widget on the given surface. It should be called at each frame
        :param surface: The surface on which the widget is drawn
        :return: None
        """
        surface.fill(0x555555)
        surface.blit(self.surface,
                     ((self.bb.width - self.surface.get_width()) / 2,
                      (self.bb.height - self.surface.get_height()) / 2))

    def on_left_click_bb(self, pos):
        """
        Called when the user presses the left mouse button in the bounding box of the Widget.
        It simply calls the callback function (self.on_click)
        :param pos: The position of the mouse when the event occurred
        :return: None
        """
        self.on_click()

    def rerender(self, text=None, font_size=None, bold=None):
        """
        Re-renders the text of the ButtonWidget
        This method allows to change the text, the font size or the boldness of the font
        :param text: The new text. If None, the old text is kept. By default, its value is None
        :param font_size: The new font size. If None, the old font size is kept. By default, its value is None
        :param bold: The new boldness of the font. If None, the old boldness is kept. By default, its value is None
        :return: None
        """
        if text is not None:
            self.text = text
        if font_size is None:
            font_size = self.font_size
        if bold is None:
            bold = self.font.get_bold()
        self.font = pygame.font.SysFont("Arial", font_size, bold=bold)
        self.surface = self.font.render(self.text, True, (255, 255, 255))
