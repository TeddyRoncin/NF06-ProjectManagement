from time import time

from src.render.Window import Window
from src.render.Screen import Screen


window = Window()
window.set_screen(Screen.TEST_SCREEN)
curr_time = time()
while True:
    window.tick()
