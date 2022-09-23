import time


class Animation:

    """
    This class represents an animation. An animation is a manager of AnimationEffects.

    These are the fields of an Animation :
    - animation_effects : A list containing all the AnimationEffects needed to produce the animation
    - duration : The duration, in seconds, of a complete cycle of the animation.
                 Once the cycle is finished, the animation restarts.
    - progress : The progress between 0 and 1 of the animation. For example, if the animation lasts 2 seconds and
                 has been running for 1.5 seconds, then progress is 0.75.
    - last_frame : The timestamp of the last render. If the animation hasn't displayed any frame, then it equals 0.
                   During the first rendering, the animation starts with progress = 0,
                   and the last_frame is set to the current timestamp.
    - paused : Whether the animation is paused or not. Being paused means that the animation isn't running anymore,
               but is still being rendered. The progress of the animation is saved.
    - stopped : Whether the animation is stopped or not. Being stopped means that the animation isn't running
                nor being rendered anymore. The progress of the animation is reset to 0.
    """

    def __init__(self, animation_effects, duration):
        """
        Creates an Animation
        :param animation_effects: The AnimationEffects that should be rendered by the Animation
        :param duration: The duration in seconds of a cycle of the Animation.
                         Once this cycle is finished, the Animation starts again
        """
        self.animation_effects = animation_effects
        self.duration = duration
        self.progress = 0
        self.last_frame = 0
        self.paused = True
        self.stopped = True

    def start(self):
        """
        Starts or restart the Animation.
        Sets progress back to 0.
        After the Animation has been (re)launched, it will (re)start rendering and running.
        :return: None
        """
        self.progress = 0
        self.last_frame = 0
        self.paused = False
        self.stopped = False

    def pause(self):
        """
        Pauses the Animation.
        After the Animation has been paused, it will stop running, but continuing being rendered
        :return: None
        """
        self.paused = True

    def resume(self):
        """
        Resumes the Animation.
        This is the same as starting the Animation (see Animation.start()), but the progress is not reinitialized.
        :return: None
        """
        self.last_frame = 0
        self.paused = False

    def stop(self):
        """
        Stops the Animation.
        Resets the progress to 0.
        After the Animation has been stopped, it will not continue being rendered nor will it continue running
        :return: None
        """
        self.stopped = True
        self.progress = 0

    def render(self, surface):
        """
        Renders the animation
        :param surface: The surface to render the animation to
        :return: None
        """
        if self.stopped:
            return
        if not self.paused:
            current_time = time.time()
            if self.last_frame == 0:  # That means the animation has not started yet
                self.last_frame = current_time
            frame_duration = current_time - self.last_frame
            self.progress += frame_duration / self.duration
            # Set it back to a number between 0 and 1 if it goes over 1 (or over 2, 3, ... It can happen if the frame
            # was slow to render and the animation is fast)
            self.progress -= int(self.progress)
            self.last_frame = current_time
        self.render_no_update(surface)

    def render_no_update(self, surface):
        """
        Used to render the Animation without checking if the Animation is stopped or paused.
        It does not update the Animation (attributes stay unchanged), it only renders it in the current state it is in
        It calls the AnimationEffect.render() method of each AnimationEffect
        :param surface:
        :return:
        """
        for effect in self.animation_effects:
            effect.render(surface, self.progress)
