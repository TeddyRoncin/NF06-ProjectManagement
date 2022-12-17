from Project import Project
from render.Window import Window
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.ButtonWithConfirmationWidget import ButtonWithConfirmationWidget
from render.widget.EntryWidget import EntryWidget
from render.widget.LabelWidget import LabelWidget


class ProjectSettingsScreen(Screen):

    def __init__(self, project, last_screen):
        self.project = project
        self.last_screen = last_screen
        self.title_label = LabelWidget((0, 100), "Paramètres du projet", font_size=50, color=(0, 0, 0), bold=True)
        self.title_label.bb.x = (1920 - self.title_label.bb.width) / 2
        self.name_label = LabelWidget((655, 210), "Nom :", color=(0, 0, 0), font_size=24)
        self.name_entry = EntryWidget((655, 250), (200, 30), (200, 30), 100, False, default_content=self.project.name)
        self.name_warning_label = LabelWidget((655, 285), "", color=(255, 0, 0), font_size=20)
        self.description_label = LabelWidget((655, 340), "Description :", color=(0, 0, 0), font_size=24)
        self.description_entry = EntryWidget((655, 380), (600, 300), (600, 300), -1, True, default_content=self.project.description)
        self.description_warning_label = LabelWidget((655, 685), "", color=(255, 0, 0), font_size=20)
        self.save_button = ButtonWidget((655, 750), (300, 100), "Sauvegarder", self.on_save, font_size=30, bold=True)
        self.cancel_button = ButtonWidget((965, 750), (300, 100), "Annuler", lambda: Window.instance.set_screen(self.last_screen), font_size=30, bold=True)
        self.delete_button = ButtonWithConfirmationWidget((655, 860), (610, 100), "Supprimer", self.on_delete, font_size=30, bold=True)

    def get_widgets(self):
        yield self.title_label
        yield self.name_label
        yield self.name_entry
        yield self.name_warning_label
        yield self.description_label
        yield self.description_entry
        yield self.description_warning_label
        yield self.save_button
        yield self.cancel_button
        yield self.delete_button

    def on_save(self):
        is_valid = True
        if self.name_entry.get_content() == "":
            self.name_warning_label.set_text("Le nom ne peut pas être vide")
            is_valid = False
        else:
            self.name_warning_label.set_text("")
        if self.description_entry.get_content() == "":
            self.description_warning_label.set_text("La description ne peut pas être vide")
            is_valid = False
        else:
            self.description_warning_label.set_text("")
        if not is_valid:
            return
        self.project.name = self.name_entry.get_content()
        self.project.description = self.description_entry.get_content()
        Window.instance.set_screen(self.last_screen)

    def on_delete(self):
        # We need to import it here to avoid circular imports
        from HomeScreen import HomeScreen
        Project.delete_project(self.project)
        Window.instance.set_screen(HomeScreen())
