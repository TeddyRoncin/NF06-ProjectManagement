"""
The entry point of the application. It initializes everything and contains the main loop.
"""

from Project import Project
from render.screen.HomeScreen import HomeScreen
from render.Window import Window

if __name__ == '__main__':
    Project.load_projects()
    window = Window.instance
    window.set_screen(HomeScreen())
    while True:
        window.tick()
