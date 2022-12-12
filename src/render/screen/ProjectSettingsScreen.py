from Project import Project
from render.Window import Window
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.ButtonWithConfirmationWidget import ButtonWithConfirmationWidget
from render.widget.EntryWidget import EntryWidget


class ProjectSettingsScreen(Screen):

    def __init__(self, project, last_screen):
        self.project = project
        self.last_screen = last_screen
        self.name_entry = EntryWidget((100, 100), (100, 30), (100, 30), 100, False, default_content=self.project.name)
        self.description_entry = EntryWidget((100, 200), (300, 300), (300, 300), -1, True, default_content=self.project.description)
        self.save_button = ButtonWidget((100, 500), (100, 30), "Sauvegarder", self.on_save)
        self.delete_button = ButtonWithConfirmationWidget((100, 550), (100, 30), "Supprimer", self.on_delete)

    def get_widgets(self):
        yield self.name_entry
        yield self.description_entry
        yield self.save_button
        yield self.delete_button

    def on_save(self):
        self.project.name = self.name_entry.get_content()
        self.project.description = self.description_entry.get_content()
        Window.instance.set_screen(self.last_screen)

    def on_delete(self):
        # We need to import it here to avoid circular imports
        from HomeScreen import HomeScreen
        Project.delete_project(self.project)
        Window.instance.set_screen(HomeScreen())
