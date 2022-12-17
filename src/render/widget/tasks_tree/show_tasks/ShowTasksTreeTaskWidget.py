import pygame

from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget


class ShowTasksTreeTaskWidget(TreeTaskWidget):

    def __init__(self, task, position, get_position_offset, get_parent_bb, on_click, get_selected_task, get_scale):
        super().__init__(task, position, get_position_offset, get_parent_bb, get_scale)
        self.on_click = on_click
        self.get_selected_task = get_selected_task

    def draw(self, surface):
        if self.get_selected_task() == self.task:
            self._draw(surface, circle_color=pygame.Color(0, 0, 255))
        else:
            super().draw(surface)

    def on_left_click_bb(self, pos):
        self.on_click(self.task)
