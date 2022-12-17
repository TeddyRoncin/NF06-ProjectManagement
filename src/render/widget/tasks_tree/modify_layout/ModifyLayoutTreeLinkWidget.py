from math import sqrt

import pygame

from render.widget.tasks_tree.TreeLinkWidget import TreeLinkWidget


class ModifyLayoutTreeLinkWidget(TreeLinkWidget):

    def __init__(self,
                 from_position,
                 to_position,
                 from_task,
                 to_task,
                 get_position_offset,
                 get_parent_bb,
                 on_drag,
                 on_drop):
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

    def get_bb(self):
        super().get_bb()
        #if not self.dragging:
        return self.actual_bb
        #self.actual_bb.normalize()
        #print(self.actual_bb)
        #return self.actual_bb

    def get_distance_from_line(self, pos):
        start, end = self.get_positions_coords()
        slope = (start[1] - end[1]) / (start[0] - end[0])
        y_intercept = start[1] - slope * start[0]
        # Compute the distance between the point at coordinates pos
        # and the line defined by the equation y = slope * x + y_intercept
        return abs(pos[1] - slope * pos[0] - y_intercept) / sqrt(slope ** 2 + 1)
