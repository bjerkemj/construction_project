import os
import copy
import random
import warnings
from typing import List
from project import Project
from utils import loadProjectFromFile, ROOT

from sklearn import svm
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore", category=ConvergenceWarning)

class ProjectSimulator():
    def __init__(self, project: Project, r: float = 1.0) -> None:
        self.project = project
        self.r = r
        self.project.calculateDates(durationIndex= 1)
        self.expectedDuration = project.getLateProjectDuration()

    def simulateNProjects(self, n: int = 1000, gateCode: str = '') -> List[int]:
        projectDurationList = []
        if gateCode:
            beforeGateTimes = []
        for _ in range(n):
            projectCopy = copy.deepcopy(self.project)
            projectCopy.drawRandomSample(r=self.r)
            projectDurationList.append(projectCopy.getLateProjectDuration())
            if gateCode:
                beforeGateTimes.append(projectCopy.getEarlyCompletionDatesBeforeTask(gateCode))
        return (projectDurationList, beforeGateTimes) if gateCode else projectDurationList
    
    def classifyProjects(self, projectDurationsList) -> List[str]:
        classifications = []
        for projectDuration in projectDurationsList:
            if projectDuration < self.expectedDuration * 1.05:
                classifications.append(2)
            elif projectDuration < self.expectedDuration * 1.15:
                classifications.append(1)
            else:
                classifications.append(0)
        return classifications
    
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
        widths = [15, 15, 15, 15, 15, 15, 15, 15, 15]
        separator = '-' * (10 + sum(widths))

        print(separator)
        print('|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|'.format(
            'Min Duration', 'Max Duration', 'Mean Duration', 'Std Dev', 'Lower Decile', 'Upper Decile', 'Successful', 'Accepted', 'Fail'))
        print(separator)

        print('|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15.2f}|{:^15}|{:^15}|{:^15}|'.format(
            *statistics))
        print(separator)

    def logisticRegression(self, data, categories):
        X_train, X_test, y_train, y_test = train_test_split(data, categories, test_size=0.2, random_state=42)

        model = LogisticRegression()

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy}")

    def decisionTree(self, data, categories):
        X_train, X_test, y_train, y_test = train_test_split(data, categories, test_size=0.2, random_state=42)

        model = DecisionTreeClassifier(random_state=42)

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy}")

    def SVC(self, data, categories):
        X_train, X_test, y_train, y_test = train_test_split(data, categories, test_size=0.2, random_state=42)

        model = svm.SVC()

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        print(f"Accuracy: {accuracy}")

    def linearRegression(self, data, durations):
        X_train, X_test, y_train, y_test = train_test_split(data, durations, test_size=0.2, random_state=42)

        model = LinearRegression()

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = mean_squared_error(y_test, predictions)
        print(f"Accuracy: {accuracy}")

    def decisionTreeRegressor(self, data, durations):
        X_train, X_test, y_train, y_test = train_test_split(data, durations, test_size=0.2, random_state=42)

        model = DecisionTreeRegressor(random_state=42)

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = mean_squared_error(y_test, predictions)
        print(f"Accuracy: {accuracy}")

    def randomForest(self, data, durations):
        X_train, X_test, y_train, y_test = train_test_split(data, durations, test_size=0.2, random_state=42)

        model = RandomForestRegressor(random_state=42)

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = mean_squared_error(y_test, predictions)
        print(f"Accuracy: {accuracy}")

    @staticmethod
    def task_4():
        print('RUNNING TASK 4')
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
        print('RUNNING TASK 5')
        print('CLASSIFICATION')
        random.seed(1)
        numSamples = 2000
        filename = 'Villa.xlsx'
        filepath = os.path.join(ROOT, 'resources', filename)
        project = loadProjectFromFile(filepath=filepath)
        project.addGate("GATE1", "Milestone", ["H.2", "H.3"])
        project.calculateDates()
        project.calculateCriticalTasks()

        rs = [.8, 1.0, 1.2, 1.4]
        classif = []
        beforeTimes = []
        for r in rs:
            projectSimulator = ProjectSimulator(project=project, r=r)
            projectDurationsList, beforeGateTimes = projectSimulator.simulateNProjects(n=int(numSamples/len(rs)), gateCode='GATE1')
            classifications = projectSimulator.classifyProjects(projectDurationsList=projectDurationsList)
            classif += classifications
            beforeTimes += beforeGateTimes

        print(f'Running logistic regression on {numSamples} samples and gate placed before tasks H.2 and H.3')
        projectSimulator.logisticRegression(beforeTimes, classif)
        print()

        print(f'Running decision tree on {numSamples} samples and gate placed before tasks H.2 and H.3')
        projectSimulator.decisionTree(beforeTimes, classif)
        print()

        print(f'Running support vector classification on {numSamples} samples and gate placed before tasks H.2 and H.3')
        projectSimulator.SVC(beforeTimes, classif)


    @staticmethod 
    def task_6():
        print('REGRESSION')
        random.seed(1)
        numSamples = 2000
        filename = 'Villa.xlsx'
        filepath = os.path.join(ROOT, 'resources', filename)
        project = loadProjectFromFile(filepath=filepath)
        project.addGate("GATE1", "Milestone", ["H.2", "H.3"])
        project.calculateDates()
        project.calculateCriticalTasks()

        rs = [.8, 1.0, 1.2, 1.4]
        durations = []
        beforeTimes = []
        for r in rs:
            projectSimulator = ProjectSimulator(project=project, r=r)
            projectDurationsList, beforeGateTimes = projectSimulator.simulateNProjects(n=int(numSamples/len(rs)), gateCode='GATE1')
            durations += projectDurationsList
            beforeTimes += beforeGateTimes

        print(f'Running logistic regression on {numSamples} samples and gate placed before tasks H.2 and H.3')
        projectSimulator.linearRegression(beforeTimes, durations)
        print()

        print(f'Running decision tree on {numSamples} samples and gate placed before tasks H.2 and H.3')
        projectSimulator.decisionTreeRegressor(beforeTimes, durations)
        print()

        print(f'Running random forrest regression on {numSamples} samples and gate placed before tasks H.2 and H.3')
        projectSimulator.randomForest(beforeTimes, durations)
        
def main():
    ProjectSimulator.task_4()
    ProjectSimulator.task_5()
    ProjectSimulator.task_6()

if __name__ == '__main__':
    main()