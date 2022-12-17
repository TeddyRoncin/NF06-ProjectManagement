import pygame

from utils.decorators import singleton

pygame.init()


@singleton
class Window:

    def __init__(self):
        self.window = pygame.display.set_mode(flags=pygame.RESIZABLE)
        self.screen = None
        self.mouse_left_at = (0, 0)
        self.scale_factor = 0
        self.offsets = (0, 0)
        self.real_render_size = (0, 0)
        self._compute_scale_info()

    def tick(self):
        if self.screen is None:
            return
        self.process_events()
        self.screen.update()
        self.render()

    def render(self):
        render = pygame.Surface((1920, 1080))
        render.fill(0xffffff)
        for widget in self.screen.get_widgets():
            self._render_widget(widget, render)
        pygame.transform.smoothscale(render,
                                     self.real_render_size,
                                     self.window.subsurface(pygame.Rect(self.offsets, self.real_render_size)))
        pygame.display.flip()

    def _render_widget(self, widget, render):
        widget.draw(render.subsurface(widget.get_bb().clamp(render.get_rect())))
        for child in widget.get_children():
            self._render_widget(child, render)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.VIDEORESIZE:
                self._compute_scale_info()
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
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                event.pos = ((event.pos[0] - self.offsets[0]) / self.scale_factor,
                             (event.pos[1] - self.offsets[1]) / self.scale_factor)
            if event.type == pygame.MOUSEMOTION:
                event.pos = ((event.pos[0] - self.offsets[0]) / self.scale_factor,
                             (event.pos[1] - self.offsets[1]) / self.scale_factor)
                event.rel = (event.rel[0] / self.scale_factor, event.rel[1] / self.scale_factor)
            for widget in self.screen.get_widgets():
                self._process_event_for_widget(event, widget)

    def _process_event_for_widget(self, event, widget):

        widget.process_event(event)
        for child in widget.get_children():
            self._process_event_for_widget(event, child)

    def set_screen(self, screen):
        self.screen = screen
        self.screen.reload()

    def _compute_scale_info(self):
        self.scale_factor = min(self.window.get_size()[0] / 1920, self.window.get_size()[1] / 1080)
        self.offsets = ((self.window.get_width() - (1920 * self.scale_factor)) / 2,
                        (self.window.get_height() - (1080 * self.scale_factor)) / 2)
        self.real_render_size = (1920 * self.scale_factor, 1080 * self.scale_factor)
