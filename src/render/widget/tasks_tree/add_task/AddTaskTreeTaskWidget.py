import pygame

from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget


class AddTaskTreeTaskWidget(TreeTaskWidget):

    def __init__(self, task, position, get_position_offset, get_parent_bb, on_click):
        super().__init__(task, position, get_position_offset, get_parent_bb)
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
        super().draw(surface)
        if self.selected:
            mask = pygame.Surface(self.bb.size)
            mask.fill((0, 255, 0))
            mask.set_alpha(75)
            surface.blit(mask, (0, 0))
        elif not self.enabled:
            mask = pygame.Surface((50, 50))
            mask.fill((255, 255, 255))
            mask.set_alpha(75)
            surface.blit(mask, (0, 0))

    def set_enabled(self):
        self.enabled = self.enableable