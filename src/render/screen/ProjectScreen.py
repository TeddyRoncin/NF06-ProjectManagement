from render.screen.Screen import Screen
from render.widget.GanttWidget import GanttWidget


class ProjectScreen(Screen):

    def __init__(self, project):
        """self.gantt_widgets = [project.project_task]
        task = project.project_task
        pos = (50, 50)
        while len(task.upstream_tasks):
            task = task.upstream_tasks[0]
            self.gantt_widgets.append(GanttWidget())"""
        self.gantt_widget = GanttWidget((100, 100), project.beginning_task)

    def get_widgets(self):
        yield self.gantt_widget
