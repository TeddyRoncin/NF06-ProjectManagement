from render.widget.tasks_tree.TreeWidget import TreeWidget
from render.widget.tasks_tree.show_tasks.ShowTasksTreeTaskWidget import ShowTasksTreeTaskWidget


class ShowTasksTreeWidget(TreeWidget):

    def __init__(self, position, first_task, on_selection_change):
        super().__init__(position, first_task)
        self.selected_task = None
        self.on_selection_change = on_selection_change

    def generate_tree_task_widget(self, task, pos, position_offset, get_bb):
        return ShowTasksTreeTaskWidget(task, pos, position_offset, get_bb, self.on_task_clicked, lambda: self.selected_task)

    def on_task_clicked(self, task):
        self.selected_task = None if self.selected_task == task else task
        self.on_selection_change(self.selected_task)
