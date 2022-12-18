from Project import Project
from render.Window import Window
from render.screen.ProjectScreen import ProjectScreen
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.EntryWidget import EntryWidget
from render.widget.LabelWidget import LabelWidget


class CreateProjectScreen(Screen):

    """
    This is the screen that is used to create a new project.

    These are the fields of a CreateProjectScreen:
    - title_label: The LabelWidget that shows the title of the Screen.
    - name_label: The LabelWidget that indicates the purpose of the following EntryWidget.
    - name_entry: The EntryWidget that is used to enter the name of the project.
    - name_warning_label: The LabelWidget that shows a warning if the name is invalid.
    - description_label: The LabelWidget that indicates the purpose of the following EntryWidget.
    - description_entry: The EntryWidget that is used to enter the description of the project.
    - description_warning_label: The LabelWidget that shows a warning if the description is invalid.
    - file_name_label: The LabelWidget that indicates the purpose of the following EntryWidget.
    - file_name_entry: The EntryWidget that is used to enter the name of the file that will be used to save the project.
    - file_name_warning_label: The LabelWidget that shows a warning if the file name is invalid.
    - create_button: The ButtonWidget that is used to create the project.
    - go_back_button: The ButtonWidget that is used to go back to the HomeScreen.
    """

    def __init__(self):
        """
        Creates a CreateProjectScreen
        """
        self.title_label = LabelWidget((0, 100), "Créer un projet", font_size=50, color=(0, 0, 0), bold=True)
        self.title_label.bb.x = (1920 - self.title_label.bb.width) / 2
        self.name_label = LabelWidget((500, 210), "Nom :", color=(0, 0, 0), font_size=24)
        self.name_entry = EntryWidget((500, 250), (200, 30), (300, 30), 100, False)
        self.name_warning_label = LabelWidget((500, 285), "", color=(255, 0, 0), font_size=20)
        self.description_label = LabelWidget((500, 340), "Description :", color=(0, 0, 0), font_size=24)
        self.description_entry = EntryWidget((500, 380), (600, 300), (600, 300), -1, True)
        self.description_warning_label = LabelWidget((500, 685), "", color=(255, 0, 0), font_size=20)
        self.file_name_label = LabelWidget((500, 740), "Nom du fichier de sauvegarde :", color=(0, 0, 0), font_size=24)
        self.file_name_entry = EntryWidget((500, 780), (200, 30), (300, 30), 100, False)
        self.file_name_warning_label = LabelWidget((500, 815), "", color=(255, 0, 0), font_size=20)
        self.create_button = ButtonWidget((810, 900), (300, 100), "Créer", self.on_create, font_size=30, bold=True)
        self.go_back_button = ButtonWidget((20, 20), (150, 70), "Retour", self.on_going_back, font_size=30, bold=True)

    def get_widgets(self):
        """
        Returns the list of widgets we should be displaying on this frame.
        :return: A generator returning the widgets that should be displayed.
        """
        yield self.title_label
        yield self.name_label
        yield self.name_entry
        yield self.name_warning_label
        yield self.description_label
        yield self.description_entry
        yield self.description_warning_label
        yield self.file_name_label
        yield self.file_name_entry
        yield self.file_name_warning_label
        yield self.create_button
        yield self.go_back_button

    def on_create(self):
        """
        Callback from self.create_button. It is called when the user confirms the creation of the Project.
        It may not create it if at least one of the fields is invalid.
        If the Project is created, the user is redirected to the ProjectScreen of the newly created project.
        :return: None
        """
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
        if self.file_name_entry.get_content() == "":
            self.file_name_warning_label.set_text("Le nom du fichier ne peut pas être vide")
            is_valid = False
        else:
            self.file_name_warning_label.set_text("")
        if not is_valid:
            return
        project = Project.create_project(self.name_entry.get_content(),
                                         self.description_entry.get_content(),
                                         self.file_name_entry.get_content())
        Window.instance.set_screen(ProjectScreen(project))

    @staticmethod
    def on_going_back():
        """
        Callback from self.go_back_button. It is called when the user wants to cancel the creation of the Project.
        It redirects the user to the HomeScreen.
        :return: None
        """
        from render.screen.HomeScreen import HomeScreen
        Window.instance.set_screen(HomeScreen())
