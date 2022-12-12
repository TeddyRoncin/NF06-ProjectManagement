import time

from render.widget.ButtonWidget import ButtonWidget


class ButtonWithConfirmationWidget(ButtonWidget):

    def __init__(self, pos, size, text, on_click):
        super().__init__(pos, size, text, on_click)
        self.last_click = 0
        self.confirmation_surface = self.font.render("Confirmer ?", True, (0, 0, 0))

    def draw(self, surface):
        if time.time() - self.last_click < 3:
            surface.fill((255, 0, 0))
            surface.blit(self.confirmation_surface,
                         ((self.bb.width - self.surface.get_width()) / 2,
                          (self.bb.height - self.surface.get_height()) / 2))
        else:
            super().draw(surface)

    def on_left_click_bb(self, pos):
        current_time = time.time()
        if current_time - self.last_click < 3:
            self.on_click()
            self.last_click = 0
        else:
            self.last_click = current_time
