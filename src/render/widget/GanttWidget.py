import pygame

from render.widget.GanttTaskWidget import GanttTaskWidget
from render.widget.ScrollBarWidget import ScrollBarWidget
from render.widget.Widget import Widget


class GanttWidget(Widget):

    def __init__(self, bb, project):
        super().__init__()
        self.project = project
        self.bb = bb
        self.scroll_bar = ScrollBarWidget(self.get_bb, lambda: project.tasks_count*50 + 50)
        self.y_offset = 0
        self.task_widgets = []
        self.total_time = self.project.project_task.earliest_start + self.project.project_task.estimated_time
        self.generate_widgets(self.project.beginning_task)
        self.number_of_time_marks = (project.tasks_count // 5) % 5 + 5
        self.font = pygame.font.SysFont("Arial", 12)

    def get_children(self):
        yield from self.task_widgets
        yield self.scroll_bar

    def draw(self, surface):
        surface.fill(0xffffff)
        for i in range(self.number_of_time_marks):
            time_mark = self.font.render(str((self.project.project_task.latest_start
                                         + self.project.project_task.estimated_time) * i / self.number_of_time_marks),
                                         False,
                                         0x000000)
            pos = 100 + (self.bb.width - 100) * i / self.number_of_time_marks
            surface.blit(time_mark, (pos - time_mark.get_width() / 2, 3))
            pygame.draw.line(surface, 0x000000, (pos, 20), (pos, self.bb.height))

    def reload(self):
        self.generate_widgets(self.project.beginning_task)

    def generate_widgets(self, first_task):
        self.task_widgets.append(
            GanttTaskWidget(first_task, self.total_time, self.bb, self.scroll_bar.get_scroll_in_pixel))
        while len(first_task.downstream_tasks) == 1:
            first_task = first_task.downstream_tasks[0]
            self.task_widgets.append(
                GanttTaskWidget(first_task, self.total_time, self.bb, self.scroll_bar.get_scroll_in_pixel))
        for task in first_task.downstream_tasks:
            if task.upstream_tasks[0] != first_task:
                continue
            self.generate_widgets(task)

