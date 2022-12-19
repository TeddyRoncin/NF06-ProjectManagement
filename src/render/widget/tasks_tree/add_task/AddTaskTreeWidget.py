from render.widget.tasks_tree.TreeWidget import TreeWidget
from render.widget.tasks_tree.add_task.AddTaskTreeTaskWidget import AddTaskTreeTaskWidget


class AddTaskTreeWidget(TreeWidget):

    """
    Represents a Tree. This is a specialization of the TreeWidget. The difference is that this tree permits user
    to select Tasks to then add a new Task. The selected Tasks will be the upstream Tasks of the new Task.

    These are the fields of an AddTaskTreeWidget :
    - new_branch_checkbox : A checkbox Widget to know if the new Task should be added to a new branch or not
    - selected_tasks : A set of Tasks that have been selected by the user
    """

    def __init__(self, pos, size, first_task, new_branch_checkbox):
        """
        Creates a new AddTaskTreeWidget
        :param pos: The absolute position of the TreeWidget
        :param size: The size of the TreeWidget
        :param first_task: The first Task of the project
        :param new_branch_checkbox: The checkbox to know if the new Task should be added to a new branch or not
        """
        super().__init__(pos, size, first_task)
        self.new_branch_checkbox = new_branch_checkbox
        self.selected_tasks = set()

    def get_children(self):
        """
        Returns the children of the TreeWidget that should be rendered
        :return: A generator that yields the children of the TreeWidget
        """
        yield from super().get_children()

    def generate_tree_task_widget(self, task, pos, get_position_offset, get_bb, get_scale):
        """
        Generates a AddTaskTreeTaskWidget.
        This is automatically called by the TreeWidget when it needs to generate a new TreeTaskWidget
        :param task: The Task that the AddTaskTreeTaskWidget should represent
        :param pos: The absolute position of the AddTaskTreeTaskWidget
        :param get_position_offset: A function that returns the amount of pixels that was dragged
        :param get_bb: A function that returns the bounding box of the AddTaskTreeWidget
        :param get_scale: A function that returns information about the zoom of the AddTaskTreeWidget.
                          It returns a tuple where the first element is the scale factor
                          and the second element is the center of the zoom
        :return: The generated AddTaskTreeTaskWidget
        """
        return AddTaskTreeTaskWidget(task, pos, get_position_offset, get_bb, self.on_task_clicked, get_scale)

    def on_task_clicked(self, task, selected):
        """
        This is the callback function called by the AddTaskTreeTaskWidgets when a Task is clicked.
        It adds or removes the Task from the self.selected_tasks set.
        It also updates the enabled state of all the AddTaskTreeTaskWidgets
        and the enabled state of the new_branch_checkbox
        :param task: The Task that was clicked
        :param selected: Whether the event selected or unselected the Task
        :return: None
        """
        if selected:
            self.selected_tasks.add(task)
            self.on_enable_task(task)
        else:
            self.selected_tasks.remove(task)
            # Reset enable field for all widgets
            for widget in self.task_widgets:
                widget.set_enabled()
            # And select all the widgets back
            for widget in self.task_widgets:
                if widget.selected:
                    self.on_enable_task(widget.task)
            # It should never be activated after a task has been unselected
            self.new_branch_checkbox.activated = False
        # We decide if we should enable the new_branch_checkbox
        self.new_branch_checkbox.enabled = False
        if len(self.selected_tasks) == 1:
            selected_task = next(iter(self.selected_tasks))
            # It is not possible to create a new branch from the last or the second to last widget of a branch
            # Verify it's not the last task
            if len(selected_task.downstream_tasks) != 0 and len(selected_task.downstream_tasks[0].upstream_tasks) == 1:
                # Verify it's not the second to last task
                if len(selected_task.downstream_tasks[0].downstream_tasks) != 0 and \
                        len(selected_task.downstream_tasks[0].downstream_tasks[0].upstream_tasks) == 1:
                    self.new_branch_checkbox.enabled = True

    def on_enable_task(self, task):
        """
        It enables a single AddTaskTreeTaskWidget. It also disables all the Tasks that cannot be selected
        at the same time as the given Task
        :param task:
        :return:
        """
        # A list of all the Tasks that can still be selected
        still_enabled_tasks = set()
        for downstream in task.downstream_tasks:
            for upstream in downstream.upstream_tasks:
                still_enabled_tasks.add(upstream.id)
        for task_widget in self.task_widgets:
            # If the task is not in the still_enabled_tasks set, it means that it can no longer be selected
            # If it does, we do not enable it, because it could have been disabled by a previous call to this function
            if task_widget.task.id not in still_enabled_tasks:
                task_widget.enabled = False
