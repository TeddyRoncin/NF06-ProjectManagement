from time import time

from render.screen.HomeScreen import HomeScreen
from src.render.Window import Window
from render.screen.TestScreen import TestScreen


window = Window(TestScreen())
curr_time = time()
while True:
    window.tick()
