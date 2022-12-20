import pygame

from render.widget.Widget import Widget


class TreeTaskWidget(Widget):

    """
    This class is a base class, it provides tools to create specialized TreeTaskWidgets.
    It contains general utility features and a default definition of the methods.

    Represents a Task in the tree representation of the project. It is a child Widget of the TreeWidget.

    These are the fields of a TreeTaskWidget :
    - task : The Task it represents.
    - actual_bb : The actual bounding box of the widget, taking into account the zoom (not implemented yet),
                  the position offset, and the parent bounding box. This value is updated at each frame.
                  It is mostly used to avoid doing too many computations when it is not needed.
    - get_position_offset : A function that returns the amount the parent Widget was dragged by the user.
    - get_parent_bb : A function that returns the bounding box of the parent Widget.
    - get_scale : A function that returns the scale factor and the scale center of the parent Widget, in a tuple.
    """

    def __init__(self, task, position, get_position_offset, get_parent_bb, get_scale):
        """
        Creates a new TreeTaskWidget
        :param task: The Task it represents
        :param position: The absolute position of the Widget
        :param get_position_offset: A function that returns the amount the parent Widget was dragged by the user
        :param get_parent_bb: A function that returns the bounding box of the parent Widget
        :param get_scale: A function that returns the scale factor and the scale center of the parent Widget, in a tuple
        """
        super().__init__()
        self.task = task
        self.bb = pygame.Rect(position[0] - 50, position[1] - 50, 100, 100)
        # Avoid computations repetition in the draw function
        self.actual_bb = self.bb.copy()
        self.get_position_offset = get_position_offset
        self.get_parent_bb = get_parent_bb
        self.get_scale = get_scale

    def draw(self, surface):
        """
        Draws the widget on the given surface. It should be called at each frame.
        This is the default implementation, it draws a white circle.
        The surface should be a subsurface of the Window at positions contained by self.actual_bb
        :param surface: The surface to draw on
        :return: None
        """
        self._draw(surface, circle_color=0xffffff)

    def _draw(self, surface, circle_color):
        """
        Draws the widget on the given surface. It should be called at each frame.
        This is a general implementation, it draws a circle.
        The surface should be a subsurface of the Window at positions contained by self.actual_bb
        :param surface: The surface to draw on
        :param circle_color: The color of the circle
        :return: None
        """
        offset = [0, 0]
        parent_bb = self.get_parent_bb()
        # radius = self.get_scale()[0] * 20
        radius = 50
        if self.actual_bb.x == parent_bb.x:
            offset[0] = -radius*2 + self.actual_bb.width
        elif self.actual_bb.x == parent_bb.x + parent_bb.width:
            offset[0] = radius*2 - self.actual_bb.width
        if self.actual_bb.y == parent_bb.y:
            offset[1] = -radius*2 + self.actual_bb.height
        elif self.actual_bb.y == parent_bb.y + parent_bb.height:
            offset[1] = radius*2 - self.actual_bb.height
        pygame.draw.circle(surface, circle_color, (radius + offset[0], radius + offset[1]), radius)
        font = pygame.font.SysFont("Arial", 16)
        name_surface = font.render(self.task.name, False, pygame.Color(0, 0, 0))
        surface.blit(name_surface, (radius - name_surface.get_width()/2 + offset[0],
                                    radius - name_surface.get_height()/2 + offset[1]))

    def get_bb(self):
        """
        Returns the bounding box of the widget, in absolute coordinates.
        It computes the actualized value of self.actual_bb and returns it
        :return: The Rect the widget should be drawn at, in absolute coordinates
        """
        # TODO : implement zooming
        # scale_factor, scale_center = self.get_scale()
        self.actual_bb = self.bb.copy()
        # self.actual_bb.width = self.actual_bb.height = scale_factor * 40
        position_offset = self.get_position_offset()
        parent_bb = self.get_parent_bb()
        # self.actual_bb.centerx = (self.actual_bb.centerx - scale_center[0]) * scale_factor + parent_bb.centerx
        # self.actual_bb.centery = (self.actual_bb.centery - scale_center[1]) * scale_factor + parent_bb.centery
        self.actual_bb = self.actual_bb.move(position_offset)
        self.actual_bb = self.actual_bb.clip(parent_bb)
        return self.actual_bb

