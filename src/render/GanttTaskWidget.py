import pygame

from render.widget.Widget import Widget
from utils import pygame_utils


class GanttTaskWidget(Widget):

    COLORS = [(0xff0000, 0x880000),
              (0x00ff00, 0x008800),
              (0x0000ff, 0x000088),
              (0xffff00, 0x888800),
              (0x00ffff, 0x008888),
              (0xff00ff, 0x880088),
              ]

    def __init__(self, task, total_time, parent_bb, get_y_offset):
        super().__init__()
        self.task = task
        self.total_time = total_time
        self.parent_bb = parent_bb
        self.get_y_offset = get_y_offset
        # The raw position of the widget before the scrolling is applied
        self.pos = self.parent_bb.x, self.parent_bb.y + (self.task.index-1) * 50
        # The raw size of the widget before the cropping (due to scrolling) is applied
        self.size = self.parent_bb.width, 50
        # The height of the widget that is cropped because of scrolling (only on top)
        self.amount_cropped = 0
        self.colors = self.COLORS[(self.task.index - 1) % len(self.COLORS)]
        self.font = pygame.font.SysFont("Arial", 8)

    def draw(self, surface):
        if self.total_time == 0:
            pygame.draw.rect(surface,
                             self.colors[0],
                             pygame.Rect(0, 3 - self.amount_cropped, self.size[0], self.size[1] - 6))
            surface.blit(self.font.render(self.task.name, True, (0, 0, 0)), (0, 3 - self.amount_cropped))
        else:
            pygame.draw.rect(surface,
                             self.colors[0],
                             pygame.Rect(self.task.earliest_start / self.total_time * self.size[0],
                                         3 - self.amount_cropped,
                                         (self.task.latest_start - self.task.earliest_start + self.task.estimated_time) / self.total_time * self.size[0],
                                         self.size[1] - 6))
            surface.blit(self.font.render(self.task.name, True, (0, 0, 0)),
                         (self.task.earliest_start / self.total_time * self.size[0], 3-self.amount_cropped))
        #pygame.draw.rect(surface,
        #                 self.colors[1],
        #                 pygame.Rect(self.task.earliest_start / self.total_time * self.size[0], 3-self.amount_cropped, (self.task.latest_start-self.task.earliest_start) / self.total_time * self.size[0], self.size[1] - 6))
        #pygame.draw.rect(surface,
        #                 self.colors[1],
        #                 pygame.Rect((self.task.earliest_start + self.task.estimated_time) / self.total_time * self.size[0], 3-self.amount_cropped, (self.task.latest_start - self.task.earliest_start) / self.total_time * self.size[0], self.size[1] - 6))

    def get_bb(self):
        y_offset = self.get_y_offset()
        self.amount_cropped = max(0, self.parent_bb.y - (self.pos[1] - y_offset))
        return pygame_utils.crop_bb_to_fit(pygame.Rect((self.pos[0], self.pos[1] - y_offset), self.size),
                                           self.parent_bb)
