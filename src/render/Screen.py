from enum import Enum

import pygame

from src.render.TestWidget import TestWidget
from src.render.EntryWidget import EntryWidget


class Screen(Enum):
    TEST_SCREEN=[
        #TestWidget(),
        EntryWidget((200, 200), (100, 10), (200, 30), 50, True),
    ]

__all__ = [Screen]

