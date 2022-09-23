class AnimationEffect:

    """
    This class is a base class, which means it should not be directly instanced.
    It contains general utility features and a default definition of the methods.

    This represents an effect in an Animation.
    An AnimationEffect can be used to create a specific effect to a Surface.
    It can, for example, change its transparency over time, make it translate, ...
    These are the fields of an AnimationEffect :
    - timing_function : A mathematical function used to control the speed of the animation over time.
                        It should be defined between 0 and 1, and the outputed values represent how much
                        the effect is applied
                        For example, it permits having a fast animation at the beginning, then slow it,
                        and speed it at the end.
                        It can also permit inverting the effect.
    """

    def __init__(self, timing_function):
        """
        Creates an AnimationEffect
        :param timing_function: The function used to describe how much to apply the effect at each point of time
        """
        self.timing_function = timing_function

    def render(self, surface, progress):
        """
        Renders the AnimationEffect
        :param surface: The surface to render the AnimationEffect to
        :param progress: The progress of the Animation this AnimationEffect belongs to.
                         This parameter should not be used directly ; it should be modified by the function
                         of the field timing_function
        :return: None
        """
        pass
