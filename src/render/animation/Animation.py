import time


class Animation:

    def __init__(self, animation_effects, duration):
        self.animation_effects = animation_effects
        # The duration of 1 animation. Animations repeat over and over again
        self.duration = duration
        # The progress between 0 and 1 of the current animation
        self.progress = 0
        # Timestamp of the last frame that was rendered
        self.last_frame = 0
        # If the animation is paused, but should still be rendered
        self.paused = True
        # The animation should not continue working nor be rendered
        self.stopped = True

    # Start or restart the animation
    def start(self):
        self.progress = 0
        self.last_frame = 0
        self.paused = False
        self.stopped = False

    # Pause the animation, continues rendering
    def pause(self):
        self.paused = True

    # Resume the animation from the last frame before pausing
    def resume(self):
        self.last_frame = 0
        self.paused = False

    # Stop the animation, does not continue rendering
    def stop(self):
        self.stopped = True
        self.progress = 0

    def render(self, surface):
        if self.stopped:
            return
        if not self.paused:
            current_time = time.time()
            # That means the animation has not started yet
            if self.last_frame == 0:
                self.last_frame = current_time
            frame_duration = current_time - self.last_frame
            self.progress += frame_duration / self.duration
            # If it goes over 1 (or over 2, 3, ... if frame was slow to render and animation is fast)
            self.progress -= int(self.progress)
            self.last_frame = current_time
        self.render_no_update(surface)

    def render_no_update(self, surface):
        for effect in self.animation_effects:
            effect.render(surface, self.progress)
