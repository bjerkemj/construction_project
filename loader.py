import pandas as pd
import os

ROOT = ROOT = os.path.dirname(os.path.abspath(__file__))

def loadProjectFromFile(filepath: str) -> None:
    print(filepath)
    projectName =  os.path.basename(filepath).split('.')[0]
    print(projectName)
    if filepath.split('.')[-1] == 'xlsx':
        df = pd.read_excel(filepath)
        print(df)
    else:
        print('Not excel file')


def main():
    filename = 'Warehouse.xlsx'
    filepath = os.path.join(ROOT, filename)
    loadProjectFromFile(filepath=filepath)

if __name__ == '__main__':
    main()
