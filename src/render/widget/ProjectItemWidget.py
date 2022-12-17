import pygame.font

from render.widget.Widget import Widget


class ProjectItemWidget(Widget):

    def __init__(self, project, width, parent_bb, get_scroll):
        super().__init__()
        self.project = project
        self.parent_bb = parent_bb
        self.get_scroll = get_scroll
        self.bb = pygame.Rect(0, 0, width, 0)
        self.actual_bb = self.bb.copy()
        self.crop_amount = 0
        text_renders = []
        name_font = pygame.font.SysFont("Arial", 24)
        description_font = pygame.font.SysFont("Arial", 16)
        split_name = project.name.split(" ")
        font_height = name_font.get_height()
        whitespace_size = name_font.size(" ")[0]
        x = y = 5
        for word in split_name:
            text_render = name_font.render(word, True, 0x000000)
            if x + text_render.get_width() > width - 5:
                x = 5
                y += font_height + 3
            text_renders.append((text_render, (x, y)))
            x += text_render.get_width() + whitespace_size
        split_description = project.description.split(" ")
        font_height = description_font.get_height()
        whitespace_size = description_font.size(" ")[0]
        x = 5
        y += 50
        for word in split_description:
            text_render = description_font.render(word, True, 0x000000)
            if x + text_render.get_width() > width - 5:
                x = 5
                y += font_height + 3
            text_renders.append((text_render, (x, y)))
            x += text_render.get_width() + whitespace_size
        self.bb.height = y + font_height + 5
        self.render = pygame.Surface(self.bb.size)
        self.render.fill(0xaaaaaa)
        for word in text_renders:
            self.render.blit(word[0], word[1])
        pygame.draw.rect(self.render, 0x000000, pygame.Rect((0, 0), self.bb.size), 1)

    def draw(self, surface):
        surface.blit(self.render, (0, -self.crop_amount))

    def get_bb(self):
        self.actual_bb = self.bb.move(0, -self.get_scroll())
        self.crop_amount = max(0, self.parent_bb.y - self.actual_bb.y)
        self.actual_bb = self.actual_bb.clip(self.parent_bb)
        print(self.actual_bb)
        return self.actual_bb

    def set_position(self, pos):
        self.bb.topleft = pos
