from render.widget.tasks_tree.TreeLinkWidget import TreeLinkWidget


class ShowTasksTreeLinkWidget(TreeLinkWidget):

    """
    Represents a link between two tasks in the ShowTaskTreeWidget.
    The only difference between this and the normal TreeLinkWidget is that the color of the link is set to red
    if it represents a part of a critical path, i.e. if both tasks are critical.

    These are the fields of a ShowTasksTreeLinkWidget:
    - is_critical: Whether the link represents a part of a critical path, i.e. whether both tasks are critical.
    """

    def __init__(self, from_position, to_position, from_task, to_task, get_position_offset, get_parent_bb):
        """
        Creates a new ShowTasksTreeLinkWidget
        :param from_position: The absolute position the ShowTasksTreeLinkWidget is coming from
        :param to_position: The absolute position the ShowTasksTreeLinkWidget is going to
        :param from_task: The Task the ShowTasksTreeLinkWidget is coming from
        :param to_task: The Task the ShowTasksTreeLinkWidget is going to
        :param get_position_offset: A function that returns the amount of pixels in each direction dragged by the user
        :param get_parent_bb: A function that returns the bounding box of the parent Widget
        """
        super().__init__(from_position, to_position, get_position_offset, get_parent_bb)
        self.is_critical = from_task.is_critical and to_task.is_critical

    def draw(self, surface):
        """
        Draws the ShowTasksTreeLinkWidget on the given Surface
        :param surface: The Surface to draw the ShowTasksTreeLinkWidget on
        :return: None
        """
        if self.is_critical:
            self._draw(surface, 0xff0000)
        else:
            super().draw(surface)
