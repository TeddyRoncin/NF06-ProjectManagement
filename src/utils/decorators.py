"""
This file contains some useful decorators used in the project.
"""


def singleton(cls):
    """
    This decorator is used to make a class a singleton. It creates a field named instance
    and sets it to an instance of the class. The constructor should not take any arguments.
    :param cls: The class to make a singleton
    :return: The modified class
    """
    cls.instance = cls()
    return cls
