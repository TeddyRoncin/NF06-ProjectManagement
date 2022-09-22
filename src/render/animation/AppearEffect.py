from src.render.animation.AnimationEffect import AnimationEffect


class AppearEffect(AnimationEffect):

    def __init__(self, timing_function, from_alpha=0, to_alpha=255):
        super().__init__(timing_function)
        self.from_alpha = from_alpha
        self.to_alpha = to_alpha

    def render(self, surface, progress):
        progress = self.timing_function(progress)
        surface.set_alpha((self.to_alpha - self.from_alpha) * progress + self.from_alpha)
