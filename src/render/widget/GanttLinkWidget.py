import pygame

from render.widget.Widget import Widget
from utils.pygame_utils import crop_bb_to_fit


class GanttLinkWidget(Widget):

    def __init__(self, from_position, to_position, get_position_offset, get_parent_bb):
        super().__init__()
        self.base_bb = pygame.Rect(from_position, (to_position[0] - from_position[0], to_position[1] - from_position[1]))
        if from_position[1] <= to_position[1]:
            self.from_position = (0, 0)
            self.to_position = (self.base_bb.width, self.base_bb.height)
        else:
            self.base_bb.y += self.base_bb.height
            self.base_bb.height = -self.base_bb.height
            self.from_position = (0, self.base_bb.height)
            self.to_position = (self.base_bb.width, 0)
        self.base_bb.width += 3
        self.base_bb.height += 3
        self.actual_bb = self.base_bb.copy()
        self.get_position_offset = get_position_offset
        self.get_parent_bb = get_parent_bb

    def draw(self, surface):
        offset = [0, 0]
        parent_bb = self.get_parent_bb()
        if self.actual_bb.x == parent_bb.x:
            offset[0] = self.actual_bb.width - self.base_bb.width
        elif self.actual_bb.x == parent_bb.x + parent_bb.width:
            offset[0] = self.base_bb.width - self.actual_bb.width
        if self.actual_bb.y == parent_bb.y:
            offset[1] = -40 + self.actual_bb.height
        elif self.actual_bb.y == parent_bb.y + parent_bb.height:
            offset[1] = 40 - self.actual_bb.height
        pygame.draw.line(surface, (0, 0, 255), (self.from_position[0] + offset[0], self.from_position[1] + offset[1]), (self.to_position[0] + offset[0], self.to_position[1] + offset[1]), 3)

    def get_bb(self):
        self.actual_bb = self.base_bb.move(self.get_position_offset())
        parent_bb = self.get_parent_bb()
        crop_bb_to_fit(self.actual_bb, parent_bb)
        return self.actual_bb

    def update_position_offset(self, offset):
        self.bb = pygame.Rect(self.base_bb.x + offset[0], self.base_bb.y + offset[1], *self.base_bb.size)
