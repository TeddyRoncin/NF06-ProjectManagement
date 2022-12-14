class Screen:

    """
    This class is a base class, which means it should not be directly instanced.
    It contains general utility features and a default definition of the methods.

    Represents a set of components. These components should all be related.
    Only one screen is rendered at each frame.
    A screen can, for example, be the HomeScreen when the user launches the application,
    or the CreateProjectScreen used when the user wants to create a new project.
    """

    def get_widgets(self):
        """
        Get the list of widgets to display. It should not vary too much between each call
        :return: A generator returning all the widgets. The first to be yielded are the first to be rendered
        """
        yield from ()

    def update(self):
        """
        Update some values of the widgets if needed. This is called at every frame
        :return: None
        """
        pass

    def reload(self):
        """
        Loads or reload the screen.
        This is most useful when we come back to a screen, but this screen needs to be refreshed
        :return: None
        """
        pass
