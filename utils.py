# Tinus F Alsos and Johan Bjerkem

import os
import random
import pandas as pd
from project import Project, Task

ROOT = os.path.dirname(os.path.abspath(__file__))

def loadProjectFromFile(filepath: str) -> Project:
    projectName =  os.path.basename(filepath).split('.')[0]
    df = pd.read_excel(filepath)
    df.dropna(axis = 0, how = 'all', inplace = True)
    project = Project(projectName)
    if 'Descriptions' in df.columns:
        df.rename(columns={'Descriptions': 'Description'}, inplace=True)
    unProcesedRows = []

    for _, row in df.iterrows():
        if unProcesedRows:
            oldRow = row
            for row in unProcesedRows.copy():
                predecessorsCodes = row['Predecessors'].split(',')
                predecessors = [project.getTask(code.strip()) for code in predecessorsCodes]
                if None in predecessors:
                    continue
                unProcesedRows.remove(row)
                if pd.isnull(row['Durations']):
                    durations = [0,0,0]
                else:
                    durations = [int(duration.replace('(', '').replace(')', '').strip()) for duration in row['Durations'].split(',')]
                if pd.isnull(row['Description']):
                    row['Description'] = ''
                task = Task(type = row[0], code = row['Codes'].strip(), description = row['Description'], durations = durations, predecessors=predecessors)
                project.addTask(task)
            row = oldRow
        if pd.isnull(row['Predecessors']):
            predecessors = []
        else:
            predecessorsCodes = row['Predecessors'].split(',')
            predecessors = [project.getTask(code.strip()) for code in predecessorsCodes]
            if None in predecessors:
                unProcesedRows.append(row)
                continue
        if pd.isnull(row['Durations']):
            durations = [0,0,0]
        else:
            durations = [int(duration.replace('(', '').replace(')', '').strip()) for duration in row['Durations'].split(',')]
        if pd.isnull(row['Description']):
            row['Description'] = ''
        task = Task(type = row[0], code = row['Codes'].strip(), description = row['Description'], durations = durations, predecessors=predecessors)
        project.addTask(task)

    return project

def saveProjectToFile(project: Project, filename: str) -> None:
    folderPath = os.path.join(ROOT, 'solutions')
    if not os.path.exists(folderPath):
        os.mkdir(folderPath)
    columns=['Codes', 'Descriptions', 'Minimum Duration', 'Expected Duration', 'Maximum Duration', 'Predecessors', 'Successors', 'Early Start Date', 'Early Completion Date', 'Late Start Date', 'Late Completion Date', 'Critical']
    df = pd.DataFrame(columns = columns)
    for idx, task in enumerate(project.tasks):
        df.loc[idx] = [task.code, task.description, task.durations[0], task.durations[1], task.durations[2], ', '.join([predecessor.code for predecessor in task.predecessors]), ', '.join([successor.code for successor in task.successors]), task.earlyStartDate, task.earlyCompletionDate, task.lateStartDate, task.lateCompletionDate, task.critical]

    df.to_excel(os.path.join(folderPath, filename), index=False)

def createPNGfromDotFile(filename: str) -> None:
        os.system(f"dot -Tpng {filename}.dot > {filename}.png")

def generateDotFileFromTree(project: Project, filename: str) -> None:
    allText = getDotTextFromTree(project)
    with open(filename + '.dot', 'w') as file:
        file.write(
            "digraph g {\nfontname=\"Helvetica,Arial,sans-serif\"\nnode [fontname=\"Helvetica,Arial,sans-serif\" filledcolor = \"white\" label = \"\" style = \"filled\" shape = \"circle\" ]\nedge [fontname=\"Helvetica,Arial,sans-serif\"]\ngraph [fontsize=30 labelloc=\"t\" label=\"\" splines=true overlap=false rankdir = \"LR\"];\nratio = auto;\n")
        
        file.write(allText)
        file.write("\n}")

def getDotTextFromTree(project: Project) -> str:
    string = ""
    for task in project.tasks:
        string = addNode(string, task)
    return string

def addNode(string: str, task: Task) -> str:
        string += f'\"{task.code.replace(".", "")}\" [style = \"filled\" label = \"{task.code.replace(".", "")}\"];\n'
        for predecessor in task.predecessors:
            string += f'"{str(predecessor.code).replace(".", "")}\" -> \"{str(task.code).replace(".", "")}";\n'
        return string

def deleteAllPngs():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith('.png'):
            os.remove(file)


def deleteAllDots():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith('.dot'):
            os.remove(file)

def main():
    random.seed(1)
    filename = 'Villa.xlsx'
    filepath = os.path.join(ROOT, 'resources', filename)
    project = loadProjectFromFile(filepath=filepath)
    project.addGate("GATE1", "Milestone", ["H.2", "H.3"])
    project.calculateDates()
    project.calculateCriticalTasks()
    project.sortTasks()
    project.tablePrint()

    saveProjectToFile(project=project, filename=filename)
    # generateDotFileFromTree(project=project, filename='Villa')
    # createPNGfromDotFile(filename='Villa')

if __name__ == '__main__':
    main()
