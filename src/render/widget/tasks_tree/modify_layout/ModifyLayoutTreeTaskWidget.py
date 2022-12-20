from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget


class ModifyLayoutTreeTaskWidget(TreeTaskWidget):

    """
    Represents a Task in the ModifyLayoutTreeWidget. For the moment, it does not differ from a TreeTaskWidget.
    In the future, it should be able to be moved around the screen.

    These are the fields of a ModifyLayoutTreeTaskWidget (note that for the moment none of them are actually useful) :
    - on_drag : A callback function that will be called when the user starts dragging the ModifyLayoutTreeTaskWidget.
    - on_drop : A callback function that will be called when the user stops dragging the ModifyLayoutTreeTaskWidget.
                The function takes as parameters the Task that is represented, and the x and y absolute coordinates
                of the position the ModifyLayoutTreeTaskWidget was dropped at.
    - is_dragging : A boolean that indicates whether the ModifyLayoutTreeTaskWidget is currently being dragged.
    - drag_amount : The number of pixels the ModifyLayoutTreeTaskWidget has been dragged.
    """

    def __init__(self, task, position, get_position_offset, get_parent_bb, on_drag, on_drop, get_scale):
        """
        Creates a new ModifyLayoutTreeTaskWidget
        :param task: The Task represented by the ModifyLayoutTreeTaskWidget
        :param position: The absolute position of the ModifyLayoutTreeTaskWidget
        :param get_position_offset: A function that returns the amount of pixels that were dragged
                                    across the x and y axes
        :param get_parent_bb: A function that returns the bounding box of the parent of the ModifyLayoutTreeTaskWidget
        :param on_drag: A callback function that will be called when the user starts dragging
                        the ModifyLayoutTreeTaskWidget
        :param on_drop: A callback function that will be called when the user stops dragging the
                        ModifyLayoutTreeTaskWidget. The function takes as parameters the Task that is represented, and
                        the x and y absolute coordinates of the position the ModifyLayoutTreeTaskWidget was dropped at
        :param get_scale:
        """
        super().__init__(task, position, get_position_offset, get_parent_bb, get_scale)
        self.on_drag = on_drag
        self.on_drop = on_drop
        self.is_dragging = False
        self.drag_amount = (0, 0)

    def get_bb(self):
        """
        Returns the bounding box of the ModifyLayoutTreeTaskWidget. It also sets the value of self.actual_bb.
        :return: The bounding box of the ModifyLayoutTreeTaskWidget
        """
        return super().get_bb().move(self.drag_amount)

    def on_mouse_motion(self, pos, motion, buttons):
        """
        Called when the mouse is moved while the left mouse button is pressed. It drags the ModifyLayoutTreeTaskWidget
        if it is currently being dragged
        :param pos: The absolute position of the mouse
        :param motion: The amount of pixels the mouse was moved
        :param buttons: The buttons that are currently pressed. Each button can be accessed with
                        buttons[pygame.BUTTON_{LEFT/RIGHT/MIDDLE}-1]. If the value is 1, the button is pressed,
                        but it is not if the value is 0
        :return: None
        """
        if self.is_dragging:
            self.drag_amount = (self.drag_amount[0] + motion[0], self.drag_amount[1] + motion[1])

    def on_left_click_bb(self, pos):
        """
        Called when the left mouse button is clicked on the ModifyLayoutTreeTaskWidget.
        It starts dragging the ModifyLayoutTreeTaskWidget.

        For the moment, it is not implemented
        :param pos: The absolute position of the mouse when the event was fired
        :return: None
        """
        # TODO : implement this
        """radius = self.actual_bb.width / 2
        center = self.actual_bb.x + radius, self.actual_bb.y + radius
        if (pos[0] - radius) ** 2 + (pos[1] - radius) ** 2 <= radius ** 2:
            self.is_dragging = True
            self.on_drag()"""
        return

    def on_left_button_release(self):
        """
        Called when the left mouse button is released. It stops dragging the ModifyLayoutTreeTaskWidget.
        It calls the self.on_drop callback function and resets dragging information.

        For the moment, it is not implemented.
        :return: None
        """
        # TODO : implement this
        """if self.is_dragging:
            self.is_dragging = False
            self.drag_amount = (0, 0)
            self.on_drop(...)"""
        return
