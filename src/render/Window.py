import pygame

from utils.decorators import singleton

pygame.init()


@singleton
class Window:

    def __init__(self):
        self.screen = pygame.display.set_mode(flags=pygame.RESIZABLE)
        self.widget_manager = None
        self.mouse_left_at = (0, 0)

    def tick(self):
        if self.widget_manager is None:
            return
        self.process_events()
        self.widget_manager.update()
        self.render()

    def render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        for widget in self.widget_manager.get_widgets():
            self._render_widget(widget)
        pygame.display.flip()

    def _render_widget(self, widget):
        widget.draw(self.screen.subsurface(widget.get_bb().clamp(self.screen.get_rect())))
        for child in widget.get_children():
            self._render_widget(child)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.WINDOWLEAVE:
                self.mouse_left_at = pygame.mouse.get_pos()
            if event.type == pygame.WINDOWENTER:
                mouse_pos = pygame.mouse.get_pos()
                pygame.event.post(pygame.event.Event(
                    pygame.MOUSEMOTION,
                    pos=mouse_pos,
                    rel=(mouse_pos[0] - self.mouse_left_at[0], mouse_pos[1] - self.mouse_left_at[1]),
                    buttons=pygame.mouse.get_pressed(),
                ))
            for widget in self.widget_manager.get_widgets():
                self._process_event_for_widget(event, widget)

    def _process_event_for_widget(self, event, widget):

        widget.process_event(event)
        for child in widget.get_children():
            self._process_event_for_widget(event, child)

    def set_screen(self, screen):
        self.widget_manager = screen
        self.widget_manager.reload()


__all__ = [Window]
