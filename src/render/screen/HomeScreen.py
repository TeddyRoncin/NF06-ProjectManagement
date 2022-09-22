import pygame

from src.render.screen.Screen import Screen
from src.render.widget.ListWidget import ListWidget


class HomeScreen(Screen):

    def __init__(self):
        self.project_list = ListWidget(pygame.Rect(100, 100, 300, 50), ["Hello", "World", "Hope", "You're", "Fine"])

    def get_widgets(self):
        yield self.project_list
