import pandas as pd
import os

from project import Project, Task

ROOT = ROOT = os.path.dirname(os.path.abspath(__file__))

def loadProjectFromFile(filepath: str) -> None:
    projectName =  os.path.basename(filepath).split('.')[0]
    df = pd.read_excel(filepath)
    print(df)
    print('df finished')
    print()
    df.dropna(axis = 0, how = 'all', inplace = True)
    print(df)
    print('df finished')
    print()
    project = Project(projectName)
    if 'Descriptions' in df.columns:
        df.rename(columns={'Descriptions': 'Description'}, inplace=True)
    unProcesedRows = []

    for index, row in df.iterrows():
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

    project.calculateDates()
    project.calculateCriticalTasks()
    print(project)
    project.tablePrint()


def main():
    filename = 'Villa_ekte.xlsx'
    filepath = os.path.join(ROOT, filename)
    loadProjectFromFile(filepath=filepath)

if __name__ == '__main__':
    main()
