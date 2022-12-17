import pygame.font

from render.widget.Widget import Widget


class CheckboxWidget(Widget):

    def __init__(self, pos, label, on_value_changed=None):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 20)
        self.on_value_changed = on_value_changed
        label = label.split("\n")
        text_renders = [self.font.render(line, False, (0, 0, 0)) for line in label]
        width = max(text_renders, key=lambda text_render: text_render.get_width()).get_width()
        self.label_surface = pygame.Surface((width, len(label) * (self.font.get_height() + 4) - 4))
        # Make the background transparent
        self.label_surface.fill((255, 255, 255))
        self.label_surface.set_colorkey((255, 255, 255))
        for i, render in enumerate(text_renders):
            self.label_surface.blit(render, (0, (self.font.get_height() + 4) * i))
        self.bb = pygame.Rect(pos, (self.label_surface.get_width() + 20, max(self.label_surface.get_height() + 4, 15)))
        self.enabled = True
        self.activated = False

    def draw(self, surface):
        color = (0, 255, 0)
        if not self.enabled and not self.activated:
            color = (50, 50, 50)
        elif not self.enabled and self.activated:
            color = (50, 150, 50)
        elif self.enabled and not self.activated:
            color = (0, 0, 0)
        pygame.draw.rect(surface, color, pygame.Rect(0, (self.bb.height - 15) / 2, 15, 15))
        surface.blit(self.label_surface, (20, (self.bb.height - self.label_surface.get_height()) / 2))

    def on_left_click_bb(self, pos):
        if self.enabled:
            self.activated = not self.activated
            if self.on_value_changed:
                self.on_value_changed(self.activated)
