from render.widget.tasks_tree.TreeWidget import TreeWidget
from render.widget.tasks_tree.show_tasks.ShowTasksTreeLinkWidget import ShowTasksTreeLinkWidget
from render.widget.tasks_tree.show_tasks.ShowTasksTreeTaskWidget import ShowTasksTreeTaskWidget


class ShowTasksTreeWidget(TreeWidget):

    def __init__(self, position, size, first_task, on_selection_change):
        super().__init__(position, size, first_task)
        self.selected_task = None
        self.on_selection_change = on_selection_change

    def generate_tree_task_widget(self, task, pos, position_offset, get_bb):
        return ShowTasksTreeTaskWidget(task,
                                       pos,
                                       position_offset,
                                       get_bb,
                                       self.on_task_clicked,
                                       lambda: self.selected_task)

    def generate_tree_link_widget(self, start, end, get_position_offset, get_bb, start_widget, end_widget):
        return ShowTasksTreeLinkWidget(start, end, start_widget, end_widget, get_position_offset, get_bb)

    def on_task_clicked(self, task):
        self.selected_task = None if self.selected_task == task else task
        self.on_selection_change(self.selected_task)
