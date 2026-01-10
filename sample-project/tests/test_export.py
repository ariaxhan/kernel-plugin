#!/usr/bin/env python3
"""
Unit tests for CSV export functionality
"""
import unittest
import csv
import os
import tempfile
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from taskmgr import TaskManager


class TestCSVExport(unittest.TestCase):
    def setUp(self):
        """Create a temporary task database for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_tasks.json")
        self.csv_path = os.path.join(self.temp_dir, "test_export.csv")
        self.tm = TaskManager(db_path=self.db_path)

    def tearDown(self):
        """Clean up temporary files"""
        for file in [self.db_path, self.csv_path]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)

    def test_export_empty_tasks(self):
        """Test exporting when there are no tasks"""
        # Capture output
        from io import StringIO
        import sys

        captured_output = StringIO()
        sys.stdout = captured_output

        self.tm.export_csv(self.csv_path)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("No tasks to export", output)
        self.assertFalse(os.path.exists(self.csv_path))

    def test_export_single_task(self):
        """Test exporting a single task"""
        self.tm.add_task("Test task", "high", "2026-01-15")
        self.tm.export_csv(self.csv_path)

        # Verify CSV file exists
        self.assertTrue(os.path.exists(self.csv_path))

        # Read and verify CSV content
        with open(self.csv_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["title"], "Test task")
            self.assertEqual(rows[0]["priority"], "high")
            self.assertEqual(rows[0]["due_date"], "2026-01-15")
            self.assertEqual(rows[0]["completed"], "False")

    def test_export_multiple_tasks(self):
        """Test exporting multiple tasks with different states"""
        self.tm.add_task("Task 1", "high", "2026-01-15")
        self.tm.add_task("Task 2", "medium")
        self.tm.add_task("Task 3", "low", "2026-01-20")
        self.tm.complete_task(1)

        self.tm.export_csv(self.csv_path)

        # Read and verify CSV content
        with open(self.csv_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            self.assertEqual(len(rows), 3)

            # Verify first task is completed
            self.assertEqual(rows[0]["completed"], "True")
            self.assertNotEqual(rows[0]["completed_at"], "")

            # Verify second task has no due date
            self.assertEqual(rows[1]["due_date"], "")
            self.assertEqual(rows[1]["completed"], "False")

    def test_csv_headers(self):
        """Test that CSV has correct headers"""
        self.tm.add_task("Test task")
        self.tm.export_csv(self.csv_path)

        with open(self.csv_path, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)

            expected_headers = [
                "id",
                "title",
                "priority",
                "due_date",
                "completed",
                "created_at",
                "completed_at",
            ]
            self.assertEqual(headers, expected_headers)

    def test_export_custom_filename(self):
        """Test exporting to a custom filename"""
        custom_path = os.path.join(self.temp_dir, "my_tasks.csv")
        self.tm.add_task("Test task")
        self.tm.export_csv(custom_path)

        self.assertTrue(os.path.exists(custom_path))

        # Clean up
        os.remove(custom_path)

    def test_csv_content_integrity(self):
        """Test that all task data is preserved in CSV"""
        self.tm.add_task('Special chars: comma, quote"', "high", "2026-01-15")
        self.tm.export_csv(self.csv_path)

        with open(self.csv_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            # Verify special characters are properly escaped
            self.assertEqual(rows[0]["title"], 'Special chars: comma, quote"')


if __name__ == "__main__":
    unittest.main()
