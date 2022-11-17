import pygame.draw

from render.widget.GanttLinkWidget import GanttLinkWidget
from render.widget.GanttTaskWidget import GanttTaskWidget
from render.widget.Widget import Widget


class GanttWidget(Widget):

    def __init__(self, position, first_task):
        super().__init__()
        self.first_task = first_task
        self.position = position
        self.bb = pygame.Rect(position[0], position[1], 500, 500)
        self.size = self.first_task.downstream_tasks_count * 20, 20 * (self.first_task.max_downstream_tasks_depth - 1) + 40 * self.first_task.max_downstream_tasks_depth
        self.task_widgets = []
        self.link_widgets = []
        self.generate_widgets(self.first_task, 20, self.size[1] / 2)
        self.position_offset = (0, 0)

    def generate_widgets(self, start, x, y):
        self.task_widgets.append(GanttTaskWidget(start, (x+self.bb.x, y+self.bb.y), lambda: self.position_offset, self.get_bb))
        while len(start.downstream_tasks):
            last_x = x
            last_y = y
            x += 60
            if len(start.downstream_tasks) != 1:
                y -= (20 * (start.max_downstream_tasks_depth - 1) + 40 * start.max_downstream_tasks_depth) / 2
                for downstream_task in start.downstream_tasks:
                    y_increase = (20 * (downstream_task.max_downstream_tasks_depth - 1) + 40 * downstream_task.max_downstream_tasks_depth) / 2
                    y += y_increase
                    self.link_widgets.append(GanttLinkWidget((last_x+self.bb.x, last_y+self.bb.y), (x+self.bb.x, y+self.bb.y), lambda: self.position_offset, self.get_bb))
                    self.generate_widgets(downstream_task, x, y)
                    y += y_increase + 20
                return
            new_start = start.downstream_tasks[0]
            if new_start.upstream_tasks[0] != start:
                widget = [widget for widget in self.task_widgets if widget.task == new_start][0]
                self.link_widgets.append(GanttLinkWidget((last_x+self.bb.x, last_y+self.bb.y), (widget.bb.x+widget.bb.width/2, widget.bb.y+widget.bb.height/2), lambda: self.position_offset, self.get_bb))
                return
            if len(new_start.upstream_tasks) != 1:
                new_start_height = 20 * (new_start.max_upstream_tasks_depth - 1) + 40 * new_start.max_upstream_tasks_depth
                start_height = 20 * (start.max_upstream_tasks_depth - 1) + 40 * start.max_upstream_tasks_depth
                y += new_start_height/2 - start_height/2
            start = new_start
            self.link_widgets.append(GanttLinkWidget((last_x+self.bb.x, last_y+self.bb.y), (x+self.bb.x, y+self.bb.y), lambda: self.position_offset, self.get_bb))
            self.task_widgets.append(GanttTaskWidget(start, (x+self.bb.x, y+self.bb.y), lambda: self.position_offset, self.get_bb))

    def get_children(self):
        yield from self.link_widgets
        yield from self.task_widgets

    def draw(self, surface):
        surface.fill((120, 120, 120))

    def on_mouse_motion_bb(self, pos, motion, buttons):
        if buttons[pygame.BUTTON_LEFT-1] == 1:
            self.position_offset = (self.position_offset[0] + motion[0], self.position_offset[1] + motion[1])
            for child in self.get_children():
                child.update_position_offset(self.position_offset)

