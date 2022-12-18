import pygame

from render.widget.Widget import Widget


class LabelWidget(Widget):

    """
    Represents a simple text on the Screen.

    These are the fields of a LabelWidget :
    - color : The color of the text
    - font : The font used to render the text
    - text_render : The Surface containing the rendered text.
                    We use this field to avoid recreating the Surface at each frame, as this surface is static.
    """

    def __init__(self, pos, text, font_size=16, bold=False, color=(255, 255, 255)):
        """
        Creates a new LabelWidget
        :param pos: The absolute position of the LabelWidget
        :param text: The text displayed on the LabelWidget
        :param font_size: The size of the font used to render the text. By default, its value is 16
        :param bold: Whether the font is bold or not. By default, its value is False
        :param color: The color of the text. By default, its value is white
        """
        super().__init__()
        self.color = color
        self.font = pygame.font.SysFont("Arial", font_size, bold=bold)
        self.text_render = None
        self.bb = pygame.Rect(pos, (0, 0))
        self.set_text(text)

    def draw(self, surface):
        """
        Draws the widget on the given Surface. It should be called at each frame
        :param surface: The Surface on which the widget is drawn
        :return: None
        """
        surface.blit(self.text_render, (0, 0))

    def set_text(self, text):
        """
        Changes the text of the LabelWidget. It updates the text Surface and the bounding box
        :param text: The new text to display
        :return: None
        """
        self.text_render = self.font.render(text, False, self.color)
        self.bb = pygame.Rect(self.bb.topleft, (self.text_render.get_width(), self.text_render.get_height()))
