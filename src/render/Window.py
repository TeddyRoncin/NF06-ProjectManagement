import pygame


pygame.init()


class Window:
    instance = None

    def __init__(self):
        Window.instance = self
        self.screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
        self.widgets = []

    def tick(self):
        self.process_events()
        self.render()

    def render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        for widget in self.widgets:
            self._render_widget(widget)
        pygame.display.flip()

    def _render_widget(self, widget):
        widget.draw(self.screen.subsurface(widget.get_bb()))
        for child in widget.get_children():
            self._render_widget(child)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            for widget in self.widgets:
                self._process_event_for_widget(event, widget)

    def _process_event_for_widget(self, event, widget):
        widget.process_event(event)
        for child in widget.get_children():
            self._process_event_for_widget(event, child)

    def set_screen(self, screen):
        self.widgets = screen.value


__all__ = [Window]
