import pygame

from render.widget.ProjectItemWidget import ProjectItemWidget
from render.widget.Widget import Widget
from render.widget.ScrollBarWidget import ScrollBarWidget


class ProjectListWidget(Widget):

    """
    Represents the Widget that displays the list of projects on the HomeScreen.
    Every Project is represented by a ProjectItemWidget. They are stacked vertically.
    To display every project, it contains a ScrollBarWidget.

    These are the fields of a ProjectListWidget :
    - bb : The bounding box of the ProjectListWidget.
    - items : The list of ProjectItemWidget.
    - on_item_clicked : The callback function to call when a ProjectItemWidget is clicked.
    - total_height : The total height of the ProjectListWidget. There are no correlations between this value
                     and the height of the bounding box. It simply represents the optimal height
                     of the ProjectListWidget, but does not influence on its real height.
    - scrollbar : The ScrollBarWidget of the ProjectListWidget.
    """

    def __init__(self, bb, projects, on_item_clicked=lambda x: None):
        """
        Creates a new ProjectListWidget
        :param bb: The bounding box of the ProjectListWidget
        :param projects: The list of Projects to display
        :param on_item_clicked: The callback function to call when a ProjectItemWidget is clicked
        """
        super().__init__()
        self.bb = bb
        self.items = []
        self.on_item_clicked = on_item_clicked
        self.total_height = 0
        self.scrollbar = ScrollBarWidget(self.get_bb, lambda: self.total_height)
        self.set_projects(projects)

    def get_children(self):
        """
        Returns the list of children of the ProjectListWidget that should be displayed
        :return: A generator returning the children of the ProjectListWidget
        """
        yield from self.items
        yield self.scrollbar

    def draw(self, surface):
        """
        Draws the ProjectListWidget on the given Surface
        :param surface: The Surface to draw on
        :return: None
        """
        surface.fill(pygame.Color(100, 100, 0))

    def on_left_click_bb(self, pos):
        """
        Called when the left mouse button is clicked on the bounding box of the ProjectListWidget.
        It calls the self.on_item_clicked callback function with the Project that was clicked
        :param pos: The position of the mouse when the left mouse button was clicked
        :return: None
        """
        if pos[0] >= self.bb.width - self.scrollbar.bb.width:
            return
        absolute_pos = pos[0] + self.bb.x, pos[1] + self.bb.y
        for project_widget in self.items:
            if project_widget.actual_bb.collidepoint(absolute_pos):
                self.on_item_clicked(project_widget.project)
                return

    def get_scroll_in_pixel(self):
        """
        Returns the amount of pixels scrolled
        :return: The amount of pixels scrolled
        """
        return self.scrollbar.get_scroll_in_pixel()

    def set_projects(self, projects):
        """
        Sets the list of Projects to display. It creates a ProjectItemWidget for every Project.
        They are placed one by one in the column that is the shortest
        :param projects: The list of Projects to display
        :return: None
        """
        widgets_per_line = self.bb.width // 320
        first_widget_x = (self.bb.width % 320) // 2
        min_height_index = 0
        heights_of_lines = [10] * widgets_per_line
        for project in projects:
            widget = ProjectItemWidget(project, 300, self.bb, self.get_scroll_in_pixel)
            widget.set_position((min_height_index * 320 + first_widget_x + self.bb.x,
                                 heights_of_lines[min_height_index] + self.bb.y))
            heights_of_lines[min_height_index] += widget.bb.height + 20
            for i, height in enumerate(heights_of_lines):
                if height < heights_of_lines[min_height_index]:
                    min_height_index = i
            self.items.append(widget)
