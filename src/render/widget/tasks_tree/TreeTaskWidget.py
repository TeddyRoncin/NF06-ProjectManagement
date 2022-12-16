import pygame

from render.widget.Widget import Widget


class TreeTaskWidget(Widget):

    def __init__(self, task, position, get_position_offset, get_parent_bb):
        super().__init__()
        self.task = task
        self.bb = pygame.Rect(position[0] - 20, position[1] - 20, 40, 40)
        # Avoid computations repetition in the draw function
        self.actual_bb = self.bb.copy()
        self.get_position_offset = get_position_offset
        self.get_parent_bb = get_parent_bb

    def draw(self, surface):
        self._draw(surface, circle_color=pygame.Color(255, 0, 0))

    def _draw(self, surface, circle_color):
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
        pygame.draw.circle(surface, circle_color, (20 + offset[0], 20 + offset[1]), 20)
        font = pygame.font.SysFont("Arial", 10)
        surface.blit(font.render(self.task.name, False, pygame.Color(0, 255, 0)), (10 + offset[0], 10 + offset[1]))

    def get_bb(self):
        self.actual_bb = self.bb.move(self.get_position_offset())
        parent_bb = self.get_parent_bb()
        self.actual_bb = self.actual_bb.clip(parent_bb)
        return self.actual_bb

