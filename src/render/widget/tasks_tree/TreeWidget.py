import pygame.draw

from render.widget.tasks_tree.TreeLinkWidget import TreeLinkWidget
from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget
from render.widget.Widget import Widget


class TreeWidget(Widget):

    def __init__(self, position, size, project):
        super().__init__()
        self.project = project
        self.first_task = project.beginning_task
        self.position = position
        self.bb = pygame.Rect(position, size)
        self.size = 0, 0
        self.task_widgets = []
        self.link_widgets = []
        self.reload()
        self.position_offset = (0, 0)

    def reload(self):
        self.size = (self.first_task.downstream_tasks_count * 20,
                     20 * (self.first_task.max_downstream_tasks_depth - 1) +
                     40 * self.first_task.max_downstream_tasks_depth)
        self.task_widgets.clear()
        self.link_widgets.clear()
        self.generate_widgets(self.first_task, 20, self.size[1] / 2)

    def generate_widgets(self, start, x, y, length_differences_with_others=()):
        self.task_widgets.append(self.generate_tree_task_widget(start,
                                                                (x + self.bb.x, y + self.bb.y),
                                                                lambda: self.position_offset,
                                                                self.get_bb))
        while len(start.downstream_tasks):
            last_x = x
            last_y = y
            x += 60
            if len(start.downstream_tasks) != 1:
                y -= (20 * (start.max_downstream_tasks_depth - 1) + 40 * start.max_downstream_tasks_depth) / 2
                for downstream_task in start.downstream_tasks:
                    y_increase = (20 * (downstream_task.max_downstream_tasks_depth - 1) +
                                  40 * downstream_task.max_downstream_tasks_depth) / 2
                    y += y_increase
                    self.link_widgets.append(self.generate_tree_link_widget((last_x + self.bb.x, last_y + self.bb.y),
                                                                            (x + self.bb.x, y + self.bb.y),
                                                                            lambda: self.position_offset,
                                                                            self.get_bb,
                                                                            start,
                                                                            downstream_task))
                    self.generate_widgets(downstream_task,
                                          x,
                                          y,
                                          length_differences_with_others=(
                                              *length_differences_with_others,
                                              start.downstream_tasks_count - 1 - downstream_task.downstream_tasks_count)
                                          )
                    y += y_increase + 20
                return
            new_start = start.downstream_tasks[0]
            if new_start.upstream_tasks[0] != start:
                widget = [widget for widget in self.task_widgets if widget.task == new_start][0]
                self.link_widgets.append(self.generate_tree_link_widget((last_x + self.bb.x, last_y + self.bb.y),
                                                                        (
                                                                            widget.bb.x + widget.bb.width / 2,
                                                                            widget.bb.y + widget.bb.height / 2
                                                                        ),
                                                                        lambda: self.position_offset, self.get_bb,
                                                                        start,
                                                                        new_start))
                return
            if len(new_start.upstream_tasks) != 1:
                x += length_differences_with_others[-1] * 60
                new_start_height = 20 * (new_start.max_upstream_tasks_depth - 1) + \
                                   40 * new_start.max_upstream_tasks_depth
                start_height = 20 * (start.max_upstream_tasks_depth - 1) + 40 * start.max_upstream_tasks_depth
                y += new_start_height/2 - start_height/2
                length_differences_with_others = length_differences_with_others[:-1]
            self.link_widgets.append(self.generate_tree_link_widget((last_x + self.bb.x, last_y + self.bb.y),
                                                                    (x + self.bb.x, y + self.bb.y),
                                                                    lambda: self.position_offset, self.get_bb,
                                                                    start,
                                                                    new_start))
            self.task_widgets.append(self.generate_tree_task_widget(new_start,
                                                                    (x + self.bb.x, y + self.bb.y),
                                                                    lambda: self.position_offset,
                                                                    self.get_bb))
            start = new_start

    def get_children(self):
        yield from self.get_movable_children()

    def get_movable_children(self):
        yield from self.link_widgets
        yield from self.task_widgets

    def draw(self, surface):
        surface.fill((120, 120, 120))

    def on_mouse_motion_bb(self, pos, motion, buttons):
        if buttons[pygame.BUTTON_LEFT-1] == 1:
            self.position_offset = (self.position_offset[0] + motion[0], self.position_offset[1] + motion[1])
            #for child in self.get_movable_children():
            #    child.update_position_offset(self.position_offset)

    def generate_tree_task_widget(self, task, pos, position_offset, get_bb):
        return TreeTaskWidget(task, pos, position_offset, get_bb)

    def generate_tree_link_widget(self, start, end, get_position_offset, get_bb, start_widget, end_widget):
        return TreeLinkWidget(start, end, get_position_offset, get_bb)

