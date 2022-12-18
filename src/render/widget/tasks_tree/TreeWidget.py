import pygame.draw

from render.widget.tasks_tree.TreeLinkWidget import TreeLinkWidget
from render.widget.tasks_tree.TreeTaskWidget import TreeTaskWidget
from render.widget.Widget import Widget


class TreeWidget(Widget):

    """
    This class is a base class, it provides tools to create specialized TreeWidgets.
    It contains general utility features and a default definition of the methods.

    It represents a way to represent a Project. It shows each Task in a tree style.
    Tasks are linked together with TreeLinkWidgets. Downstream Tasks are to the right of upstream Tasks

    These are the fields of a TreeWidget :
    - project : The project to display
    - first_task : The first_task of the project
    - size : The size of the tree. There are no correlation between the bounding box and this field
    - task_widgets : A list containing TreeTaskWidgets. This Widget represents a Task.
                     See the TreeTaskWidget class for more information.
    - link_widgets : A list containing TreeLinkWidgets. This Widget represents a relation between Tasks.
                     See the TreeLinkWidget class for more information.
    - position_offset : This represents by how much the TreeWidget has been moved.
                        The TreeWidget can be moved by user dragging it.
    - scale_factor : This represents by how much the TreeWidget has been scaled.
                     The TreeWidget can be scaled by user scrolling up or down.
                     This is not implemented yet.
    - scale_center : This represents the center of the scale. It is relative to the center of the widget.
                     The TreeWidget center is moved according to where the user is scrolling.
                     This is not implemented yet.
    """

    def __init__(self, position, size, project):
        """
        Creates a new TreeWidget
        :param position: The absolute position of the Widget
        :param size: The size of the Widget
        :param project: The project that should be represented
        """
        super().__init__()
        self.project = project
        self.first_task = project.beginning_task
        self.bb = pygame.Rect(position, size)
        self.size = 0, 0
        self.task_widgets = []
        self.link_widgets = []
        self.reload()
        self.position_offset = (0, 0)
        self.scale_factor = 1
        # The scale center is relative to the center of the widget
        self.scale_center = (960, 540)

    def reload(self):
        """
        Reloads the TreeWidget after a modification of the layout of the Project
        :return: None
        """
        self.size = (self.first_task.downstream_tasks_count * 50,
                     50 * (self.first_task.max_downstream_tasks_depth - 1) +
                     100 * self.first_task.max_downstream_tasks_depth)
        self.task_widgets.clear()
        self.link_widgets.clear()
        self.generate_widgets(self.first_task, 50, self.size[1] / 2)

    def generate_widgets(self, start, x, y, length_differences_with_others=()):
        """
        Generates the TreeTaskWidgets and TreeLinkWidgets each task starting at the start parameter.
        It generates widgets until one of the following conditions is met :
        - The last task is reached.
        - The task is before an intersection. Downstream Widgets are then generated recursively.
        - The task is at the end of an intersection, and the task does not belong to the first branch
          of the intersection
        :param start: The first Task to draw
        :param x: The x position at which we should draw the Task start
        :param y: The y position at which we should draw the Task start
        :param length_differences_with_others: A list of length telling how much longer is the longest branch
                                               at the same depth level of each parent branch.
                                               This is used to make sure the x position of a Task is not smaller
                                               than one of its upstream Tasks.
        :return: None
        """
        # We add the first task
        self.task_widgets.append(self.generate_tree_task_widget(start,
                                                                (x + self.bb.x, y + self.bb.y),
                                                                lambda: self.position_offset,
                                                                self.get_bb,
                                                                lambda: (self.scale_factor, self.scale_center)))
        # We loop until we didn't reach the last task of the project.
        # If another condition described in this function docs is met earlier, we stop by returning off the function.
        while len(start.downstream_tasks) != 0:
            last_x = x
            last_y = y
            x += 150
            # This is the end of the line
            if len(start.downstream_tasks) != 1:
                y -= (50 * (start.max_downstream_tasks_depth - 1) + 100 * start.max_downstream_tasks_depth) / 2
                # For every downstream task, we generate the other widgets recursively
                for downstream_task in start.downstream_tasks:
                    y_increase = (50 * (downstream_task.max_downstream_tasks_depth - 1) +
                                  100 * downstream_task.max_downstream_tasks_depth) / 2
                    y += y_increase
                    self.link_widgets.append(self.generate_tree_link_widget((last_x + self.bb.x, last_y + self.bb.y),
                                                                            (x + self.bb.x, y + self.bb.y),
                                                                            lambda: self.position_offset,
                                                                            self.get_bb,
                                                                            start,
                                                                            downstream_task))
                    self.generate_widgets(downstream_task,
                                          x,
                                          y,
                                          length_differences_with_others=(
                                              *length_differences_with_others,
                                              start.downstream_tasks_count - 1 - downstream_task.downstream_tasks_count)
                                          )
                    y += y_increase + 50
                return
            # The next task we have to draw
            new_start = start.downstream_tasks[0]
            # If start is not the first task in the upstream_tasks of new_start, we don't generate new_start,
            # it should already be generated by another branch
            if new_start.upstream_tasks[0] != start:
                # We search the already-created widget representing new_start,
                # and then add a link between start and new_start
                widget = [widget for widget in self.task_widgets if widget.task == new_start][0]
                self.link_widgets.append(self.generate_tree_link_widget((last_x + self.bb.x, last_y + self.bb.y),
                                                                        (
                                                                            widget.bb.x + widget.bb.width / 2,
                                                                            widget.bb.y + widget.bb.height / 2
                                                                        ),
                                                                        lambda: self.position_offset, self.get_bb,
                                                                        start,
                                                                        new_start))
                return
            # We need to update the x and y values
            # (sorry, i won't explain how it works, i don't remember
            # and i really don't want to go back to it, that's just annoying math)
            if len(new_start.upstream_tasks) != 1:
                x += length_differences_with_others[-1] * 60
                new_start_height = \
                    50 * (new_start.max_upstream_tasks_depth - 1) + 100 * new_start.max_upstream_tasks_depth
                start_height = 50 * (start.max_upstream_tasks_depth - 1) + 100 * start.max_upstream_tasks_depth
                y += new_start_height/2 - start_height/2
                length_differences_with_others = length_differences_with_others[:-1]
            # Generate the link and the new_start widget
            self.link_widgets.append(self.generate_tree_link_widget((last_x + self.bb.x, last_y + self.bb.y),
                                                                    (x + self.bb.x, y + self.bb.y),
                                                                    lambda: self.position_offset, self.get_bb,
                                                                    start,
                                                                    new_start))
            self.task_widgets.append(self.generate_tree_task_widget(new_start,
                                                                    (x + self.bb.x, y + self.bb.y),
                                                                    lambda: self.position_offset,
                                                                    self.get_bb,
                                                                    lambda: (self.scale_factor, self.scale_center)))
            # And finally move to the next task
            start = new_start

    def get_children(self):
        """
        Returns a generator that provides a list of child Widgets that should be drawn on the screen.
        This Widget is drawn before the returned children
        :return: A generator that returns the children of this TreeWidget
        """
        yield from self.link_widgets
        yield from self.task_widgets

    def draw(self, surface):
        """
        Draws the TreeWidget on the surface.
        Almost everything is managed by the child Widgets, we simply need to change the background color
        :param surface: The surface on which to draw the TreeWidget
        :return: None
        """
        surface.fill((120, 120, 120))

    def on_mouse_motion_bb(self, pos, motion, buttons):
        """
        Called when the mouse is moved while the mouse is over the TreeWidget.
        This is used to move the TreeWidget around the screen.
        The TreeWidget is not moved if the left mouse button is not pressed.
        It updates self.position_offset to reflect the changes
        :param pos: The position of the mouse
        :param motion: This is a tuple representing how much the mouse moved on the screen
                       since the last mouse motion event was fired
        :param buttons: The buttons pressed by the user.
                        To get the state of a button, use buttons[pygame.BUTTON_{LEFT, RIGHT, MIDDLE}-1].
                        A value of 1 means the button is pressed, 0 means it is not.
        :return: None
        """
        if buttons[pygame.BUTTON_LEFT-1] == 1:
            # self.position_offset = (self.position_offset[0] + motion[0]/self.scale_factor,
            #                         self.position_offset[1] + motion[1]/self.scale_factor)
            self.position_offset = (self.position_offset[0] + motion[0], self.position_offset[1] + motion[1])

    def on_scroll_down(self):
        """
        Called when the user scrolls down. This is used to zoom out of the TreeWidget.
        To change the zoom level, the mouse needs to be in the bounding box of the TreeWidget.
        It updates the scale factor and the scale center accordingly to the position of the mouse
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.bb.collidepoint(mouse_pos) and self.scale_factor > 0.2:
            self.scale_center = (self.scale_center[0] + (mouse_pos[0]-self.scale_center[0]) / self.scale_factor,
                                 self.scale_center[1] + (mouse_pos[1]-self.scale_center[1]) / self.scale_factor)
            self.scale_factor -= 0.1

    def on_scroll_up(self):
        """
        Called when the user scrolls up. This is used to zoom in on the TreeWidget.
        To change the zoom level, the mouse needs to be in the bounding box of the TreeWidget.
        It updates the scale factor and the scale center accordingly to the position of the mouse
        :return: None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.bb.collidepoint(mouse_pos) and self.scale_factor < 4:
            self.scale_center = (self.scale_center[0] + (mouse_pos[0]-self.scale_center[0]) / self.scale_factor,
                                 self.scale_center[1] + (mouse_pos[1]-self.scale_center[1]) / self.scale_factor)
            self.scale_factor += 0.1

    def generate_tree_task_widget(self, task, pos, get_position_offset, get_bb, get_scale):
        """
        Generates a TreeTaskWidget for the given task.
        If a specialized TreeWidget (a child class of TreeWidget) needs a specific behavior from a TreeTaskWidget,
        it should override this method to return a subclass of TreeTaskWidget
        :param task: The Task used to generate the TreeTaskWidget
        :param pos: The absolute position of the TreeTaskWidget
        :param get_position_offset: A function that returns the position offset of the TreeWidget
        :param get_bb: A function that returns the bounding box of the TreeWidget
        :param get_scale: A function that returns the scale factor and the scale center of the TreeWidget in a tuple
        :return: The newly created TreeTaskWidget
        """
        return TreeTaskWidget(task, pos, get_position_offset, get_bb, get_scale)

    def generate_tree_link_widget(self, start, end, get_position_offset, get_bb, from_task, to_task):
        """
        Generates a TreeLinkWidget between the given Tasks.
        If a specialized TreeWidget (a child class of TreeWidget) needs a specific behavior from a TreeLinkWidget,
        it should override this method to return a subclass of TreeLinkWidget
        :param start: The absolute position of the upstream Task of the TreeLinkWidget
        :param end: The absolute position of the downstream Task of the TreeLinkWidget
        :param get_position_offset: A function that returns the position offset of the TreeWidget
        :param get_bb: A function that returns the bounding box of the TreeWidget
        :param from_task: The upstream Task. In this implementation, this is not used
        :param to_task: The downstream Task. In this implementation, this is not used
        :return: The newly created TreeLinkWidget
        """
        return TreeLinkWidget(start, end, get_position_offset, get_bb)
