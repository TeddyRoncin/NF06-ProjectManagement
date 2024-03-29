from render.widget.tasks_tree.TreeWidget import TreeWidget
from render.widget.tasks_tree.modify_layout.ModifyLayoutTreeLinkWidget import ModifyLayoutTreeLinkWidget
from render.widget.tasks_tree.modify_layout.ModifyLayoutTreeTaskWidget import ModifyLayoutTreeTaskWidget


class ModifyLayoutTreeWidget(TreeWidget):

    """
    Represents a TreeWidget where the user can modify the layout by dragging the links.

    These are the fields of a ModifyLayoutTreeWidget :
    - can_drag : A boolean that indicates if the user can drag the links or not.
                 The user cannot drag a link if he is already dragging once.
    """

    def __init__(self, position, size, project):
        """
        Creates a new ModifyLayoutTreeWidget
        :param position: The absolute position of the ModifyTreeLinkWidget
        :param size: The size of the ModifyTreeLinkWidget
        :param project: The Project to render
        """
        super().__init__(position, size, project)
        self.can_drag = True

    def generate_tree_task_widget(self, task, pos, get_position_offset, get_bb, get_scale):
        """
        Generates a new ModifyLayoutTreeTaskWidget
        :param task: The Task represented by the ModifyLayoutTreeTaskWidget
        :param pos: The absolute position of the ModifyLayoutTreeTaskWidget
        :param get_position_offset: A function that returns the amount of pixels that were dragged
        :param get_bb: A function that returns the bounding box of this ModifyLayoutTreeWidget
        :param get_scale: A function that returns information about the zoom.
                          This is a tuple containing the scale factor and the position of the center of the zoom
        :return: A new ModifyLayoutTreeTaskWidget
        """
        return ModifyLayoutTreeTaskWidget(task, pos, get_position_offset, get_bb, self.on_drag, self.on_tree_changing,
                                          get_scale)

    def generate_tree_link_widget(self, start, end, get_position_offset, get_bb, from_task, to_task):
        """
        Generates a new ModifyLayoutTreeLinkWidget
        :param start: The absolute position of the start of the ModifyLayoutTreeLinkWidget
        :param end: The absolute position of the end of the ModifyLayoutTreeLinkWidget
        :param get_position_offset: A function that returns the amount of pixels that were dragged
        :param get_bb: A function that returns the bounding box of this ModifyLayoutTreeWidget
        :param from_task: The upstream Task that the ModifyLayoutTreeLinkWidget connects
        :param to_task: The downstream Task that the ModifyLayoutTreeLinkWidget connects
        :return: A new ModifyLayoutTreeTaskWidget
        """
        return ModifyLayoutTreeLinkWidget(start, end, from_task, to_task, get_position_offset, get_bb, self.on_drag,
                                          self.on_tree_changing)

    def on_drag(self):
        """
        This is a callback function that is called by the ModifyLayoutTreeLinkWidgets when the user starts dragging
        a ModifyLayoutTreeLinkWidgets. This function returns whether the user can drag the ModifyLayoutTreeLinkWidget
        or not according to the value of self.can_drag. It also sets self.can_drag to False.
        :return: True if the user can drag the ModifyLayoutTreeLinkWidget, False otherwise
        """
        if not self.can_drag:
            return False
        self.can_drag = False
        return True

    def on_tree_changing(self, from_task, to_task, x, y):
        """
        This is a callback function that is called by the ModifyLayoutTreeLinkWidgets when the user stops dragging.
        First, self.can_drag is set to True to allow other ModifyLayoutTreeLinkWidgets to be dragged.
        Then, if the change is valid, the Project is updated. Finally, we reload the ModifyLayoutTreeWidget.
        :param from_task: The upstream Task that the ModifyLayoutTreeLinkWidget connects
        :param to_task: The downstream Task that the ModifyLayoutTreeLinkWidget connects
        :param x: The x coordinate of the position where downstream part of the ModifyLayoutTreeLinkWidget was dropped
        :param y: The y coordinate of the position where downstream part of the ModifyLayoutTreeLinkWidget was dropped
        :return: None
        """
        self.can_drag = True
        downstream_task = None
        for widget in self.task_widgets:
            bb = widget.get_bb()
            widget_pos = bb.x + bb.width / 2, bb.y + bb.height / 2
            if (x - widget_pos[0]) ** 2 + (y - widget_pos[1]) ** 2 < 50*50:
                downstream_task = widget.task
        # If we didn't click anywhere, there is nothing to do
        if downstream_task is None:
            return
        # We can't move a link that is before an intersection
        if len(from_task.downstream_tasks) > 1 or len(to_task.upstream_tasks) > 2:
            return
        # We can't move a link if from_task isn't the end of a branch
        if len(to_task.upstream_tasks) < 2:
            return
        # We can't move a link if the new downstream task is after an intersection
        if len(downstream_task.upstream_tasks) > 1:
            return
        # We can't move a link if the new downstream task is the first task of a branch
        if len(downstream_task.upstream_tasks[0].downstream_tasks) > 1:
            return
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
            while current_task != downstream_task and \
                    current_task.downstream_tasks_count < downstream_task.downstream_tasks_count and \
                    depth >= 0:
                if len(current_task.upstream_tasks) > 1:
                    depth += 1
                current_task = current_task.upstream_tasks[0]
                if len(current_task.downstream_tasks) > 1:
                    depth -= 1
            if current_task != downstream_task or depth < 0:
                return
        else:
            current_task = to_task
            while current_task != downstream_task and \
                    current_task.downstream_tasks_count > downstream_task.downstream_tasks_count and \
                    depth >= 0:
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
        # We need to know at which position the task should be inserted as an upstream task
        depth = 1
        last_task = None
        current_task = from_task
        while depth > 0:
            if len(current_task.upstream_tasks) > 1:
                depth += 1
            last_task = current_task
            current_task = current_task.upstream_tasks[0]
            if len(current_task.downstream_tasks) > 1:
                depth -= 1
        # We can now insert the task at the right position
        downstream_task.add_upstream_task(from_task, current_task.downstream_tasks.index(last_task))
        self.reload()

    def on_mouse_motion_bb(self, pos, motion, buttons):
        """
        This function is called when the user moves the mouse while the mouse is over ModifyLayoutTreeWidget.
        It only drags the ModifyLayoutTreeWidget if the user is not dragging a ModifyLayoutTreeLinkWidget
        :param pos: The relative position of the mouse
        :param motion: The amount the mouse moved since the last MOUSEMOTION event was fired
        :param buttons: The buttons that are currently pressed. Each button can be accessed with
                        buttons[pygame.BUTTON_{LEFT/RIGHT/MIDDLE}-1]. If the value is 1, the button is pressed,
                        but it is not if the value is 0
        :return: None
        """
        if self.can_drag:
            super().on_mouse_motion_bb(pos, motion, buttons)
