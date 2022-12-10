from Task import Task
from render.Window import Window
from render.screen.Screen import Screen
from render.widget.ButtonWidget import ButtonWidget
from render.widget.CheckboxWidget import CheckboxWidget
from render.widget.EntryWidget import EntryWidget
from render.widget.LabelWidget import LabelWidget
from render.widget.tasks_tree.add_task.AddTaskTreeWidget import AddTaskTreeWidget


class AddTaskScreen(Screen):

    def __init__(self, project, last_screen):
        self.project = project
        self.new_branch_checkbox = CheckboxWidget((200, 200), "Créer sur une nouvelle branche ?")
        self.new_branch_checkbox.enabled = False
        self.tree_widget = AddTaskTreeWidget((100, 100), project.beginning_task, self.new_branch_checkbox)
        self.name_widget = EntryWidget((10, 50), (100, 30), (100, 30), 100, False)
        self.error_widget = LabelWidget((10, 10), "")
        self.description_widget = EntryWidget((10, 90), (200, 100), (200, 100), -1, True)
        self.add_task_button = ButtonWidget((300, 300), (100, 25), "Ajouter", self.on_add_task)
        self.last_screen = last_screen

    def get_widgets(self):
        yield self.tree_widget
        yield self.name_widget
        yield self.error_widget
        yield self.description_widget
        yield self.add_task_button
        yield self.new_branch_checkbox

    def on_add_task(self):
        if self.name_widget.get_content() == "":
            self.error_widget.set_text("Le nom de la tâche ne peut pas être vide")
            return
        upstream_tasks = self.tree_widget.selected_tasks
        if len(upstream_tasks) == 0:
            self.error_widget.set_text("Vous devez sélectionner au moins une tâche parente")
            return
        create_new_branch = self.new_branch_checkbox.activated
        task = Task(name=self.name_widget.get_content(),
                    description=self.description_widget.get_content())
        self.project.tasks_count += 1
        if create_new_branch:
            upstream_task = upstream_tasks.pop()
            downstream_task = upstream_task.downstream_tasks[0]
            # Then we have to create an intersection. The end of the intersection is the end of the branch
            if len(upstream_task.downstream_tasks) == 1:
                depth = 1
                last_downstream_task = upstream_task
                # We find the end of the branch (it could be the last one, so we check the if it is to avoid running into an error)
                while len(downstream_task.downstream_tasks) != 0 and depth != 0:
                    # We are entering an intersection
                    if len(downstream_task.downstream_tasks) > 1:
                        depth += 1
                    last_downstream_task = downstream_task
                    downstream_task = downstream_task.downstream_tasks[0]
                    # We are leaving an intersection
                    if len(downstream_task.upstream_tasks) > 1:
                        depth -= 1
                downstream_task = last_downstream_task
            else:
                depth = 1
                # We find the end of the intersection
                while depth != 0:
                    # We are entering an intersection
                    if len(downstream_task.downstream_tasks) > 1:
                        depth += 1
                    downstream_task = downstream_task.downstream_tasks[0]
                    # We are leaving an intersection
                    if len(downstream_task.upstream_tasks) > 1:
                        depth -= 1
            downstream_task.add_upstream_task(task)
            # Finally, link task and upstream_task
            task.add_upstream_task(upstream_task)
        # We are not creating a new branch
        else:
            # Then there could be multiple downstream tasks
            if len(upstream_tasks) == 1:
                upstream_task = upstream_tasks.pop()
                downstream_tasks = list(upstream_task.downstream_tasks)
                task.add_upstream_task(upstream_task)
                for downstream_task in downstream_tasks:
                    downstream_task.replace_upstream_task(upstream_task, task)
            # Then there is only one downstream task
            else:
                downstream_task = next(iter(upstream_tasks)).downstream_tasks[0]
                # Copy tasks, because we are going to modify the list
                all_upstream_tasks = list(downstream_task.upstream_tasks)
                downstream_task.add_upstream_task(task)
                # We do it this way to be sure the upstream tasks are added in the right order
                for upstream_task in all_upstream_tasks:
                    if upstream_task in upstream_tasks:
                        downstream_task.remove_upstream_task(upstream_task)
                        task.add_upstream_task(upstream_task)
        Window.instance.set_screen(self.last_screen)

