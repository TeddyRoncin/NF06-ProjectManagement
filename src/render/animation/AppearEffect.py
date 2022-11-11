from render.animation.AnimationEffect import AnimationEffect


class AppearEffect(AnimationEffect):

    """
    An AnimationEffect that changes the opacity of a surface over time.

    These are the fields of an AppearEffect :
    - from_alpha : the minimum alpha value, displayed when field timing_function
                   (see AnimationEffect.timing_function) returns 0
    - to_alpha : the maximum alpha value, displayed when field timing_function
                 (see AnimationEffect.timing_function) returns 1
    """

    def __init__(self, timing_function, from_alpha=0, to_alpha=255):
        """
        Creates an AppearEffect
        :param timing_function: The timing function of the effect. It controls the alpha filter that will be applied
                                to the surface over time. It should be defined between 0 and 1.
                                When it is evaluated to 0, the alpha value is set to from_alpha ;
                                when it is evaluated to 1, the alpha value is set to to_alpha
        :param from_alpha: The alpha value (between 0 and 255) that will be applied to the Surface
                           when timing_function is evaluated to 0
        :param to_alpha: The alpha value (between 0 and 255) that will be applied to the Surface
                           when timing_function is evaluated to 1
        """
        super().__init__(timing_function)
        self.from_alpha = from_alpha
        self.to_alpha = to_alpha

    def render(self, surface, progress):
        """
        Renders the effect
        :param surface: The surface the effect should be rendered to
        :param progress: The progress of the Animation containing this AppearEffect
        :return: None
        """
        progress = self.timing_function(progress)
        surface.set_alpha((self.to_alpha - self.from_alpha) * progress + self.from_alpha)
