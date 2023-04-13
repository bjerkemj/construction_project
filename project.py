

from typing import List


class Project:

    def __init__(self, name: str) -> None:
        self.name = name
        self.tasks = []

    def __repr__(self) -> str:
        tasksString = ''
        for task in self.tasks:
            tasksString += str(task)+'\n'
        return f'Project {self.name} contains the following tasks:\n{tasksString}'
    
class Task:
    
    def __init__(self, type: str, code: str, description: str, durations: tuple(int, int, int), predecessors: List) -> None:
        self.type = type
        self.code = code
        self.description = description
        self.durations = durations
        self.predecessors = predecessors

    def setType(self, type: str) -> None:
        self.type = type

    def setCode(self, code: str) -> None:
        self.code = code

    def setDescription(self, description: str) -> None:
        self.description = description

    def setDurations(self, durations: tuple(int, int, int)) -> None:
        self.durations = durations
    
    def setPredecessors(self, predecessors: List) -> None:
        self.predecessors = predecessors

    def getType(self) -> str:
        return self.type

    def getCode(self) -> str:  
        return self.code
    
    def getDescription(self) -> str:
        return self.description
    
    def getDurations(self) -> tuple(int, int, int):
        return self.durations
    
    def getPredecessors(self) -> List:
        return self.predecessors
    
    

    def __repr__(self) -> str:
        predeccoressorsString = ''
        for predecessor in self.predecessors:
            predeccoressorsString += predecessor.code + ' '
        return f'Task {self.code} {self.description} with predecessors {predeccoressorsString}'
        
    

def main():
    p = Project('testProject')
    print(p)

if __name__ == '__main__':
    main()
