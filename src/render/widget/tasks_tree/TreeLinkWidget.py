import pygame

from render.widget.Widget import Widget


class TreeLinkWidget(Widget):

    def __init__(self, from_position, to_position, get_position_offset, get_parent_bb):
        super().__init__()
        self.line_bb = pygame.Rect(from_position,
                                       (to_position[0] - from_position[0], to_position[1] - from_position[1]))
        self.line_bb.normalize()
        self.bb = self.line_bb.inflate(4, 4)
        # Positions are tuple containing 0s or 1s as x and y
        # 0 means left or top, 1 means right or bottom of the bounding box
        self.from_position = (int(from_position[0] > to_position[0]), int(from_position[1] > to_position[1]))
        self.to_position = (int(from_position[0] < to_position[0]), int(from_position[1] < to_position[1]))
        self.actual_bb = self.bb.copy()
        self.get_position_offset = get_position_offset
        self.get_parent_bb = get_parent_bb

    def draw(self, surface):
        self._draw(surface, 0x333333)

    def _draw(self, surface, color):
        start_pos, end_pos = self.get_positions_coords()
        offset = self.compute_drawing_offset()
        pygame.draw.line(surface,
                         color,
                         (start_pos[0] + offset[0], start_pos[1] + offset[1]),
                         (end_pos[0] + offset[0], end_pos[1] + offset[1]),
                         3)

    def get_positions_coords(self):
        return (self.line_bb.width * self.from_position[0], self.line_bb.height * self.from_position[1]), \
               (self.line_bb.width * self.to_position[0], self.line_bb.height * self.to_position[1])

    def compute_drawing_offset(self):
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
        self.actual_bb = self.bb.move(self.get_position_offset())
        parent_bb = self.get_parent_bb()
        self.actual_bb = self.actual_bb.clip(parent_bb)
        return self.actual_bb


