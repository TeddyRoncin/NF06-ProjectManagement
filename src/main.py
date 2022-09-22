from time import time

from src.render.Window import Window
from render.screen.TestScreen import TestScreen


window = Window(TestScreen())
curr_time = time()
while True:
    window.tick()
