import pygame

from render.widget.Widget import Widget


class TreeLinkWidget(Widget):

    """
    This class is a base class, it provides tools to create specialized TreeLinkWidgets.
    It contains general utility features and a default definition of the methods.

    Represents a link between two Tasks in the tree representation of a Project. It is a child Widget of the TreeWidget.
    The link is represented by a line between the two Tasks.

    These are the fields of a TreeLinkWidget :
    - line_bb : The raw bounding box of the line. It differs from the bb field because the bb field is a little bigger
                to be sure the line can be rendered entirely.
                It is used to calculate the positions in pixels of the two Tasks.
                See from_position and to_position for more information.
    - from_position : A tuple containing the x position and the y position of the upstream Task of this link.
                      It can only contain 2 values : 0 or 1.
                      0 means left or top, 1 means right or bottom of the bounding box.
                      To get the actual position in pixels, multiply the width or height of the line_bb by the value.
    - to_position : A tuple containing the x position and the y position of the downstream task of this link.
                    The way it works is the same as for the from_position field.
                    For more information, see from_position.
    - actual_bb : The real bounding box of the link. It is the absolute position at which the link should be drawn.
                  It is recomputed at each frame.
    - get_position_offset : A function that returns how much the parent Widget has been dragged.
    - get_parent_bb : A function that returns the bounding box of the parent Widget.
    """

    def __init__(self, from_position, to_position, get_position_offset, get_parent_bb):
        """
        Creates a new TreeLinkWidget
        :param from_position: The position of the TreeTaskWidget representing the upstream Task of this TreeLinkWidget
        :param to_position: The position of the TreeTaskWidget representing the downstream Task of this TreeLinkWidget
        :param get_position_offset: A function that returns how much the parent Widget has been dragged
        :param get_parent_bb: A function that returns the bounding box of the parent Widget
        """
        super().__init__()
        self.line_bb = pygame.Rect(from_position,
                                   (to_position[0] - from_position[0], to_position[1] - from_position[1]))
        self.line_bb.normalize()
        self.bb = self.line_bb.inflate(4, 4)
        # Positions are tuple containing 0s or 1s as x and y
        # 0 means left or top, 1 means right or bottom of the bounding box
        self.from_position = (int(from_position[0] > to_position[0]), int(from_position[1] > to_position[1]))
        self.to_position = (int(from_position[0] <= to_position[0]), int(from_position[1] <= to_position[1]))
        self.actual_bb = self.bb.copy()
        self.get_position_offset = get_position_offset
        self.get_parent_bb = get_parent_bb

    def draw(self, surface):
        """
        Draws the TreeLinkWidget on the given surface. This function is called at each frame.
        This is the default implementation, it draws a dark grey line
        :param surface: The surface should be a subsurface of the Window at positions contained by self.actual_bb
        :return: None
        """
        self._draw(surface, 0x333333)

    def _draw(self, surface, color):
        """
        Draws the widget on the given surface. It should be called at each frame.
        This is a general implementation, it draws a circle.
        The surface should be a subsurface of the Window at positions contained by self.actual_bb
        :param surface:
        :param color:
        :return:
        """
        start_pos, end_pos = self.get_positions_coords()
        offset = self.compute_drawing_offset()
        pygame.draw.line(surface,
                         color,
                         (start_pos[0] + offset[0], start_pos[1] + offset[1]),
                         (end_pos[0] + offset[0], end_pos[1] + offset[1]),
                         3)

    def get_positions_coords(self):
        """
        Returns the relative coordinates of the two Tasks in pixels
        :return: A tuple containing two pair of coordinates. The first are the coordinates of the upstream Task,
                 and the second those of the downstream Task
        """
        return (self.line_bb.width * self.from_position[0], self.line_bb.height * self.from_position[1]), \
               (self.line_bb.width * self.to_position[0], self.line_bb.height * self.to_position[1])

    def compute_drawing_offset(self):
        """
        Computes the x and y offset we should draw the link at. If the line is not entirely visible
        because it is too high relatively to the parent bounding box, we don't want to draw the line
        from the top corners (which would be the top of the parent Widget), but from higher
        :return: A list containing the x and y offsets
        """
        offset = [0, 0]
        parent_bb = self.get_parent_bb()
        if self.actual_bb.x == parent_bb.x:
            offset[0] = self.actual_bb.width - self.bb.width
        elif self.actual_bb.x == parent_bb.x + parent_bb.width:
            offset[0] = self.bb.width - self.actual_bb.width
        if self.actual_bb.y == parent_bb.y:
            offset[1] = -40 + self.actual_bb.height
        elif self.actual_bb.y == parent_bb.y + parent_bb.height:
            offset[1] = 40 - self.actual_bb.height
        return offset

    def get_bb(self):
        """
        Returns the bounding box of this TreeLinkWidget. It actualises the actual_bb field, and then returns it
        :return: The bounding box of this TreeLinkWidget
        """
        self.actual_bb = self.bb.move(self.get_position_offset())
        parent_bb = self.get_parent_bb()
        self.actual_bb = self.actual_bb.clip(parent_bb)
        return self.actual_bb
