import pygame

from render.widget.GanttTaskWidget import GanttTaskWidget
from render.widget.ScrollBarWidget import ScrollBarWidget
from render.widget.Widget import Widget


class GanttWidget(Widget):

    """
    This represents the Project in a Gantt chart. It is a vertical list of tasks. Each task is represented
    by a rectangle that spreads over the time when the task is being done.
    The GanttWidget is scrollable to be able to display every task.

    These are the fields of a GanttWidget :
    - project : the Project to display
    - bb : the bounding box of the Widget
    - is_earliest_graph : a boolean that indicates if the graph is the graph for the earliest possible times (True)
                          or the latest (False)
    - scroll_bar : the ScrollBarWidget of the Widget
    - task_widgets : the list of GanttTaskWidget that represent the tasks of the project
    - total_time : the total number of days of the project
    - number_of_time_marks : the number of time marks to display on the Gantt chart
    - font : the font used to display the time marks
    """

    def __init__(self, bb, project, is_earliest_graph):
        """
        Creates a GanttWidget
        :param bb: The bounding box of the Widget
        :param project: The Project to display
        :param is_earliest_graph: A boolean that indicates if the graph is the graph
                                  for the earliest possible times (True) or the latest (False)
        """
        super().__init__()
        self.project = project
        self.bb = bb
        self.is_earliest_graph = is_earliest_graph
        self.scroll_bar = ScrollBarWidget(self.get_bb, lambda: project.tasks_count*50 + 50)
        self.task_widgets = []
        self.total_time = self.project.project_task.earliest_start + self.project.project_task.estimated_time
        self.generate_widgets(self.project.beginning_task)
        self.number_of_time_marks = (project.tasks_count // 5) % 5 + 5
        self.font = pygame.font.SysFont("Arial", 16)

    def get_children(self):
        """
        Returns the children of the Widget that should be rendered
        :return: A generator returning the children of the Widget
        """
        yield from self.task_widgets
        yield self.scroll_bar

    def draw(self, surface):
        """
        Draws the Widget on the given Surface. It draws the time marks
        :param surface: The Surface on which the Widget should be drawn
        :return: None
        """
        surface.fill(0xffffff)
        for i in range(self.number_of_time_marks):
            time_mark = self.font.render(str((self.project.project_task.latest_start
                                         + self.project.project_task.estimated_time) * i / self.number_of_time_marks),
                                         False,
                                         0x000000)
            pos = 100 + (self.bb.width - 100) * i / self.number_of_time_marks
            surface.blit(time_mark, (pos - time_mark.get_width() / 2, 3))
            pygame.draw.line(surface, 0x000000, (pos, 20), (pos, self.bb.height))

    def reload(self):
        """
        Reloads the Widget. It removes all GanttTaskWidget and regenerates them
        :return: None
        """
        self.task_widgets.clear()
        self.total_time = self.project.project_task.earliest_start + self.project.project_task.estimated_time
        self.generate_widgets(self.project.beginning_task)
        self.number_of_time_marks = (self.project.tasks_count // 5) % 5 + 5

    def generate_widgets(self, first_task):
        """
        Generates the GanttTaskWidgets for the given task and its downstream tasks on the same line.
        This function is called recursively
        :param first_task: The first task of the line
        :return: None
        """
        self.task_widgets.append(GanttTaskWidget(first_task,
                                                 self.is_earliest_graph,
                                                 self.total_time,
                                                 self.bb,
                                                 self.scroll_bar.get_scroll_in_pixel))
        while len(first_task.downstream_tasks) == 1 and len(first_task.downstream_tasks[0].upstream_tasks) == 1:
            first_task = first_task.downstream_tasks[0]
            self.task_widgets.append(GanttTaskWidget(first_task,
                                     self.is_earliest_graph,
                                     self.total_time,
                                     self.bb,
                                     self.scroll_bar.get_scroll_in_pixel))
        for task in first_task.downstream_tasks:
            if task.upstream_tasks[0] != first_task:
                continue
            self.generate_widgets(task)

