import pygame

from render.animation.Animation import Animation
from render.animation.AppearEffect import AppearEffect
from render.widget.Widget import Widget
from render.widget.ScrollBarWidget import ScrollBarWidget
from utils import timing_functions


class EntryWidget(Widget):

    """
    An entry Widget that allows the user to enter text. The text can be spread over multiple lines.
    The EntryWidget automatically adapts its size based on its content. When reaching its maximum size,
    a scrollbar is shown (both vertically and horizontally).

    These are the fields of an EntryWidget :
    - font : The font used to render the text
    - font_height : The height of each line
    - min_size : A tuple containing the minimum size of the EntryWidget
    - max_size : A tuple containing the maximum size of the EntryWidget
    - max_chars : The maximum number of characters that can be entered in the EntryWidget.
                  If its value is -1, there is no limit.
    - multiple_lines : A boolean indicating if the EntryWidget can have multiple lines.
    - focus : A boolean indicating if the EntryWidget currently has the focus.
              If it does not, the cursor is not shown and the user cannot enter text.
    - content : A list of strings containing the text in the EntryWidget. Each string is a line.
    - total_size : A tuple containing the total size, in pixels, of the EntryWidget.
                   There are no correlations between this size of the EntryWidget's bounding box.
                   This field is used for the scrolling functionality.
    - horizontal_scroll_bar : The horizontal ScrollBarWidget of the EntryWidget.
    - vertical_scroll_bar : The vertical ScrollBarWidget of the EntryWidget.
    - cursor_position : A list of two integers containing the position of the cursor in the EntryWidget.
                        The first integer is the line index and the second the character index.
    - cursor_surface : The Surface containing the cursor. This Surface is rendered by the cursor_animation field.
                       See the cursor_animation field for more information.
    - cursor_animation : The Animation used to render the cursor. It permits making it appear and disappear smoothly.
                         The only effect is an AppearEffect.
    """

    def __init__(self, pos, min_size, max_size, max_chars, multiple_lines, default_content=""):
        """
        Creates a new EntryWidget
        :param pos: The absolute position of the EntryWidget
        :param min_size: The minimum size of the EntryWidget
        :param max_size: The maximum size of the EntryWidget
        :param max_chars: The maximum number of characters that can be entered in the EntryWidget.
                          If its value is -1, there is no limit
        :param multiple_lines: A boolean indicating if the EntryWidget can have multiple lines
        :param default_content: The default content of the EntryWidget. By default, it is an empty string
        """
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
        """
        This is an internal function. It should not be used outside this class

        Generates the Animation of the cursor_animation field. The only effect it contains is an AppearEffect.
        :return: The generated Animation
        """
        animation_effect = AppearEffect(timing_functions.cursor)
        animation = Animation([animation_effect], 1)
        animation.render_no_update(self.cursor_surface)
        return animation

    def get_children(self):
        """
        Returns the child Widgets of the EntryWidget that should be drawn on the Window.
        :return: A generator returning the child Widgets
        """
        yield self.horizontal_scroll_bar
        yield self.vertical_scroll_bar

    def draw(self, surface):
        """
        Draws the EntryWidget on the given Surface
        :param surface: The Surface on which the EntryWidget should be drawn
        :return: None
        """
        text_surfaces = []
        width = 0
        for text in self.content:
            text_surface = self.font.render(text, True, pygame.Color(0, 0, 0))
            # The first element is the surface and the second is the y coordinate the text should be drawn to
            text_surfaces.append(text_surface)
            width = max(width, text_surface.get_width() + 4)
        self.total_size = (max(self.min_size[0], width), max(self.min_size[1], len(text_surfaces) * self.font_height))
        self.bb.width = min(self.max_size[0], self.total_size[0])
        self.bb.height = min(self.max_size[1], self.total_size[1])
        background_color = pygame.Color(220, 220, 220)
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
        """
        Called when the user left-clicks. If the clicked was performed outside the bounding box of the EntryWidget,
        the focus is lost and the cursor Animation is stopped.
        Otherwise, the focus is gained and the Animation is resumed
        :param pos: The position of the click, relative to the EntryWidget
        :return: None
        """
        gained_focus = self.is_in_relative_bb(pos)
        if not self.focus and gained_focus:
            self.cursor_animation.start()
        elif self.focus and not gained_focus:
            self.cursor_animation.stop()
            self.cursor_animation.render_no_update(self.cursor_surface)
        self.focus = gained_focus

    def on_key_press(self, event):
        """
        Called when the user presses a key. If the EntryWidget has the focus, one of the following action is performed
        depending on the key that was pressed :
        - If the key is the backspace key and there is a character before the cursor, this character is deleted,
          and the cursor is moved to the left.
        - If the key is the delete key and there is a character after the cursor, this character is deleted.
        - If the key is a left or right arrow key, and it is possible to perform this action,
          the cursor is moved in the corresponding direction. If needed, it is sent to the previous or next line.
        - If the key is not any of the above, the unicode value of the key is added to the EntryWidget's content
          if we did not already reach the maximum number of characters
        :param event: The event that was triggered
        :return: None
        """
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
            elif sum(len(line) for line in self.content) < self.max_chars or self.max_chars == -1:
                self.content[self.cursor_position[0]] = \
                    self.content[self.cursor_position[0]][:self.cursor_position[1]] + \
                    event.unicode + \
                    self.content[self.cursor_position[0]][self.cursor_position[1]:]
                self.cursor_position[1] += 1

    def get_content(self):
        """
        Returns the content of the EntryWidget.
        It simply concatenates all the lines of the EntryWidget with a newline character
        :return: The content of the EntryWidget
        """
        return "\n".join(self.content)

    def set_content(self, content):
        """
        Modifies the content of the EntryWidget. The cursor is moved back to the very beginning of the EntryWidget
        :param content: The new content
        :return: None
        """
        self.content = content.split("\n")
        self.cursor_position = [0, 0]
