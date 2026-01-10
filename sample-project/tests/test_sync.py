#!/usr/bin/env python3
"""
Unit tests for API sync functionality
"""
import unittest
import os
import tempfile
import json
import sys
from pathlib import Path
from unittest.mock import patch, Mock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cryptography.fernet import Fernet
import requests
from taskmgr import TaskManager


class TestAPISync(unittest.TestCase):
    def setUp(self):
        """Create a temporary task database for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_tasks.json")
        os.environ["TASKMGR_API_URL"] = "http://localhost:5000"
        # Set encryption key for tests
        self.test_key = Fernet.generate_key().decode()
        os.environ["TASK_ENCRYPTION_KEY"] = self.test_key

    def tearDown(self):
        """Clean up temporary files"""
        # Clean up
        if "TASKMGR_API_URL" in os.environ:
            del os.environ["TASKMGR_API_URL"]
        if "TASK_ENCRYPTION_KEY" in os.environ:
            del os.environ["TASK_ENCRYPTION_KEY"]
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        # Clean up backup files
        backup_path = os.path.join(self.temp_dir, "test_tasks.json.backup")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rmdir(self.temp_dir)

    @patch("taskmgr.requests.get")
    def test_sync_pull_on_startup(self, mock_get):
        """Test that tasks are pulled from server on startup"""
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"tasks": [{"id": 1, "title": "Server task", "priority": "high", "completed": False, "created_at": "2026-01-10T00:00:00+00:00"}], "server_time": "2026-01-10T00:00:00+00:00"},
        )

        tm = TaskManager(db_path=self.db_path)

        mock_get.assert_called_once()
        self.assertEqual(len(tm.tasks), 1)
        self.assertEqual(tm.tasks[0]["title"], "Server task")

    @patch("taskmgr.requests.get")
    def test_offline_mode_on_server_unavailable(self, mock_get):
        """Test graceful degradation when server is unavailable"""
        mock_get.side_effect = requests.RequestException("Connection refused")

        # Should not crash, just warn
        tm = TaskManager(db_path=self.db_path)
        self.assertEqual(len(tm.tasks), 0)

    @patch("taskmgr.requests.get")
    @patch("taskmgr.requests.post")
    def test_sync_push_on_add(self, mock_post, mock_get):
        """Test that new tasks are pushed to server"""
        mock_get.return_value = Mock(status_code=200, json=lambda: {"tasks": [], "server_time": "2026-01-10T00:00:00+00:00"})
        mock_post.return_value = Mock(status_code=201)

        tm = TaskManager(db_path=self.db_path)
        tm.add_task("New task", "high")

        mock_post.assert_called_once()
        call_args = mock_post.call_args
        # Verify the task data was sent
        self.assertIn("json", call_args.kwargs)
        task_data = call_args.kwargs["json"]
        self.assertEqual(task_data["title"], "New task")

    @patch("taskmgr.requests.get")
    @patch("taskmgr.requests.put")
    def test_sync_push_on_complete(self, mock_put, mock_get):
        """Test that task updates are pushed to server"""
        mock_get.return_value = Mock(status_code=200, json=lambda: {"tasks": [], "server_time": "2026-01-10T00:00:00+00:00"})
        mock_put.return_value = Mock(status_code=200)

        tm = TaskManager(db_path=self.db_path, enable_sync=False)
        tm.add_task("Task to complete")
        tm.sync_enabled = True
        tm.complete_task(1)

        mock_put.assert_called_once()
        # Verify PUT request was made to correct endpoint
        call_args = mock_put.call_args
        self.assertIn("/tasks/1", call_args.args[0])

    @patch("taskmgr.requests.get")
    @patch("taskmgr.requests.delete")
    def test_sync_push_on_delete(self, mock_delete, mock_get):
        """Test that task deletions are pushed to server"""
        mock_get.return_value = Mock(status_code=200, json=lambda: {"tasks": [], "server_time": "2026-01-10T00:00:00+00:00"})
        mock_delete.return_value = Mock(status_code=200)

        tm = TaskManager(db_path=self.db_path, enable_sync=False)
        tm.add_task("Task to delete")
        tm.sync_enabled = True
        tm.delete_task(1)

        mock_delete.assert_called_once()
        # Verify DELETE request was made to correct endpoint
        call_args = mock_delete.call_args
        self.assertIn("/tasks/1", call_args.args[0])

    @patch("taskmgr.requests.get")
    @patch("taskmgr.requests.post")
    def test_local_save_on_sync_failure(self, mock_post, mock_get):
        """Test that tasks are saved locally even if sync fails"""
        mock_get.return_value = Mock(status_code=200, json=lambda: {"tasks": [], "server_time": "2026-01-10T00:00:00+00:00"})
        mock_post.side_effect = requests.RequestException("Network error")

        tm = TaskManager(db_path=self.db_path)
        tm.add_task("Test task")

        # Task should be in memory
        self.assertEqual(len(tm.tasks), 1)
        self.assertEqual(tm.tasks[0]["title"], "Test task")

        # Task should be saved to disk
        with open(self.db_path, "r") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test task")


if __name__ == "__main__":
    unittest.main()
