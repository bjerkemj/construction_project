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
    
    def test_calculate_dates(self):
        project = Project("Test Project")
        task1 = Task(type="Task", code="A1", description="Task 1", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Task 2", durations=[2, 3, 4], predecessors=[task1])
        task3 = Task(type="Task", code="A3", description="Task 3", durations=[1, 2, 3], predecessors=[task1])
        task4 = Task(type="Task", code="A4", description="Task 4", durations=[3, 4, 5], predecessors=[task2, task3])

        project.addTask(task1)
        project.addTask(task2)
        project.addTask(task3)
        project.addTask(task4)

        project.calculateDates(1)

        self.assertEqual(task1.getEarlyStartDate(), 0)
        self.assertEqual(task1.getLateStartDate(), 0)
        self.assertEqual(task4.getEarlyCompletionDate(), project.getEarlyProjectDuration())

    def test_add_gate(self):
        project = Project("Test Project")
        task1 = Task(type="Task", code="A1", description="Task 1", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Task 2", durations=[2, 3, 4], predecessors=[task1])
        task3 = Task(type="Task", code="A3", description="Task 3", durations=[1, 2, 3], predecessors=[task1])
        task4 = Task(type="Task", code="A4", description="Task 4", durations=[3, 4, 5], predecessors=[task2, task3])

        project.addTask(task1)
        project.addTask(task2)
        project.addTask(task3)
        project.addTask(task4)

        project.addGate("G1", "Gate 1", ["A1"])
        gate = project.getTask("G1")

        self.assertIsNotNone(gate)
        self.assertEqual(len(gate.getPredecessors()), 1)
        self.assertEqual(len(gate.getSuccessors()), 2)

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

        task1.clearSucessors()
        self.assertEqual(len(task1.successors), 0)

    def test_calculate_early_dates_no_predecessors(self):
        task1 = Task(type="Task", code="A1", description="Task 1", durations=[1, 2, 3])
        task1.calculateEarlyDates()

        self.assertEqual(task1.getEarlyStartDate(), 0)
        self.assertEqual(task1.getEarlyCompletionDate(), task1.randomDuration)

    def test_calculate_late_dates_no_successors(self):
        task1 = Task(type="Task", code="A1", description="Task 1", durations=[1, 2, 3])
        task1.calculateEarlyDates()
        task1.calculateLateDates()

        self.assertEqual(task1.getLateStartDate(), task1.getEarlyStartDate())
        self.assertEqual(task1.getLateCompletionDate(), task1.getEarlyCompletionDate())

    def test_is_critical(self):
        task1 = Task(type="Task", code="A1", description="Task 1", durations=[1, 2, 3])
        task2 = Task(type="Task", code="A2", description="Task 2", durations=[2, 3, 4])

        task1.earlyStartDate = 0
        task1.lateStartDate = 0

        task2.earlyStartDate = 3
        task2.lateStartDate = 4

        self.assertTrue(task1.isCritical())
        self.assertFalse(task2.isCritical())

if __name__ == '__main__':
    unittest.main()