from math import sqrt

import pygame

from render.widget.tasks_tree.TreeLinkWidget import TreeLinkWidget


class ModifyLayoutTreeLinkWidget(TreeLinkWidget):

    """
    This represents a link between two Tasks in a ModifyLayoutTreeWidget.
    The downstream part of the ModifyLayoutTreeLinkWidget can be dragged to change the layout of the Project.

    These are tbe fields of a ModifyLayoutTreeLinkWidget :
    - from_task : The Task from which the link starts.
    - to_task : The Task to which the link ends.
    - on_drag : A callback function that is called when the user starts dragging the ModifyLayoutTreeLinkWidget.
                If a ModifyLayoutTreeLinkWidget is already being dragged, this function returns False,
                and the dragging of this ModifyLayoutTreeLinkWidget is not started.
    - on_drop : A callback function that is called when the user releases the ModifyLayoutTreeLinkWidget.
                It takes 4 arguments : the starting Task, the ending Task,
                the x and the y position the ModifyLayoutTreeLinkWidget was dropped.
    - original_from : The original position of the starting Task (in the same format as from_position).
    - original_to : The original position of the ending Task (in the same format as to_position).
    - original_bb : The original bounding box of the ModifyLayoutTreeLinkWidget.
    - dragging : A boolean that is True if this ModifyLayoutTreeLinkWidget is being dragged.
    - motion : How many pixels were dragged since the start of the dragging.
    """

    def __init__(self,
                 from_position,
                 to_position,
                 from_task,
                 to_task,
                 get_position_offset,
                 get_parent_bb,
                 on_drag,
                 on_drop):
        """
        Creates a new ModifyLayoutTreeLinkWidget
        :param from_position: The absolute position of the start
        :param to_position: The absolute position of the end
        :param from_task: The Task from which the ModifyLayoutTreeLinkWidget starts
        :param to_task: The Task to which the ModifyLayoutTreeLinkWidget ends
        :param get_position_offset: A function that returns how much the parent Widget was dragged
        :param get_parent_bb: A function that returns the bounding box of the parent Widget
        :param on_drag: A callback function that is called when the user starts dragging the ModifyLayoutTreeLinkWidget.
                        It should return True if the dragging can start, and False otherwise
        :param on_drop: A callback function that is called when the user releases the ModifyLayoutTreeLinkWidget.
                        It takes 4 arguments : the starting Task, the ending Task,
                        the x and the y position the ModifyLayoutTreeLinkWidget was dropped
        """
        super().__init__(from_position, to_position, get_position_offset, get_parent_bb)
        self.from_task = from_task
        self.to_task = to_task
        self.on_drag = on_drag
        self.on_drop = on_drop
        self.original_from = self.from_position
        self.original_to = self.to_position
        self.original_bb = self.line_bb.copy()
        self.dragging = False
        self.motion = (0, 0)

    def on_left_click_bb(self, pos):
        """
        Called when the user clicks on the bounding box of the ModifyLayoutTreeLinkWidget.
        It starts the dragging if user really clicked on the line and self.on_drag returns True
        :param pos:
        :return:
        """
        if self.get_distance_from_line(pos) <= 5:
            # If we are already dragging something else, we cannot drag this
            if not self.on_drag():
                return
            relative_start, relative_end = self.get_positions_coords()
            start = relative_start[0] + self.bb.x, relative_start[1] + self.bb.y
            end = relative_end[0] + self.bb.x, relative_end[1] + self.bb.y
            pos_abs = pos[0] + self.bb.x, pos[1] + self.bb.y
            self.line_bb = pygame.Rect(start, (pos_abs[0] - start[0], pos_abs[1] - start[1]))
            self.from_position = self.from_position = (int(self.line_bb.width < 0), int(self.line_bb.height < 0))
            self.to_position = (int(self.line_bb.width > 0), int(self.line_bb.height > 0))
            self.line_bb.normalize()
            self.bb = self.line_bb.inflate(2, 2)
            self.motion = (pos_abs[0] - end[0], pos_abs[1] - end[1])
            self.dragging = True

    def on_left_button_release(self):
        """
        Called when the user releases the left button.
        It stops the dragging and calls the self.on_drop callback function
        :return: None
        """
        if self.dragging:
            _, end = self.get_positions_coords()
            self.on_drop(self.from_task, self.to_task, end[0] + self.actual_bb.x, end[1] + self.actual_bb.y)
            self.dragging = False
            self.line_bb = self.original_bb.copy()
            self.bb = self.line_bb.inflate(2, 2)
            self.from_position = self.original_from
            self.to_position = self.original_to
            self.motion = (0, 0)

    def on_mouse_motion(self, pos, motion, buttons):
        """
        Called when the user moves the mouse. If the ModifyLayoutTreeLinkWidget is being dragged, it moves it
        :param pos: The relative position of the mouse
        :param motion: The amount the mouse moved since the last call
        :param buttons: The buttons that are currently pressed. Each button can be accessed with
                        buttons[pygame.BUTTON_{LEFT/RIGHT/MIDDLE}-1]. If the value is 1, the button is pressed,
                        but it is not if the value is 0
        :return: None
        """
        if not self.dragging:
            return
        self.motion = (self.motion[0] + motion[0], self.motion[1] + motion[1])
        self.line_bb = self.original_bb.copy()
        if self.original_from[0] < self.original_to[0]:
            self.line_bb.width += self.motion[0]
        else:
            self.line_bb.x += self.motion[0]
            self.line_bb.width -= self.motion[0]
        if self.original_from[1] < self.original_to[1]:
            self.line_bb.height += self.motion[1]
        else:
            self.line_bb.y += self.motion[1]
            self.line_bb.height -= self.motion[1]
        self.from_position = self.original_from
        self.to_position = self.original_to
        if self.line_bb.width < 0:
            self.from_position, self.to_position = (self.to_position[0], self.from_position[1]), \
                                                   (self.from_position[0], self.to_position[1])
        if self.line_bb.height < 0:
            self.from_position, self.to_position = (self.from_position[0], self.to_position[1]), \
                                                   (self.to_position[0], self.from_position[1])
        self.line_bb.normalize()
        self.bb = self.line_bb.inflate(2, 2)

    def get_distance_from_line(self, pos):
        """
        Returns the distance between the given position and the line. The coordinates are relative to the bounding box
        :param pos: The relative position
        :return: The distance between the given position and the line
        """
        start, end = self.get_positions_coords()
        slope = (start[1] - end[1]) / (start[0] - end[0])
        y_intercept = start[1] - slope * start[0]
        # Compute the distance between the point at coordinates pos
        # and the line defined by the equation y = slope * x + y_intercept
        return abs(pos[1] - slope * pos[0] - y_intercept) / sqrt(slope ** 2 + 1)
