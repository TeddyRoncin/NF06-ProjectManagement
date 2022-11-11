def init_class(cls):
    cls._clsinit()
    return cls


def singleton(cls):
    cls.instance = cls()
    return cls
