import pygame

from render.widget.Widget import Widget


class GanttTaskWidget(Widget):

    """
    Represents a single Task in the GanttWidget.
    It is a rectangle that is spread over the whole time the task is being worked on.

    These are the fields of the class :
    - COLORS : The colors used to represent the tasks.

    These are the fields of a GanttTaskWidget :
    - task : The Task that is represented by this Widget.
    - is_earliest_graph : Whether the time represented is the earliest or the latest possible.
    - total_time : The total time (in day) of the Project.
    - parent_bb : The bounding box of the parent Widget.
                  This is used while rendering to crop the bounding box of this Widget.
    - get_y_offset : A function that returns the number of pixels scrolled.
    - pos : The raw position of the Widget before the scrolling is applied.
    - size : The raw size of the Widget before the cropping (due to scrolling) is applied.
    - timeline_size : The size of the timeline part (the part with the rectangle) of the Widget.
    - amount_cropped : The height of the Widget that is cropped upwards because of scrolling.
    - color : The color of the rectangle. Different tasks have different colors to be able to distinguish them well.
    - task_name_render : The rendered name of the task. We compute it before rendering to avoid doing it every frame.
    """

    COLORS = [0xff0000,
              0x00ff00,
              0x0000ff,
              0xffff00,
              0x00ffff,
              0xff00ff,
              ]

    def __init__(self, task, is_earliest_graph, total_time, parent_bb, get_y_offset):
        """
        Creates a new GanttTaskWidget
        :param task: The Task that is represented by this Widget
        :param is_earliest_graph: Whether the time represented is the earliest or the latest possible
        :param total_time: The total time (in day) of the Project
        :param parent_bb: The bounding box of the parent Widget.
        :param get_y_offset: A function that returns the number of pixels scrolled
        """
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
        self.color = self.COLORS[(self.task.index - 1) % len(self.COLORS)]
        font = pygame.font.SysFont("Arial", 12)
        self.task_name_render = font.render(self.task.name, True, 0x000000)

    def draw(self, surface):
        """
        Draws the Widget on the given Surface
        :param surface: The Surface on which to draw the Widget
        :return: None
        """
        surface.blit(self.task_name_render, (0, (50 - self.task_name_render.get_height()) / 2 - self.amount_cropped))
        if self.total_time == 0:
            pygame.draw.rect(surface,
                             self.color,
                             pygame.Rect((100, 3 - self.amount_cropped), self.timeline_size))
        else:
            start = self.task.earliest_start if self.is_earliest_graph else self.task.latest_start
            end = start + self.task.estimated_time
            pygame.draw.rect(surface,
                             self.color,
                             pygame.Rect(100 + start / self.total_time * self.timeline_size[0],
                                         3 - self.amount_cropped,
                                         (end - start
                                          + self.task.estimated_time) / self.total_time * self.timeline_size[0],
                                         self.timeline_size[1]))

    def get_bb(self):
        """
        Returns the real bounding box of the Widget. It refreshes the value of self.amount_cropped
        :return: The real bounding box of the Widget
        """
        y_offset = self.get_y_offset()
        self.amount_cropped = max(0, self.parent_bb.y - (self.pos[1] - y_offset))
        return pygame.Rect((self.pos[0], self.pos[1] - y_offset), self.size).clip(self.parent_bb)
