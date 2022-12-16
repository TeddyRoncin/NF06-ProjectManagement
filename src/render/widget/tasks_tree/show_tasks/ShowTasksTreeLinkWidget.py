from render.widget.tasks_tree.TreeLinkWidget import TreeLinkWidget


class ShowTasksTreeLinkWidget(TreeLinkWidget):

    def __init__(self, from_position, to_position, from_widget, to_widget, get_position_offset, get_parent_bb):
        super().__init__(from_position, to_position, get_position_offset, get_parent_bb)
        self.from_widget = from_widget
        self.to_widget = to_widget
        print(self.from_widget.is_critical, self.to_widget.is_critical)
        self.is_critical = self.from_widget.is_critical and self.to_widget.is_critical

    def draw(self, surface):
        if self.is_critical:
            self._draw(surface, 0xff0000)
        else:
            super().draw(surface)

