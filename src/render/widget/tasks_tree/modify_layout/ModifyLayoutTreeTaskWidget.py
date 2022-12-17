from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget


class ModifyLayoutTreeTaskWidget(TreeTaskWidget):

    def __init__(self, task, position, get_position_offset, get_parent_bb, on_drag, on_drop, get_scale):
        super().__init__(task, position, get_position_offset, get_parent_bb, get_scale)
        self.on_drag = on_drag
        self.on_drop = on_drop
        self.is_dragging = False
        self.drag_amount = (0, 0)

    def get_bb(self):
        return super().get_bb().move(self.drag_amount)

    def on_mouse_motion(self, pos, motion, buttons):
        if self.is_dragging:
            self.drag_amount = (self.drag_amount[0] + motion[0], self.drag_amount[1] + motion[1])

    def on_left_click_bb(self, pos):
        # TODO : implement this
        return
        radius = self.actual_bb.width / 2
        center = self.actual_bb.x + radius, self.actual_bb.y + radius
        print("clicking ! ", pos, center, radius)
        if (pos[0] - radius) ** 2 + (pos[1] - radius) ** 2 <= radius ** 2:
            self.is_dragging = True
            self.on_drag()

    def on_left_button_release(self):
        # TODO : implement this
        return
        if self.is_dragging:
            self.is_dragging = False
            self.drag_amount = (0, 0)
            self.on_drop()
