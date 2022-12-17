from render.widget.tasks_tree.TreeWidget import TreeWidget
from render.widget.tasks_tree.modify_layout.ModifyLayoutTreeLinkWidget import ModifyLayoutTreeLinkWidget
from render.widget.tasks_tree.modify_layout.ModifyLayoutTreeTaskWidget import ModifyLayoutTreeTaskWidget


class ModifyLayoutTreeWidget(TreeWidget):

    def __init__(self, position, task):
        super().__init__(position, (500, 500), task)
        self.can_drag = True

    def generate_tree_task_widget(self, task, pos, position_offset, get_bb, get_scale):
        return ModifyLayoutTreeTaskWidget(task, pos, position_offset, get_bb, self.on_drag, self.on_tree_changing, get_scale)

    def generate_tree_link_widget(self, start, end, get_position_offset, get_bb, start_widget, end_widget):
        return ModifyLayoutTreeLinkWidget(start, end, start_widget, end_widget, get_position_offset, get_bb, self.on_drag, self.on_tree_changing)

    def on_drag(self):
        if not self.can_drag:
            return False
        self.can_drag = False
        return True

    def on_tree_changing(self, from_task, to_task, x, y):
        self.can_drag = True
        downstream_task = None
        for widget in self.task_widgets:
            bb = widget.get_bb()
            widget_pos = bb.x + bb.width / 2, bb.y + bb.height / 2
            if (x - widget_pos[0]) ** 2 + (y - widget_pos[1]) ** 2 < 100:
                downstream_task = widget.task
        # If we didn't click anywhere, there is nothing to do
        if downstream_task is None:
            return
        # We can't move a link that is before an intersection
        if len(from_task.downstream_tasks) > 1 or len(to_task.upstream_tasks) > 1:
            return
        # We can't move a link if from_task isn't the end of a branch
        if len(to_task.upstream_tasks) < 2:
            return
        # We cannot make the downstream task of the task a "more downstream" task than the last
        # (by default it will be the "most downstream" possible)
        # What's more, there must be at least 1 task that is "jumped" by the branch
        """if from_task.downstream_tasks[0].downstream_tasks_count >= downstream_task.downstream_tasks_count:
            return"""
        # We now need to verify that both tasks are on the same branch and at the same depth
        # For that, we just go upstream from the old downstream tasks into the tree,
        # and try to find the new downstream task
        # If at some point, the current downstream task has less downstream tasks than the old downstream task,
        # we know we already past it. Because we could not find it, it is not on the same branch at the same depth
        # If at some point the depth (relative to the old downstream task) is negative,
        # then we left the branch, and we can conclude that the two tasks are not on the same branch
        # (at least not at the same depth)
        depth = 0
        if to_task.downstream_tasks_count < downstream_task.downstream_tasks_count:
            current_task = to_task.upstream_tasks[0]
            if current_task == from_task:
                # There must be at least one more
                current_task = to_task.upstream_tasks[1]
            while current_task != downstream_task and current_task.downstream_tasks_count < downstream_task.downstream_tasks_count and depth >= 0:
                if len(current_task.upstream_tasks) > 1:
                    depth += 1
                current_task = current_task.upstream_tasks[0]
                if len(current_task.downstream_tasks) > 1:
                    depth -= 1
            if current_task != downstream_task or depth < 0:
                return
        else:
            current_task = to_task
            while current_task != downstream_task and current_task.downstream_tasks_count > downstream_task.downstream_tasks_count and depth >= 0:
                if len(current_task.downstream_tasks) > 1:
                    depth += 1
                current_task = current_task.downstream_tasks[0]
                if len(current_task.upstream_tasks) > 1:
                    depth -= 1
            if current_task != downstream_task or depth < 0:
                return
        downstream_tasks = list(from_task.downstream_tasks)
        for task in downstream_tasks:
            task.remove_upstream_task(from_task)
        downstream_task.add_upstream_task(from_task)
        self.reload()

    def on_mouse_motion_bb(self, pos, motion, buttons):
        if self.can_drag:
            super().on_mouse_motion_bb(pos, motion, buttons)
