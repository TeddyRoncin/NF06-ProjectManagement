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
        print(self.size)
        print(self.first_task.max_downstream_tasks_depth)
        self.task_widgets = []
        self.link_widgets = []
        self.generate_widgets(self.first_task, 20, self.size[1] / 2)

    def generate_widgets(self, start, x, y):
        self.task_widgets.append(GanttTaskWidget(start, (x+self.bb.x, y+self.bb.y)))
        while len(start.downstream_tasks):
            last_x = x
            last_y = y
            x += 60
            if len(start.downstream_tasks) != 1:
                y -= (20 * (start.max_downstream_tasks_depth - 1) + 40 * start.max_downstream_tasks_depth) / 2
                for downstream_task in start.downstream_tasks:
                    y_increase = (20 * (downstream_task.max_downstream_tasks_depth - 1) + 40 * downstream_task.max_downstream_tasks_depth) / 2
                    y += y_increase
                    self.link_widgets.append(GanttLinkWidget((last_x+self.bb.x, last_y+self.bb.y), (x+self.bb.x, y+self.bb.y)))
                    self.generate_widgets(downstream_task, x, y)
                    y += y_increase + 20
                return
            new_start = start.downstream_tasks[0]
            if new_start.upstream_tasks[0] != start:
                widget = [widget for widget in self.task_widgets if widget.task == new_start][0]
                self.link_widgets.append(GanttLinkWidget((last_x+self.bb.x, last_y+self.bb.y), (widget.bb.x+widget.bb.width/2, widget.bb.y+widget.bb.height/2)))
                return
            if len(new_start.upstream_tasks) != 1:
                new_start_height = 20 * (new_start.max_upstream_tasks_depth - 1) + 40 * new_start.max_upstream_tasks_depth
                start_height = 20 * (start.max_upstream_tasks_depth - 1) + 40 * start.max_upstream_tasks_depth
                y += new_start_height/2 - start_height/2
            start = new_start
            self.link_widgets.append(GanttLinkWidget((last_x+self.bb.x, last_y+self.bb.y), (x+self.bb.x, y+self.bb.y)))
            self.task_widgets.append(GanttTaskWidget(start, (x+self.bb.x, y+self.bb.y)))

    def get_children(self):
        yield from self.link_widgets
        yield from self.task_widgets

    """def get_horizontal_nodes_count(self, start):
        # Keep track of how many nodes there are from this one
        horizontal_nodes_count = 1
        # As long as there are downstream nodes, ie this is not the last node
        while len(start.downstream_nodes) != 0:
            # We found another node
            horizontal_nodes_count += 1
            # If there are multiple downstream nodes, we have to increase horizontal_nodes_count with a recursive call
            if len(start.downstream_nodes) != 1:
                # Sub length is the length from the downstream nodes
                sub_length = 0
                for downstream_node in start.downstream_nodes:
                    # We don't care about smaller branches
                    sub_length = max(sub_length, self.get_horizontal_nodes_count(downstream_node))
                return horizontal_nodes_count + sub_length
            # If there is only one node, then we just continue in the tree
            start = start.downstream_nodes[0]
        return horizontal_nodes_count"""
