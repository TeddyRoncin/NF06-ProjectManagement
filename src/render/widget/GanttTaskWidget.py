import pygame

from render.widget.Widget import Widget
from utils.pygame_utils import crop_bb_to_fit


class GanttTaskWidget(Widget):

    def __init__(self, task, position, get_position_offset, get_parent_bb):
        super().__init__()
        self.task = task
        self.base_bb = pygame.Rect(position[0] - 20, position[1] - 20, 40, 40)
        self.bb = self.base_bb.copy()
        # Avoid computations repetition in the draw function
        self.actual_bb = self.bb.copy()
        self.get_position_offset = get_position_offset
        self.get_parent_bb = get_parent_bb

    def draw(self, surface):
        offset = [0, 0]
        parent_bb = self.get_parent_bb()
        if self.actual_bb.x == parent_bb.x:
            offset[0] = -40 + self.actual_bb.width
        elif self.actual_bb.x == parent_bb.x + parent_bb.width:
            offset[0] = 40 - self.actual_bb.width
        if self.actual_bb.y == parent_bb.y:
            offset[1] = -40 + self.actual_bb.height
        elif self.actual_bb.y == parent_bb.y + parent_bb.height:
            offset[1] = 40 - self.actual_bb.height
        pygame.draw.circle(surface, pygame.Color(255, 0, 0), (20 + offset[0], 20 + offset[1]), 20)
        font = pygame.font.SysFont("Arial", 10)
        surface.blit(font.render(self.task.name, False, pygame.Color(0, 255, 0)), (10+offset[0], 10+offset[1]))

    def get_bb(self):
        self.actual_bb = self.base_bb.move(self.get_position_offset())
        parent_bb = self.get_parent_bb()
        crop_bb_to_fit(self.actual_bb, parent_bb)
        return self.actual_bb

    def update_position_offset(self, offset):
        self.bb = pygame.Rect(self.base_bb.x + offset[0], self.base_bb.y + offset[1], *self.base_bb.size)
