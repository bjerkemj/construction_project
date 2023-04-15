from project import Project, Task

class ProjectSimulator():


    def __init__(self, project: Project, r: float = 1.0) -> None:
        self.project = project
        self.r = r

    