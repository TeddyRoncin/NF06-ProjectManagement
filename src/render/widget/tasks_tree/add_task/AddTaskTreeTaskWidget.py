import pygame

from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget


class AddTaskTreeTaskWidget(TreeTaskWidget):

    def __init__(self, task, position, get_position_offset, get_parent_bb, on_click, get_scale):
        super().__init__(task, position, get_position_offset, get_parent_bb, get_scale)
        self.selected = False
        self.on_click = on_click
        # Is this task possible to enable ? The last task should not be, every other one should
        self.enableable = task.downstream_tasks_count != 0
        self.enabled = self.enableable

    def on_left_click_bb(self, pos):
        if self.enabled:
            self.selected = not self.selected
            self.on_click(self.task, self.selected)

    def draw(self, surface):
        if self.selected:
            self._draw(surface, 0x00ff00)
        elif not self.enabled:
            self._draw(surface, 0xbbbbbb)
        else:
            super().draw(surface)

    def set_enabled(self):
        self.enabled = self.enableable
