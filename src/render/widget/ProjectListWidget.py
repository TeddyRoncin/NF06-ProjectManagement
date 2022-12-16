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
        """scroll = self.get_scroll_in_pixel()
        for i, item in enumerate(self.items):
            surface.blit(self.font.render(item, True, pygame.Color(255, 255, 255)), (0, i * self.item_height - scroll))"""

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
        x = self.first_widget_x
        y = 10
        max_height_of_line = 0
        for project in projects:
            widget = ProjectItemWidget(project, 300, self.bb, self.get_scroll_in_pixel)
            if x + widget.bb.width > self.bb.width - 10:
                x = self.first_widget_x
                y += max_height_of_line + 10
            if widget.bb.height > max_height_of_line:
                max_height_of_line = widget.bb.height
            widget.set_position((x + self.bb.x, y + self.bb.y))
            print("adding widget at", (x,y))
            self.items.append(widget)
            x += widget.bb.width + 10
            print("adding project " + str(project.name))
        print(self.items)
        self.total_height = y + max_height_of_line + 10
        print(self.total_height)
