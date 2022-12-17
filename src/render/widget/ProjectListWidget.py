import pygame

from render.widget.ProjectItemWidget import ProjectItemWidget
from render.widget.Widget import Widget
from render.widget.ScrollBarWidget import ScrollBarWidget


class ProjectListWidget(Widget):

    def __init__(self, bb, projects, on_item_clicked=lambda x: None):
        super().__init__()
        self.bb = bb
        self.items = []
        self.on_item_clicked = on_item_clicked
        self.font = pygame.font.SysFont("Arial", 16)
        self.total_height = 0
        self.scrollbar = ScrollBarWidget(self.get_bb, lambda: self.total_height)
        self.widgets_per_line = 0
        self.first_widget_x = 0
        self.set_projects(projects)

    def get_children(self):
        yield from self.items
        yield self.scrollbar

    def draw(self, surface):
        surface.fill(pygame.Color(100, 100, 0))

    def on_left_click_bb(self, pos):
        if pos[0] >= self.bb.width - self.scrollbar.bb.width:
            return
        absolute_pos = pos[0] + self.bb.x, pos[1] + self.bb.y
        for project_widget in self.items:
            if project_widget.actual_bb.collidepoint(absolute_pos):
                self.on_item_clicked(project_widget.project)
                return

    def get_scroll_in_pixel(self):
        return self.scrollbar.get_scroll_in_pixel()

    def set_projects(self, projects):
        self.widgets_per_line = self.bb.width // 320
        self.first_widget_x = (self.bb.width % 320) // 2
        min_height_index = 0
        heights_of_lines = [10] * self.widgets_per_line
        for project in projects:
            widget = ProjectItemWidget(project, 300, self.bb, self.get_scroll_in_pixel)
            widget.set_position((min_height_index * 320 + self.first_widget_x + self.bb.x,
                                 heights_of_lines[min_height_index] + self.bb.y))
            heights_of_lines[min_height_index] += widget.bb.height + 20
            for i, height in enumerate(heights_of_lines):
                if height < heights_of_lines[min_height_index]:
                    min_height_index = i
            self.items.append(widget)
