from render.screen.Screen import Screen
from render.widget.EntryWidget import EntryWidget
from render.widget.TestWidget import TestWidget


class TestScreen(Screen):

    def __init__(self):
        self.test_widget = TestWidget()
        self.entry = EntryWidget((200, 200), (100, 10), (200, 30), 50, True)

    def get_widgets(self):
        yield self.entry
        yield self.test_widget
