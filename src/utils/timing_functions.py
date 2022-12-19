"""
This file contains functions to compute the timings of the Animations.
"""


def cursor(t):
    """
    The function used by the cursor animation.
    It starts at 0, increases slower and slower to 1, and then goes down faster and faster to 0
    :param t: The fraction of the animation that has been completed. It should vary between 0 and 1
    :return: The completion of the effect at that time, 1 being fully completed and 0 being not completed at all
    """
    return - 4 * (t - 0.5) ** 2 + 1
