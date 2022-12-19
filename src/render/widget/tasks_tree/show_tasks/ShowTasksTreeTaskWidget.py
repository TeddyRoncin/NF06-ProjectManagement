from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget


class ShowTasksTreeTaskWidget(TreeTaskWidget):

    """
    Represents a Task in a ShowTaskTreeWidget. The only difference between this and the normal TreeTaskWidget is that
    the ShowTasksTreeTaskWidget is selectable.

    These are the fields of a ShowTasksTreeTaskWidget :
    - on_click: A callback function that is called when the ShowTasksTreeTaskWidget is clicked.
                It takes a parameter : the associated Task to the ShowTasksTreeTaskWidget
    - get_selected_task: A function that returns the currently selected Task.
                         This is used to know if the current instance is the Task selected.
    """

    def __init__(self, task, position, get_position_offset, get_parent_bb, on_click, get_selected_task, get_scale):
        """
        Creates a new ShowTasksTreeTaskWidget
        :param task: The Task the ShowTasksTreeTaskWidget represents
        :param position: The absolute position of the ShowTasksTreeTaskWidget
        :param get_position_offset: A function that returns the amount of pixels in each direction dragged by the user
        :param get_parent_bb: A function that returns the bounding box of the parent Widget
        :param on_click: A callback function that is called when the ShowTasksTreeTaskWidget is clicked
        :param get_selected_task: A function that returns the currently selected Task
        :param get_scale: A function that returns the information about the zoom. It returns a tuple where
                          the first element is the scale factor and the second element is the center of the zoom
        """
        super().__init__(task, position, get_position_offset, get_parent_bb, get_scale)
        self.on_click = on_click
        self.get_selected_task = get_selected_task

    def draw(self, surface):
        """
        Draws the ShowTasksTreeTaskWidget on the given Surface
        :param surface: The Surface to draw the ShowTasksTreeTaskWidget on
        :return: None
        """
        if self.get_selected_task() == self.task:
            self._draw(surface, circle_color=0xbbbbbb)
        else:
            super().draw(surface)

    def on_left_click_bb(self, pos):
        """
        Called when the ShowTasksTreeTaskWidget is clicked. This method simply calls the callback function on_click
        :param pos: The relative position of the click
        :return: None
        """
        self.on_click(self.task)
