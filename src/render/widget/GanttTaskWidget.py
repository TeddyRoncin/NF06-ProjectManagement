import pygame

from render.widget.Widget import Widget


class GanttTaskWidget(Widget):

    COLORS = [(0xff0000, 0x880000),
              (0x00ff00, 0x008800),
              (0x0000ff, 0x000088),
              (0xffff00, 0x888800),
              (0x00ffff, 0x008888),
              (0xff00ff, 0x880088),
              ]

    def __init__(self, task, is_earliest_graph, total_time, parent_bb, get_y_offset):
        super().__init__()
        self.task = task
        self.is_earliest_graph = is_earliest_graph
        self.total_time = total_time
        self.parent_bb = parent_bb
        self.get_y_offset = get_y_offset
        # The raw position of the widget before the scrolling is applied
        self.pos = self.parent_bb.x, self.parent_bb.y + 20 + (self.task.index-1) * 50
        # The raw size of the widget before the cropping (due to scrolling) is applied
        self.size = self.parent_bb.width, 50
        # The size of the timeline part of the widget.
        # We leave 100 pixels to display the name, and 3 pixels up and down for a small margin between each task
        self.timeline_size = self.size[0] - 100, self.size[1] - 6
        # The height of the widget that is cropped because of scrolling (only on top)
        self.amount_cropped = 0
        self.colors = self.COLORS[(self.task.index - 1) % len(self.COLORS)]
        font = pygame.font.SysFont("Arial", 12)
        self.task_name_render = font.render(self.task.name, True, 0x000000)

    def draw(self, surface):
        surface.blit(self.task_name_render, (0, (50 - self.task_name_render.get_height()) / 2 - self.amount_cropped))
        if self.total_time == 0:
            pygame.draw.rect(surface,
                             self.colors[0],
                             pygame.Rect((100, 3 - self.amount_cropped), self.timeline_size))
        else:
            start = self.task.earliest_start if self.is_earliest_graph else self.task.latest_start
            end = start + self.task.estimated_time
            pygame.draw.rect(surface,
                             self.colors[0],
                             pygame.Rect(100 + start / self.total_time * self.timeline_size[0],
                                         3 - self.amount_cropped,
                                         (end - start
                                          + self.task.estimated_time) / self.total_time * self.timeline_size[0],
                                         self.timeline_size[1]))

    def get_bb(self):
        y_offset = self.get_y_offset()
        self.amount_cropped = max(0, self.parent_bb.y - (self.pos[1] - y_offset))
        return pygame.Rect((self.pos[0], self.pos[1] - y_offset), self.size).clip(self.parent_bb)
