from render.widget.tasks_tree.TreeWidget import TreeWidget
from render.widget.tasks_tree.add_task.AddTaskTreeTaskWidget import AddTaskTreeTaskWidget


class AddTaskTreeWidget(TreeWidget):

    def __init__(self, pos, first_task, new_branch_checkbox):
        super().__init__(pos, (500, 500), first_task)
        self.new_branch_checkbox = new_branch_checkbox
        self.selected_tasks = set()

    def get_children(self):
        yield from super().get_children()

    def generate_tree_task_widget(self, task, pos, position_offset, get_bb, get_scale):
        return AddTaskTreeTaskWidget(task, pos, position_offset, get_bb, self.on_task_clicked, get_scale)

    def on_task_clicked(self, task, selected):
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
        still_enabled_tasks = set()
        for downstream in task.downstream_tasks:
            for upstream in downstream.upstream_tasks:
                still_enabled_tasks.add(upstream.id)
        for task_widget in self.task_widgets:
            if task_widget.task.id not in still_enabled_tasks:
                task_widget.enabled = False




