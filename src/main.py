from time import time

from Project import Project
from render.screen.HomeScreen import HomeScreen
from render.Window import Window


class Main:

    def __init__(self):
        self.projects, non_loadable = Project.load_projects()
        print("projects loaded !")
        self.window = Window.instance
        self.window.set_screen(HomeScreen(self.projects))
        print(Window.instance)

    def run(self):
        while True:
            self.window.tick()


if __name__ == '__main__':
    Main().run()
