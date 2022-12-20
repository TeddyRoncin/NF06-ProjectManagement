from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget


class AddTaskTreeTaskWidget(TreeTaskWidget):

    """
    This represents a Task in the AddTaskTreeWidget. It is a specialization of the TreeTaskWidget.
    The difference is that the AddTaskTreeTaskWidget permits user to select it.
    It can also be disabled to prevent user from selecting it.

    These are the fields of an AddTaskTreeTaskWidget :
    - selected : A boolean that indicates if the Task is selected or not
    - on_click : The callback function that needs to be called when the Task is clicked.
                 It takes 2 parameters : the Task represented by the AddTaskTreeTaskWidget
                 and a boolean that indicates if the event selected the AddTaskTreeTaskWidget or not
    - enableable : A boolean that indicates if the Task can be enabled or not
    - enabled : A boolean that indicates if the Task is enabled or not
    """

    def __init__(self, task, position, get_position_offset, get_parent_bb, on_click, get_scale):
        """
        Creates a new AddTaskTreeTaskWidget
        :param task: The Task that the AddTaskTreeTaskWidget should represent
        :param position: The absolute position of the AddTaskTreeTaskWidget
        :param get_position_offset: A function that returns the amount of pixels that was dragged
        :param get_parent_bb: A function that returns the bounding box of the AddTaskTreeWidget
        :param on_click: The callback function that needs to be called when the Task is clicked.
                         It takes 2 parameters : the Task represented by the AddTaskTreeTaskWidget
                         and a boolean that indicates if the event selected the AddTaskTreeTaskWidget or not
        :param get_scale: A function that returns information about the zoom of the AddTaskTreeWidget.
                          It returns a tuple where the first element is the scale factor
                          and the second element is the center of the zoom
        """
        super().__init__(task, position, get_position_offset, get_parent_bb, get_scale)
        self.selected = False
        self.on_click = on_click
        # Is this task possible to enable ? The last task should not be, every other one should
        self.enableable = task.downstream_tasks_count != 0
        self.enabled = self.enableable

    def on_left_click_bb(self, pos):
        """
        This is called when the user left-clicks on the AddTaskTreeTaskWidget. It selects or unselects the Task
        and calls the callback function self.on_click
        :param pos: The relative position of the mouse when the user left-clicked
        :return: None
        """
        if self.enabled:
            self.selected = not self.selected
            self.on_click(self.task, self.selected)

    def draw(self, surface):
        """
        Draws the AddTaskTreeTaskWidget on the given Surface
        :param surface: The Surface on which the AddTaskTreeTaskWidget should be drawn
        :return: None
        """
        if self.selected:
            self._draw(surface, 0x00ff00)
        elif not self.enabled:
            self._draw(surface, 0xbbbbbb)
        else:
            super().draw(surface)

    def set_enabled(self):
        """
        Enables the AddTaskTreeTaskWidget. If it cannot be enabled (self.enableable is False), then nothing happens.
        :return: None
        """
        self.enabled = self.enableable
