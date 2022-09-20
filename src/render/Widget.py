import pygame


class Widget:
    def __init__(self):
        self.bb = pygame.Rect(0, 0, 0, 0)

    def get_bb(self):
        return self.bb

    def get_children(self):
        return []

    def draw(self, surface):
        pass

    def get_relative_pos(self, point):
        bb = self.get_bb()
        return point[0] - bb.left, point[1] - bb.top

    def is_in_relative_bb(self, point):
        return 0 <= point[0] < self.bb.width and 0 <= point[1] < self.bb.height

    def process_event(self, event):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event)
            if event.button == pygame.BUTTON_LEFT:
                self.on_left_button_release()
            elif event.button == pygame.BUTTON_RIGHT:
                self.on_right_button_release()
        elif event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                self.on_scroll_up()
            else:
                self.on_scoll_down()
        elif event.type == pygame.MOUSEMOTION:
            pos = self.get_relative_pos(event.pos)
            self.on_mouse_motion(pos, event.rel, event.buttons)
            if self.is_in_relative_bb(pos):
                self.on_mouse_motion_bb(pos, event.rel, event.buttons)
        elif event.type == pygame.KEYDOWN:
            self.on_key_press(event)

    def on_left_click(self, pos):
        pass

    def on_left_click_bb(self, pos):
        pass

    def on_left_button_release(self):
        pass

    def on_right_button_release(self):
        pass

    def on_right_click(self, pos):
        pass

    def on_scroll_up(self):
        pass

    def on_scoll_down(self):
        pass

    def on_mouse_motion(self, pos, motion, buttons):
        pass

    def on_mouse_motion_bb(self, pos, motion, buttons):
        pass

    def on_key_press(self, event):
        pass


__all__ = [Widget]
