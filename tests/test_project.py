import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from project import Project, Task

class TestProject(unittest.TestCase):
    def test_add_task(self):
        project = Project("Test Project")
        task1 = Task(type="Task", code="A1", description="Build a house!", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Build a garage!", durations=[1, 2, 3])

        project.addTask(task1)
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0], task1)

        project.addTask(task2)
        self.assertEqual(len(project.tasks), 2)

    def test_get_task(self):
        project = Project("Test Project")
        task1 = Task(type="Task", code="A1", description="Build a house!", durations=[1, 2, 5])
        task2 = Task(type="Task", code="A2", description="Build a garage!", durations=[1, 3, 4])
        task3 = Task(type="Task", code="A3", description="Build a fence!", durations=[1, 2, 3])

        project.addTask(task1)
        project.addTask(task2)
        project.addTask(task3)
        retrieved_task = project.getTask("A2")
        self.assertEqual(retrieved_task, task2)

class TestTask(unittest.TestCase):
    def test_add_predecessor(self):
        task1 = Task(type="Task", code="A1", description="Build a house!", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Build a garage!", durations=[1, 2, 3])
        task3 = Task(type="Task", code="A3", description="Build a fence!", durations=[1, 1, 1])

        task2.addPredecessor(task1)
        task2.addPredecessor(task3)
        self.assertEqual(len(task2.predecessors), 2)
        self.assertEqual(len(task1.successors), 1)
        self.assertEqual(len(task3.successors), 1)

    def test_add_successor(self):
        task1 = Task(type="Task", code="A1", description="Build a house!", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Build a garage", durations=[1, 1, 4])
        task3 = Task(type="Task", code="A3", description="Build a fence!", durations=[1, 1, 1])

        task1.addSucessor(task2)
        task1.addSucessor(task3)
        self.assertEqual(len(task1.successors), 2)
        self.assertEqual(len(task2.predecessors), 1)
        self.assertIn(task2, task1.successors)

    def test_clear_predeccessors(self):
        task1 = Task(type="Task", code="A1", description="Build a house!", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Build a garage", durations=[1, 1, 4])
        task3 = Task(type="Task", code="A3", description="Build a fence!", durations=[1, 1, 1])

        task1.addPredecessor(task2)
        task1.addPredecessor(task3)
        self.assertEqual(len(task1.predecessors), 2)

        task1.clearPredecessors()
        self.assertEqual(len(task1.predecessors), 0)

    def test_clear_successors(self):
        task1 = Task(type="Task", code="A1", description="Build a house!", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Build a garage", durations=[1, 1, 4])
        task3 = Task(type="Task", code="A3", description="Build a fence!", durations=[1, 1, 1])

        task1.addSucessor(task2)
        task1.addSucessor(task3)
        self.assertEqual(len(task1.successors), 2)

        task1.clearPredecessors()
        self.assertEqual(len(task1.successors), 0)

if __name__ == '__main__':
    unittest.main()