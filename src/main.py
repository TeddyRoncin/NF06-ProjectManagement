from time import time

from Project import Project
from render.screen.HomeScreen import HomeScreen
from render.Window import Window


class Main:

    def __init__(self):
        self.projects, non_loadable = Project.load_projects()
        self.window = Window.instance
        self.window.set_screen(HomeScreen(self.projects))

    def run(self):
        while True:
            self.window.tick()


if __name__ == '__main__':
    Main().run()
