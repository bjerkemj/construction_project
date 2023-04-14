import pandas as pd
import os

from project import Project, Task

ROOT = ROOT = os.path.dirname(os.path.abspath(__file__))

def loadProjectFromFile(filepath: str) -> None:
    print(filepath)
    projectName =  os.path.basename(filepath).split('.')[0]
    print(projectName)
    if filepath.split('.')[-1] == 'xlsx':
        df = pd.read_excel(filepath)
        print(df)
        print('df finished')
        print()
        project = Project(projectName)
        for index, row in df.iterrows():
            if pd.isnull(row['Predecessors']):
                predecessors = []
            else:
                predecessorsCodes = row['Predecessors'].split(',')
                predecessors = [project.getTask(code.strip()) for code in predecessorsCodes]
            if pd.isnull(row['Durations']):
                durations = [0,0,0]
            else:
                durations = [int(duration.replace('(', '').replace(')', '').strip()) for duration in row['Durations'].split(',')]
            if pd.isnull(row['Description']):
                row['Description'] = ''
            task = Task(type = row[0], code = row['Codes'].strip(), description = row['Description'], durations = durations, predecessors=predecessors)
            project.addTask(task)
    elif filepath.split('.')[-1] == 'tsv':
        

        print('Not excel file')

    project.calculateDates()
    project.calculateCriticalTasks()
    # print(project.tasks)

    print(project)

    project.tablePrint()


def main():
    filename = 'Warehouse.xlsx'
    filepath = os.path.join(ROOT, filename)
    loadProjectFromFile(filepath=filepath)

if __name__ == '__main__':
    main()
