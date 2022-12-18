import pygame


class Widget:

    """
    This class is a base class, which means it should not be directly instanced.
    It contains general utility features and a default definition of the methods.

    Represents a widget on the Screen. A Widget is an element that should be used to render the Screen.
    It can for example be a text entry (EntryWidget), a scroll bar (ScrollBarWidget), ...
    It occupies a certain size at a certain position on the screen. These data are stored in a bounding box

    These are the fields of the class :
    - bb : The bounding box of the Widget. This doesn't have to be used by the children classes,
           but it is a tool that the Widget class provides.
    """

    def __init__(self):
        """
        Creates a new Widget
        """
        self.bb = pygame.Rect(0, 0, 0, 0)

    def get_bb(self):
        """
        Returns the bounding box of the Widget for the frame we are drawing.
        The implementation in this class returns field bb
        :return: A pygame.Rect object containing the position and the size of the Widget
        """
        return self.bb

    def get_children(self):
        """
        Returns a generator that provides all the children of the Widget.
        This is useful if the Widget is managing other Widget : for example, a Widget that displays
        a list of things (ListWidget) needs a ScrollingBarWidget, so the ScrollingBarWidget a child of the ListWidget.
        The parent Widget is drawn before the children
        By default, a Widget doesn't have children.
        :return: A generator containing all children of the class.
                 The children are drawn in the same order they are provided
        """
        yield from ()

    def draw(self, surface):
        """
        Draws the Widget to the Surface. This method is called at each frame. By default, nothing is drawn.
        :param surface: The Surface to draw the Widget to.
                        This is actually a subsurface, so modifying it will modify the parent Surface
        :return: None
        """
        pass

    def get_relative_pos(self, point, bb=None):
        """
        Returns the relative position of a point to a bounding box.
        This is the position of the point in the coordinate system with origin the top-left corner of the bounding box,
        x going right and y going down (same orientation as the Pygame coordinate systems)
        :param point: The point to translate into our coordinate system
        :param bb: The bounding box that permits creating the coordinate system.
                   By default, it is set to the value of Widget.get_bb()
        :return: A tuple containing the coordinates of the point in the new coordinate system
        """
        if not bb:
            bb = self.get_bb()
        return point[0] - bb.left, point[1] - bb.top

    def is_in_relative_bb(self, point, bb=None):
        """
        Returns whether a point is in a bounding box
        :param point: The point to check. It should be given as a tuple representing the x and y coordinates in the
                      coordinate system of the bounding box parameter bb
        :param bb: The bounding box to check. By default, its value is the value of Widget.get_bb()
        :return: Whether the point is in the bounding box
        """
        if not bb:
            bb = self.get_bb()
        return 0 <= point[0] < bb.width and 0 <= point[1] < bb.height

    def process_event(self, event):
        """
        Processes an event. It is called for each event that occurred at each frame.
        It dispatches the event through one or multiple of the methods below this one
        :param event: The raw event that occurred. This should be created by Pygame using the pygame.event module
        :return: None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pos = self.get_relative_pos(event.pos)
                self.on_left_click(pos)
                if self.is_in_relative_bb(pos):
                    self.on_left_click_bb(pos)
            elif event.button == pygame.BUTTON_RIGHT:
                bb = self.get_bb()
                pos = (event.pos[0] - bb.left, event.pos[1] - bb.top)
                self.on_right_click(pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.on_left_button_release()
            elif event.button == pygame.BUTTON_RIGHT:
                self.on_right_button_release()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                self.on_scroll_up()
            else:
                self.on_scroll_down()
        elif event.type == pygame.MOUSEMOTION:
            pos = self.get_relative_pos(event.pos)
            self.on_mouse_motion(pos, event.rel, event.buttons)
            if self.is_in_relative_bb(pos):
                self.on_mouse_motion_bb(pos, event.rel, event.buttons)
        elif event.type == pygame.KEYDOWN:
            self.on_key_press(event)

    def on_left_click(self, pos):
        """
        This is called when the user presses the left button on the mouse

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :param pos: The position of the click, relative to the bounding box of this Widget
        :return: None
        """
        pass

    def on_left_click_bb(self, pos):
        """
        This is called when the user presses the left button on the mouse
        and the click happens within the bounding box (returned by Widget.get_bb()) of this Widget

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :param pos: The position of the click, relative to the bounding box of this Widget
        :return: None
        """
        pass

    def on_left_button_release(self):
        """
        This is called when the user releases the left button on the mouse

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :return: None
        """
        pass

    def on_right_click(self, pos):
        """
        This is called when the user presses the right button on the mouse

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :param pos: The position of the click, relative to the bounding box of this Widget
        :return: None
        """
        pass

    def on_right_button_release(self):
        """
        This is called when the user releases the right button on the mouse

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :return: None
        """
        pass

    def on_scroll_up(self):
        """
        This is called when the user turns the visible part of the wheel of the mouse away from him.

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :return: None
        """
        pass

    def on_scroll_down(self):
        """
        This is called when the user turns the visible part of the wheel of the mouse closer to him.

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :return: None
        """
        pass

    def on_mouse_motion(self, pos, motion, buttons):
        """
        This is called when the user moves the mouse.

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :param pos: The position of the mouse, relative to the bounding box of this Widget
        :param motion: The new position of the mouse relative to the last one.
                       For example, if we moved 1 pixel to the right, then motion is (1,0)
        :param buttons: An array containing the buttons states. The index of each button is pygame.BUTTON_{button} - 1
        :return: None
        """
        pass

    def on_mouse_motion_bb(self, pos, motion, buttons):
        """
        This is called when the user moves the mouse
        and the event happens in the bounding box (returned by Widget.get_bb()) of this Widget.

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :param pos: The position of the mouse, relative to the bounding box of this Widget
        :param motion: The new position of the mouse relative to the last one.
                       For example, if we moved 1 pixel to the right, then motion is (1,0)
        :param buttons: An array containing the buttons states. The index of each button is pygame.BUTTON_{button} - 1
        :return: None
        """
        pass

    def on_key_press(self, event):
        """
        This is called when the user presses a key on the keyboard.

        It is automatically called by the Widget.process_event(event) method.
        If a Widget needs to fetch this event, it should overwrite this method.
        By default, it does nothing
        :param event: The raw event given by Pygame
        :return: None
        """
        pass
