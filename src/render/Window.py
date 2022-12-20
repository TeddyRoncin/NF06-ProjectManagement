import sys

import pygame

from utils.decorators import singleton


# Initialize pygame
pygame.init()


@singleton
class Window:

    """
    It is a singleton, meaning it is instantiated only once and automatically. It should not be instantiated manually.
    The instance can be accessed using the instance class field

    Represents the Window of the application. It manages the rendering and the events.
    The rendering is not done directly on the screen, but instead on a 1920x1080 surface,
    which is then scaled to fit the screen.

    These are the fields of the Window :
    - window : The pygame screen
    - screen : The current Screen. It is the screen that is currently displayed.
               Only one screen can be displayed at a time.
    - mouse_left_at : The position of the mouse when it left the Window. When the mouse leaves
                      and then re-enters the Window at a different position, no MOUSEMOTION event is fired by pygame
                      telling how much the mouse moved outside the Window. This field is used to manually fire
                      this missing event when the mouse re-enters the Window.
    - scale_factor : The factor by which the rendering is scaled down
                     (for example, if the Window is 3840x2160 pixels, then rendering is scaled down by a factor of 2).
                     It is the smallest factor between the width and the height of the Window.
                     It is recomputed automatically when the Window is resized.
    - offsets : The offsets of the rendering on the Window. If the Window does not have the same aspect ratio
                as the rendering (which is 16:9), then black rectangles are left on the sides.
                This field represents the coordinates of the top left corner of the rendering on the Window.
                It is recomputed automatically when the Window is resized.
    - real_render_size : The size of the rendering on the Window in pixels.
                         It may not be 1920x1080 if the size of the Window is different from 1920x1080.
                         It is used to know how to scale the rendering to fit the Window.
                         It is recomputed automatically when the Window is resized.
    """

    def __init__(self):
        """
        Creates the Window
        """
        self.window = pygame.display.set_mode(flags=pygame.RESIZABLE)
        pygame.display.set_caption("Project Manager")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        self.screen = None
        self.mouse_left_at = (0, 0)
        self.scale_factor = 0
        self.offsets = (0, 0)
        self.real_render_size = (0, 0)
        self._compute_scale_info()

    def tick(self):
        """
        A call to this method is the very definition of a frame :)
        It processes the events, then renders the screen.
        :return:
        """
        if self.screen is None:
            return
        self.process_events()
        self.screen.update()
        self.render()

    def render(self):
        """
        Renders the screen on the Window. It first creates the rendering surface, then renders the Widgets on it,
        draws it onto the Window, and finally flushes the render
        :return: None
        """
        render = pygame.Surface((1920, 1080))
        render.fill(0xffffff)
        for widget in self.screen.get_widgets():
            self._render_widget(widget, render)
        pygame.transform.smoothscale(render,
                                     self.real_render_size,
                                     self.window.subsurface(pygame.Rect(self.offsets, self.real_render_size)))
        pygame.display.flip()

    def _render_widget(self, widget, render):
        """
        Renders a Widget and its children. This method is called recursively for each child of the given Widget.
        This is an internal method and should not be called outside this class
        :param widget: The Widget to render
        :param render: The rendering surface of the frame
        :return: None
        """
        widget.draw(render.subsurface(widget.get_bb().clamp(render.get_rect())))
        for child in widget.get_children():
            self._render_widget(child, render)

    def process_events(self):
        """
        Processes the events. For each event, depending on its type, it does the following :
        - If the event is a QUIT event, it quits the application
        - If the event is a VIDEORESIZE event, it resizes recomputes the scaling info
        - If the event is a WINDOWLEAVE event, it records the position of the mouse
        - If the event is a WINDOWENTER event, it fires a MOUSEMOTION event for the traveled distance
          since the mouse left
        - If the event is a MOUSEBUTTONDOWN, MOUSEBUTTONUP or MOUSEMOTION event,
          it modifies the positions so that they are correct in the rendering surface referential.
        In any case (except if we already left the application), the event is fired for every Widget of the screen
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
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
        """
        Processes an event for a Widget and its children.
        This method is called recursively for each child of the given Widget.
        This is an internal method and should not be called outside this class
        :param event: The event to process
        :param widget: The Widget that will process the event
        :return: None
        """
        widget.process_event(event)
        for child in widget.get_children():
            self._process_event_for_widget(event, child)

    def set_screen(self, screen):
        """
        Changes the current Screen. It sets the given Screen as the current one, and reloads it
        :param screen: The new Screen
        :return: None
        """
        self.screen = screen
        self.screen.reload()

    def _compute_scale_info(self):
        """
        Computes the scaling info. It computes the scale_factor, the offsets and the real_render_size fields.
        This is an internal method and should not be called outside this class.
        It is called automatically when the Window is created or resized.
        :return: None
        """
        self.scale_factor = min(self.window.get_size()[0] / 1920, self.window.get_size()[1] / 1080)
        self.offsets = ((self.window.get_width() - (1920 * self.scale_factor)) / 2,
                        (self.window.get_height() - (1080 * self.scale_factor)) / 2)
        self.real_render_size = (1920 * self.scale_factor, 1080 * self.scale_factor)
