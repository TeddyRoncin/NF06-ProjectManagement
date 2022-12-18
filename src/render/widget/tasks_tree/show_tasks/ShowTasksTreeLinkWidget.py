from render.widget.tasks_tree.TreeLinkWidget import TreeLinkWidget


class ShowTasksTreeLinkWidget(TreeLinkWidget):

    def __init__(self, from_position, to_position, from_task, to_task, get_position_offset, get_parent_bb):
        super().__init__(from_position, to_position, get_position_offset, get_parent_bb)
        self.from_task = from_task
        self.to_task = to_task
        self.is_critical = self.from_task.is_critical and self.to_task.is_critical

    def draw(self, surface):
        if self.is_critical:
            self._draw(surface, 0xff0000)
        else:
            super().draw(surface)

