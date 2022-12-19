"""
This file contains the math utilities for the project.
"""


def clamp(x, inf, sup):
    """
    Clamps a value between two values. Here are some example usages :
    >>> clamp(5, 0, 10)
    5
    >>> clamp(5, 0, 4)
    4
    >>> clamp(5, 6, 10)
    6
    :param x: The value to clamp
    :param inf: The lower bound
    :param sup: The upper bound
    :return: The clamped value
    """
    return max(inf, min(x, sup))
