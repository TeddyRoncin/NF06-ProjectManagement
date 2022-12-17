import os
import sys

from Task import Task
import json

from TaskStatus import TaskStatus
from utils import c_functions


class Project:
    """
    Represents a project. A project is a list of tasks, which should be completed before it is over.
    This class also contains a method to load all the projects.

    These are the fields of a Project :
    - name : The name of the project
    - file : The name of the file in which the project is stored
    - description : A description of the project
    - tasks_count : The number of tasks of the project
    - project_task : The task representing the end of the project. This task should be present on EVERY projects
    - beginning_task : The task representing the start of the project. This task should be present on EVERY projects
    """

    projects = []
    non_loadable_projects = []

    @staticmethod
    def load_projects():
        """
        Loads the projects. Each project is a JSON file stored in the data/projects directory
        Projects are stored in the projects list, and non-loadable projects are stored in the non_loadable_projects list
        :return: A tuple. The first value is the list of projects,
                 and the second value is the list of non-loadable projects
        """
        projects = []
        non_loadable_projects = []
        for project_file_name in os.listdir("data/projects"):
            try:
                print(f"Loading {project_file_name}")
                with open("data/projects/" + project_file_name, "r") as file:
                    project_data = json.load(file)
                    tasks = [Task(i) for i in range(len(project_data["tasks"]))]
                    for i, task in enumerate(project_data["tasks"]):
                        tasks[i].name = task["name"]
                        tasks[i].description = task["description"]
                        tasks[i].status = TaskStatus(int(task["status"]))
                        # Just sharing this random fact : there are actually many convention
                        # about using snake_case or camelCase in JSON, depending on what languages you use.
                        # You can find a list there :
                        # https://stackoverflow.com/questions/5543490/json-naming-convention-snake-case-camelcase-or-pascalcase#answer-25368854
                        tasks[i].estimated_time = task["estimated_time"]
                        for upstream_task in task["upstream"]:
                            print(f"\tLinking {tasks[i].id} and {upstream_task}")
                            tasks[i].add_upstream_task(tasks[upstream_task])
                    # The first task of the list is the beginning task, and the second one is the project task
                    projects.append(Project(project_data["name"],
                                            project_file_name,
                                            project_data["description"],
                                            tasks))
            except Exception as e:
                non_loadable_projects.append(project_file_name)
                print("An exception occurred while loading the project", file=sys.stderr)
                print(e, file=sys.stderr)
        Project.projects = projects
        Project.non_loadable_projects = non_loadable_projects
        return projects, non_loadable_projects

    @staticmethod
    def create_project(name, description, file_name):
        """
        Creates a new project. It also creates the JSON file
        :param name: The name of the project
        :param description: The description of the project
        :param file_name: The name of the file in which the project will be saved
        :return: The newly created project
        """
        project = Project(name, file_name, description)
        Project.projects.append(project)
        project.save()
        return project

    @staticmethod
    def delete_project(project):
        """
        Deletes a project. The deletion is permanent, because the file is also deleted.
        :param project: The project to delete
        :return: None
        """
        Project.projects.remove(project)
        os.remove("data/projects/" + project.file)

    def __init__(self, name, file, description="", tasks=None):
        """
        Represents a project. A project has a name, a file name, a description.
        A project must have at least 2 tasks :
            * the beginning_task (represents the beginning of the project)
            * the project_task (represents the project ending).
        """
        if tasks is None:
            tasks = [Task(0, name), Task(1, name)]
            # We need to link the 2 tasks
            tasks[1].add_upstream_task(tasks[0])
        self.name = name
        self.file = file
        self.description = description
        self.tasks = tasks
        self.tasks_count = len(self.tasks)
        self.project_task = tasks[1]
        self.beginning_task = tasks[0]

    def add_existing_task(self, task, upstream_tasks, create_new_branch):
        """
        Adds an existing task to the project
        This task should NOT have downstream or upstream tasks
        :param task: The task to add to the project
        :param upstream_tasks: The tasks that should be completed before this task
        :param create_new_branch: Whether we should create a new branch for this task
        :return: None
        """
        if create_new_branch:
            upstream_task = upstream_tasks.pop()
            downstream_task = upstream_task.downstream_tasks[0]
            # Then we have to create an intersection. The end of the intersection is the end of the branch
            if len(upstream_task.downstream_tasks) == 1:
                depth = 1
                last_downstream_task = upstream_task
                # We find the end of the branch
                # (it could be the last one, so we also check the if that it isn't to avoid running into an error)
                while len(downstream_task.downstream_tasks) != 0 and depth != 0:
                    # We are entering an intersection
                    if len(downstream_task.downstream_tasks) > 1:
                        depth += 1
                    last_downstream_task = downstream_task
                    downstream_task = downstream_task.downstream_tasks[0]
                    # We are leaving an intersection
                    if len(downstream_task.upstream_tasks) > 1:
                        depth -= 1
                # We don't want to go back if we left the loop because we arrived at the last task
                if len(downstream_task.downstream_tasks) != 0:
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
        # We add the task to the project
        self.tasks.append(task)
        self.tasks_count += 1
        # And finally we fix all the indices
        c_functions.fix_indices(self)

    def add_task(self, name, description, estimated_time, upstream_tasks, create_new_branch):
        """
        Adds a new task to the project.
        :param name: The name of the task
        :param description: The description of the task
        :param upstream_tasks: The upstream tasks of this task
        :param create_new_branch: Whether to create the task on a new branch
        :return: None
        """
        task = Task(name=name, description=description, estimated_time=estimated_time, id_=self.tasks_count)
        self.add_existing_task(task, upstream_tasks, create_new_branch)
        self.load()

    def remove_task(self, task):
        """
        Removes a task from the project.
        :param task: The task to remove
        :return: None
        """
        # This is a branch with a length of 1, so we simply need to remove it
        if len(task.upstream_tasks[0].downstream_tasks) > 1 and len(task.downstream_tasks[0].upstream_tasks) > 1:
            # The task cannot have multiple upstream and downstream tasks
            task.remove_upstream_task(task.upstream_tasks[0])
            task.downstream_tasks[0].remove_upstream_task(task)
        elif len(task.upstream_tasks) > 1:
            upstream_tasks = list(task.upstream_tasks)
            for upstream_task in upstream_tasks:
                print(upstream_task)
                print(upstream_task.downstream_tasks)
                task.remove_upstream_task(upstream_task)
                task.downstream_tasks[0].add_upstream_task(upstream_task)
                print(upstream_task.downstream_tasks)
            task.downstream_tasks[0].remove_upstream_task(task)
        elif len(task.downstream_tasks) > 1:
            downstream_tasks = list(task.downstream_tasks)
            for downstream_task in downstream_tasks:
                downstream_task.remove_upstream_task(task)
                downstream_task.add_upstream_task(task.upstream_tasks[0])
            task.remove_upstream_task(task.upstream_tasks[0])
        else:
            task.downstream_tasks[0].add_upstream_task(task.upstream_tasks[0])
            task.remove_upstream_task(task.upstream_tasks[0])
            task.downstream_tasks[0].remove_upstream_task(task)
        # We remove the task from the project
        self.tasks.pop(task.id)
        self.tasks_count -= 1
        # Then, we have to shift every task id greater than task.id by -1
        for i in range(task.id, len(self.tasks)):
            task.id -= 1
        # And finally we fix all the indices
        c_functions.fix_indices(self)
        self.load()

    def save(self):
        """
        Saves the project in a JSON file. The file is saved in data/projects/{self.file}
        :return: None
        """
        project_data = {"name": self.name,
                        "description": self.description,
                        "tasks": [
                            {"name": "", "description": "", "status": 0, "estimated_time": 0, "upstream": []} for _ in range(self.tasks_count)
                        ]}
        self.add_tasks_to_data(project_data, self.project_task)
        with open("data/projects/" + self.file, "w") as file:
            json.dump(project_data, file)

    def add_tasks_to_data(self, project_data, current_task):
        """
        Used by self.save() to add all tasks to the tasks list.
        It adds tasks info on a line to the project_data list.
        This is a recursive algorithm, which propagates upwards
        :param project_data: The dictionary containing info about the project.
        It's what is going to be saved in the JSON file.
        The project_data dictionary will be modified at the end of the function
        :param current_task: The task we should start this algorithm at
        :return: None
        """
        while len(current_task.upstream_tasks) == 1 and project_data["tasks"][current_task.id]["name"] == "":
            next_task = current_task.upstream_tasks[0]
            # Adding the current task to the next task's upstream_tasks list
            project_data["tasks"][current_task.id]["upstream"].append(next_task.id)
            self.load_task_to_data(project_data, current_task)
            current_task = next_task
        if project_data["tasks"][current_task.id]["name"] != "":
            return
        self.load_task_to_data(project_data, current_task)
        for task in current_task.upstream_tasks:
            project_data["tasks"][current_task.id]["upstream"].append(task.id)
            # We skip tasks that have already been managed
            if project_data["tasks"][task.id]["name"] == "":
                self.add_tasks_to_data(project_data, task)

    def load_task_to_data(self, project_data, task):
        """
        Loads a single task to the JSON data (excluding the upstream field)
        :param project_data: The dictionary representing the JSON root object
        :param task: The task to load
        :return: None
        """
        project_data["tasks"][task.id]["name"] = task.name
        project_data["tasks"][task.id]["description"] = task.description
        project_data["tasks"][task.id]["status"] = task.status.value
        project_data["tasks"][task.id]["estimated_time"] = task.estimated_time

    def load(self):
        """
        This function is called when the project is loaded.
        It sets the index value of each task
        :return: None
        """
        c_functions.fix_indices(self)
        c_functions.compute_earliest_start(self)
        c_functions.compute_latest_start(self)
        c_functions.identify_critical_tasks(self)
