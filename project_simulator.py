import os
from typing import List
from project import Project
import copy
from utils import loadProjectFromFile, ROOT
import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


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
        successful = len([duration for duration in projectDurationsList if duration < self.expectedDuration * 1.05])
        acceptable = len([duration for duration in projectDurationsList if duration < self.expectedDuration * 1.15 ]) - successful
        failed = len(projectDurationsList) - successful - acceptable
        return [minProjectDuration, maxProjectDuration, meanProjectDuration, standardDeviation, lowerDecile, upperDecile, successful, acceptable, failed]

    def printStatistics(self, statistics):
        # Define column widths and separator character
        widths = [15, 15, 15, 15, 15, 15, 15, 15, 15]
        separator = '-' * (10 + sum(widths))

        # Print header row
        print(separator)
        print('|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|'.format(
            'Min Duration', 'Max Duration', 'Mean Duration', 'Std Dev', 'Lower Decile', 'Upper Decile', 'Successful', 'Accepted', 'Fail'))
        print(separator)

        # Print data rows
        print('|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15}|{:^15}|{:^15}|'.format(
            *statistics))
        print(separator)

    def logisticRegression(self, data, categories):
        encoded_categories = [0 if category == 'A' else 1 for category in categories]

        X_train, X_test, y_train, y_test = train_test_split(data, encoded_categories, test_size=0.2, random_state=42)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy}")

    @staticmethod
    def task_4():
        random.seed(1)
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

    @staticmethod 
    def task_5():
        random.seed(1)
        filename = 'Warehouse.xlsx'
        filepath = os.path.join(ROOT, 'resources', filename)
        project = loadProjectFromFile(filepath=filepath)
        project.addGate("G1", "Milestone", predecessors=[project.getTask("F"), project.getTask("D")], successors=[project.getTask("G")])
        project.calculateDates()
        project.calculateCriticalTasks()
        project.sortTasks()
        project.tablePrint()


        
def main():
    ProjectSimulator.task_5()

if __name__ == '__main__':
    main()