import os
from typing import List
from project import Project
import copy
from loader import loadProjectFromFile, ROOT

class ProjectSimulator():


    def __init__(self, project: Project, r: float = 1.0) -> None:
        self.project = project
        self.r = r
        self.project.calculateDates(durationIndex= 1)
        self.expectedDuration = project.getLateProjectDuration()

    def simulateNProjects(self, n: int = 1000) -> List[int]:
        projectDurationList = []
        for i in range(n):
            projectCopy = copy.deepcopy(self.project)
            projectCopy.drawRandomSample(r=self.r)
            projectDurationList.append(projectCopy.getLateProjectDuration())
        return projectDurationList
    
    def calculateStatistics(self, projectDurationsList: List[float]) -> List[float]:
        projectDurationsList.sort()
        minProjectDuration = min(projectDurationsList)
        maxProjectDuration = max(projectDurationsList)
        meanProjectDuration = sum(projectDurationsList)/len(projectDurationsList)
        standardDeviation = (sum([(projectDuration - meanProjectDuration)**2 for projectDuration in projectDurationsList])/len(projectDurationsList))**0.5
        lowerDecile = projectDurationsList[int(len(projectDurationsList)*0.1)]
        upperDecile = projectDurationsList[int(len(projectDurationsList)*0.9)]
        return [minProjectDuration, maxProjectDuration, meanProjectDuration, standardDeviation, lowerDecile, upperDecile]
    
    def calculateCategoryStatistics(self, projectDurationsList: List[float]) -> List[float]:
        pass
    
    def printStatistics(self, statistics):
        # Define column widths and separator character
        widths = [20, 20, 20, 20, 20, 20]
        separator = '-' * sum(widths)

        # Print header row
        print(separator)
        print('|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|'.format(
            'Min Duration', 'Max Duration', 'Mean Duration', 'Std Deviation', 'Lower Decile', 'Upper Decile'))
        print(separator)

        # Print data rows
        print('|{:^20.2f}|{:^20.2f}|{:^20.2f}|{:^20.2f}|{:^20.2f}|{:^20.2f}|'.format(
            *statistics))
        print(separator)
    


def main():
    filename = 'Villa.xlsx'
    filepath = os.path.join(ROOT, 'resources', filename)
    project = loadProjectFromFile(filepath=filepath)

    rs = [.8, 1.0, 1.2, 1.4]
    for r in rs:
        projectSimulator = ProjectSimulator(project=project, r=r)
        projectDurationsList = projectSimulator.simulateNProjects(n=1000)
        statistics = projectSimulator.calculateStatistics(projectDurationsList=projectDurationsList)
        print(f'For r = {r}, the statistics are:')
        projectSimulator.printStatistics(statistics)
        


if __name__ == '__main__':
    main()