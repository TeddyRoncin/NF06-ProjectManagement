from math import sqrt

import pygame

from render.widget.Widget import Widget

class GanttLinkWidget(Widget):

    def __init__(self, from_position, to_position):
        super().__init__()
        print("CREATION !!")
        print(from_position, to_position)
        # We inverse the sign because the y-axis goes down
        slope = (to_position[1] - from_position[1]) / (to_position[0] - from_position[0])
        delta_x = sqrt(20**2 / (slope**2 + 1))
        delta_y = slope * delta_x
        from_position = (from_position[0] + delta_x, from_position[1] + delta_y)
        to_position = (to_position[0] - delta_x, to_position[1] - delta_y)
        print(slope, delta_x, delta_y, from_position, to_position)
        self.bb = pygame.Rect((from_position[0] - 3/2, from_position[1] - 3/2), (to_position[0] - from_position[0], to_position[1] - from_position[1]))
        print(self.bb)
        if from_position[1] <= to_position[1]:
            self.from_position = (3/2, 3/2)
            self.to_position = (self.bb.width-3/2, self.bb.height-3/2)
        else:
            self.bb.y += self.bb.height
            self.bb.height = -self.bb.height
            self.from_position = (3/2, self.bb.height-3/2)
            self.to_position = (self.bb.width-3/2, 3/2)
        self.bb.width += 3
        self.bb.height += 3
        print(self.from_position, self.to_position, self.bb)

    def draw(self, surface):
        pygame.draw.line(surface, (0, 0, 255), self.from_position, self.to_position, 3)
