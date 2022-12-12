from Project import Project
from render.Window import Window
from render.screen.ProjectScreen import ProjectScreen
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.EntryWidget import EntryWidget


class CreateProjectScreen(Screen):

    def __init__(self):
        self.name_entry = EntryWidget((100, 100), (100, 30), (100, 30), 100, False)
        self.description_entry = EntryWidget((100, 200), (300, 300), (300, 300), -1, True)
        self.file_name_entry = EntryWidget((250, 100), (100, 30), (100, 30), 100, False)
        self.create_button = ButtonWidget((100, 500), (100, 30), "Créer", self.on_create)

    def get_widgets(self):
        yield self.name_entry
        yield self.description_entry
        yield self.file_name_entry
        yield self.create_button

    def on_create(self):
        if self.file_name_entry.get_content() == "":
            return
        project = Project.create_project(self.name_entry.get_content(),
                                         self.description_entry.get_content(),
                                         self.file_name_entry.get_content())
        Window.instance.set_screen(ProjectScreen(project))
