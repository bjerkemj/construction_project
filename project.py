import random
from typing import List


class Project:

    def __init__(self, name: str) -> None:
        self.name = name
        self.tasks = []
        self.earlyProjectDuration = None
        self.lateProjectDuration = None

    def __repr__(self) -> str:
        tasksString = ''
        for task in self.tasks:
            tasksString += '\n\t' + str(task)
        return f'Project {self.name} contains the following tasks:{tasksString}'
    
    def tablePrint(self) -> None:
        # Formatting done with chatGPT
        print('Project: ' + self.name)
        lengths = [5, 5, 8, 11, 16, 11, 16, 8]
        formatted_strings = [ "Task".rjust(lengths[0]),
                            "Type".rjust(lengths[1]),
                            "Duration".rjust(lengths[2]),
                            "Early Start".rjust(lengths[3]),
                            "Early Completion".rjust(lengths[4]),
                            "Late Start".rjust(lengths[5]),
                            "Late Completion".rjust(lengths[6]),
                            "Critical".rjust(lengths[7]) ]
        print('\t'.join(formatted_strings))
        for task in self.tasks:
            print(task.tablePrint())
    
    def getTask(self, code: str) -> 'Task':
        for task in self.tasks:
            if task.code == code:
                return task
        return None
    
    def addTask(self, task: 'Task') -> None:
        self.tasks.append(task)
    
    def calculateEarlyDates(self, durationIndex: int = -1) -> None:
        taskCopy = self.tasks.copy()
        while len(taskCopy) > 0:
            for idx, task in enumerate(taskCopy):
                if all([predecessor not in taskCopy for predecessor in task.getPredecessors()]) or (len(task.getPredecessors()) == 0):
                    taskCopy.pop(idx).calculateEarlyDates(durationIndex)
                    break

    def calculateLateDates(self, durationIndex: int = -1) -> None:
        taskCopy = self.tasks.copy()[::-1]
        while len(taskCopy) > 0:
            for idx, task in enumerate(taskCopy):
                if all([successor not in taskCopy for successor in task.getSuccessors()]) or (len(task.getSuccessors()) == 0):
                    taskCopy.pop(idx).calculateLateDates(durationIndex)
                    break

    def calculateDates(self, durationIndex: int = -1) -> None:
        self.calculateEarlyDates(durationIndex)
        self.calculateLateDates(durationIndex)
        self.calculateProjectDurations()

    def calculateProjectDurations(self) -> None:
        self.calculateEarlyProjectDuration()
        self.calculateLateProjectDuration()

    def calculateEarlyProjectDuration(self) -> None:
        self.earlyProjectDuration = max([task.getEarlyCompletionDate() for task in self.tasks])

    def calculateLateProjectDuration(self) -> None:
        self.lateProjectDuration = max([task.getLateCompletionDate() for task in self.tasks])

    def getEarlyProjectDuration(self) -> float:
        return self.earlyProjectDuration
    
    def getLateProjectDuration(self) -> float:
        return self.lateProjectDuration

    def calculateCriticalTasks(self) -> None:
        for task in self.tasks:
            task.isCritical()
    
class Task:
    
    def __init__(self, type: str, code: str, description: str, durations: List[int], predecessors: List = []) -> None:
        self.type = type
        self.code = code
        self.description = description
        self.durations = durations
        self.predecessors = []
        self.successors = []
        for predecessor in predecessors:
            self.addPredecessor(predecessor)
        self.earlyStartDate = None
        self.earlyCompletionDate = None
        self.lateStartDate = None
        self.lateCompletionDate = None
        self.critical = False
        self.randomDuration = random.triangular(durations[0], durations[2], durations[1])
        self.duration = None

    def setType(self, type: str) -> None:
        self.type = type

    def setCode(self, code: str) -> None:
        self.code = code

    def setDescription(self, description: str) -> None:
        self.description = description

    def setDurations(self, durations: List[int]) -> None:
        self.durations = durations
    
    def setPredecessors(self, predecessors: List) -> None:
        self.predecessors = predecessors

    def getType(self) -> str:
        return self.type

    def getCode(self) -> str:  
        return self.code
    
    def getDescription(self) -> str:
        return self.description
    
    def getDurations(self) -> List[int]:
        return self.durations
    
    def getPredecessors(self) -> List:
        return self.predecessors
    
    def getSuccessors(self) -> List:
        return self.successors
    
    def addPredecessor(self, predecessor: 'Task') -> None:
        self.predecessors.append(predecessor)
        if self not in predecessor.successors:
            predecessor.addSucessor(self)
    
    def addSucessor(self, successor: 'Task') -> None:
        self.successors.append(successor)
        if self not in successor.predecessors:
            successor.addPredecessor(self)

    def getEarlyStartDate(self) -> int:
        return self.earlyStartDate
    
    def getEarlyCompletionDate(self) -> int:
        return self.earlyCompletionDate
    
    def getLateStartDate(self) -> int:
        return self.lateStartDate
    
    def getLateCompletionDate(self) -> int:        
        return self.lateCompletionDate
    
    def calculateEarlyDates(self, durationIndex: int = -1) -> None:
        if durationIndex == -1:
            self.duration = self.randomDuration
        else:
            self.duration = self.durations[durationIndex]
        if len(self.predecessors) == 0:
            self.earlyStartDate = 0
            self.earlyCompletionDate = self.duration
        else:
            self.earlyStartDate = max([predecessor.getEarlyCompletionDate() for predecessor in self.predecessors])
            self.earlyCompletionDate = self.earlyStartDate + self.duration


    def calculateLateDates(self, durationIndex: int = -1) -> None:
        if durationIndex == -1:
            self.duration = self.randomDuration
        else:
            self.duration = self.durations[durationIndex]
        if len(self.successors) == 0:
            self.lateCompletionDate = self.earlyCompletionDate
            self.lateStartDate = self.earlyCompletionDate - self.duration
        else:
            self.lateCompletionDate = min([successor.getLateStartDate() for successor in self.successors])
            self.lateStartDate = self.lateCompletionDate - self.duration

    def isCritical(self) -> bool:
        self.critical = (self.earlyStartDate == self.lateStartDate) and (self.earlyStartDate != None)
        return self.critical

    def __repr__(self) -> str:
        predeccoressorsString = ''
        for predecessor in self.predecessors:
            predeccoressorsString += predecessor.code + ' '
        return f'Task {self.code} ({self.description}) with predecessors: {predeccoressorsString}'
    
    def tablePrint(self) -> str:
        lengths = [5, 5, 8, 11, 16, 11, 16, 8]
        critical = str(self.critical)
        formatted_strings = [str(round(elem, 2)).rjust(lengths[i]) 
                            if isinstance(elem, (float, int)) 
                            else str(elem).rjust(lengths[i])
                            for i, elem in enumerate([self.code, self.type, self.randomDuration,
                                                    self.earlyStartDate, self.earlyCompletionDate,
                                                    self.lateStartDate, self.lateCompletionDate, critical])]
        return '\t'.join(formatted_strings)
    
        
    

def main():
    p = Project('testProject')
    print(p)

if __name__ == '__main__':
    main()
