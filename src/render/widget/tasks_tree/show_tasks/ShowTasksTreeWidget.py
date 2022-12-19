from render.widget.tasks_tree.TreeWidget import TreeWidget
from render.widget.tasks_tree.show_tasks.ShowTasksTreeLinkWidget import ShowTasksTreeLinkWidget
from render.widget.tasks_tree.show_tasks.ShowTasksTreeTaskWidget import ShowTasksTreeTaskWidget


class ShowTasksTreeWidget(TreeWidget):

    """
    Represents a tree. This is a specialisation of the TreeWidget. The difference between a normal TreeWidget
    and a ShowTasksTreeWidget is that the ShowTasksTreeWidget allows the user to click on a Task to select it.

    These are the fields of a ShowTasksTreeWidget :
    - selected_task: The Task that is currently selected by the user. If no Task is selected, this is None.
    - on_selection_change: A callback function that is called when the selected Task changes.
                           It takes a parameter : the new selected Task.
    """

    def __init__(self, position, size, first_task, on_selection_change):
        """
        Creates a new ShowTasksTreeWidget
        :param position: The absolute position of the ShowTasksTreeWidget
        :param size: The size of the ShowTasksTreeWidget
        :param first_task: The first Task of the ShowTasksTreeWidget
        :param on_selection_change: A callback function that is called when the selected Task changes.
                                    It takes the selected Task as parameter
        """
        super().__init__(position, size, first_task)
        self.selected_task = None
        self.on_selection_change = on_selection_change

    def generate_tree_task_widget(self, task, pos, get_position_offset, get_bb, get_scale):
        """
        Generates a ShowTasksTreeTaskWidget. This is automatically called by the TreeWidget when it needs to create
        a new TreeTaskWidget
        :param task: The Task the ShowTasksTreeTaskWidget represents
        :param pos: The absolute position of the ShowTasksTreeTaskWidget
        :param get_position_offset: A function that returns the amount of pixels in each direction dragged by the user
        :param get_bb: A function that returns the bounding box of this Widget
        :param get_scale: A function that returns the information about the zoom. It returns a tuple where
                          the first element is the scale factor and the second element is the center of the zoom
        :return: The generated ShowTasksTreeTaskWidget
        """
        return ShowTasksTreeTaskWidget(task,
                                       pos,
                                       get_position_offset,
                                       get_bb,
                                       self.on_task_clicked,
                                       lambda: self.selected_task,
                                       get_scale)

    def generate_tree_link_widget(self, start, end, get_position_offset, get_bb, from_task, to_task):
        """
        Generates a ShowTasksTreeLinkWidget. This is automatically called by the TreeWidget when it needs to create
        a new TreeLinkWidget
        :param start: The absolute coordinates of the start position of the ShowTasksTreeLinkWidget
        :param end: The absolute coordinates of the end position of the ShowTasksTreeLinkWidget
        :param get_position_offset: A function that returns the amount of pixels in each direction dragged by the user
        :param get_bb: A function that returns the bounding box of this Widget
        :param from_task: The Task the ShowTasksTreeLinkWidget is coming from
        :param to_task: The Task the ShowTasksTreeLinkWidget is going to
        :return: The generated ShowTasksTreeLinkWidget
        """
        return ShowTasksTreeLinkWidget(start, end, from_task, to_task, get_position_offset, get_bb)

    def on_task_clicked(self, task):
        """
        This is a callback function called by the TreeTasksTreeTaskWidgets when the user clicks on of it.
        It selects the Task. If the Task is already selected, it is deselected.
        It also calls the self.on_selection_change callback function
        :param task: The Task that was clicked
        :return: None
        """
        self.selected_task = None if self.selected_task == task else task
        self.on_selection_change(self.selected_task)
