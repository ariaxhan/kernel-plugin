#!/usr/bin/env python3
"""
Unit tests for database optimization functionality
"""
import unittest
import os
import tempfile
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from taskmgr import TaskManager


class TestDatabaseOptimization(unittest.TestCase):
    def setUp(self):
        """Create a temporary task database for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_tasks.json')
        self.tm = TaskManager(db_path=self.db_path)

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_optimize_empty_database(self):
        """Test optimizing when there are no tasks"""
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.tm.optimize_db()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("No tasks to optimize", output)

    def test_optimize_no_gaps(self):
        """Test optimizing when there are no gaps in IDs"""
        self.tm.add_task("Task 1")
        self.tm.add_task("Task 2")
        self.tm.add_task("Task 3")

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.tm.optimize_db()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("already optimized", output.lower())
        self.assertIn("No gaps found", output)

        # Verify IDs remain unchanged
        self.assertEqual([t['id'] for t in self.tm.tasks], [1, 2, 3])

    def test_optimize_with_gaps(self):
        """Test optimizing when there are gaps in IDs"""
        self.tm.add_task("Task 1")
        self.tm.add_task("Task 2")
        self.tm.add_task("Task 3")
        self.tm.add_task("Task 4")

        # Delete task 2, creating a gap
        self.tm.delete_task(2)

        # Verify gap exists
        ids_before = [t['id'] for t in self.tm.tasks]
        self.assertEqual(ids_before, [1, 3, 4])

        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.tm.optimize_db()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify optimization happened
        self.assertIn("Database optimized", output)
        self.assertIn("Old IDs: [1, 3, 4]", output)
        self.assertIn("New IDs: [1, 2, 3]", output)

        # Verify IDs are now sequential
        ids_after = [t['id'] for t in self.tm.tasks]
        self.assertEqual(ids_after, [1, 2, 3])

    def test_optimize_multiple_gaps(self):
        """Test optimizing with multiple gaps"""
        for i in range(1, 6):
            self.tm.add_task(f"Task {i}")

        # Delete tasks 2 and 4, creating two gaps
        self.tm.delete_task(2)
        self.tm.delete_task(4)

        # Verify gaps exist
        ids_before = [t['id'] for t in self.tm.tasks]
        self.assertEqual(ids_before, [1, 3, 5])

        self.tm.optimize_db()

        # Verify IDs are now sequential
        ids_after = [t['id'] for t in self.tm.tasks]
        self.assertEqual(ids_after, [1, 2, 3])

        # Verify task titles are preserved in order
        titles = [t['title'] for t in self.tm.tasks]
        self.assertEqual(titles, ["Task 1", "Task 3", "Task 5"])

    def test_optimize_preserves_task_data(self):
        """Test that optimization preserves all task data except ID"""
        self.tm.add_task("Task 1", "high", "2026-01-15")
        self.tm.add_task("Task 2", "medium", "2026-01-20")
        self.tm.add_task("Task 3", "low")

        # Complete task 1
        self.tm.complete_task(1)

        # Delete task 2
        self.tm.delete_task(2)

        # Store task data before optimization
        task_before = self.tm.tasks[1].copy()
        old_id = task_before['id']

        self.tm.optimize_db()

        # Find the same task after optimization (by title)
        task_after = next(t for t in self.tm.tasks if t['title'] == task_before['title'])

        # Verify all fields except ID are preserved
        self.assertEqual(task_after['title'], task_before['title'])
        self.assertEqual(task_after['priority'], task_before['priority'])
        self.assertEqual(task_after['due_date'], task_before['due_date'])
        self.assertEqual(task_after['completed'], task_before['completed'])
        self.assertEqual(task_after['created_at'], task_before['created_at'])

        # Verify ID changed
        self.assertNotEqual(task_after['id'], old_id)

    def test_optimize_maintains_sort_order(self):
        """Test that tasks maintain their order after optimization"""
        self.tm.add_task("First")
        self.tm.add_task("Second")
        self.tm.add_task("Third")
        self.tm.add_task("Fourth")

        # Delete middle tasks
        self.tm.delete_task(2)
        self.tm.delete_task(3)

        titles_before = [t['title'] for t in self.tm.tasks]

        self.tm.optimize_db()

        titles_after = [t['title'] for t in self.tm.tasks]

        # Verify order is maintained
        self.assertEqual(titles_before, titles_after)

    def test_optimize_persists_to_disk(self):
        """Test that optimized IDs are saved to disk"""
        self.tm.add_task("Task 1")
        self.tm.add_task("Task 2")
        self.tm.add_task("Task 3")
        self.tm.delete_task(2)

        self.tm.optimize_db()

        # Create a new TaskManager instance to load from disk
        tm2 = TaskManager(db_path=self.db_path)

        # Verify the optimized IDs were persisted
        ids = [t['id'] for t in tm2.tasks]
        self.assertEqual(ids, [1, 2])


if __name__ == '__main__':
    unittest.main()
