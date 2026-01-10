#!/usr/bin/env python3
"""
Unit tests for encryption functionality
"""
import unittest
import os
import tempfile
import json
import sys
from pathlib import Path
from io import StringIO

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cryptography.fernet import Fernet
from taskmgr import TaskManager


class TestEncryption(unittest.TestCase):
    def setUp(self):
        """Create a temporary task database for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_tasks.json")
        # Set encryption key for tests
        self.test_key = Fernet.generate_key().decode()
        os.environ["TASK_ENCRYPTION_KEY"] = self.test_key
        self.tm = TaskManager(db_path=self.db_path)

    def tearDown(self):
        """Clean up temporary files"""
        # Clean up
        if "TASK_ENCRYPTION_KEY" in os.environ:
            del os.environ["TASK_ENCRYPTION_KEY"]
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        # Clean up backup files
        backup_path = os.path.join(self.temp_dir, "test_tasks.json.backup")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rmdir(self.temp_dir)

    def test_add_confidential_task(self):
        """Test adding a confidential task"""
        self.tm.add_task("Secret project", "high", confidential=True)
        self.assertEqual(len(self.tm.tasks), 1)
        self.assertTrue(self.tm.tasks[0]["confidential"])
        self.assertEqual(self.tm.tasks[0]["title"], "Secret project")

    def test_confidential_task_encrypted_on_disk(self):
        """Test that confidential tasks are encrypted in JSON file"""
        self.tm.add_task("Secret", confidential=True)

        # Read raw JSON
        with open(self.db_path, "r") as f:
            raw_data = json.load(f)

        self.assertEqual(len(raw_data), 1)
        self.assertTrue(raw_data[0]["encrypted"])
        self.assertIn("data", raw_data[0])
        # Ensure title is NOT in plaintext
        raw_json_str = json.dumps(raw_data)
        self.assertNotIn("Secret", raw_json_str)

    def test_confidential_task_roundtrip(self):
        """Test encrypt-save-load-decrypt roundtrip"""
        self.tm.add_task("Confidential info", "high", "2026-01-20", confidential=True)
        original_task = self.tm.tasks[0].copy()

        # Reload from disk
        tm2 = TaskManager(db_path=self.db_path)
        loaded_task = tm2.tasks[0]

        self.assertEqual(loaded_task["title"], original_task["title"])
        self.assertEqual(loaded_task["priority"], original_task["priority"])
        self.assertEqual(loaded_task["due_date"], original_task["due_date"])
        self.assertTrue(loaded_task["confidential"])

    def test_mixed_confidential_and_normal(self):
        """Test handling both encrypted and plaintext tasks"""
        self.tm.add_task("Public task", "low")
        self.tm.add_task("Secret task", "high", confidential=True)

        self.assertEqual(len(self.tm.tasks), 2)
        self.assertFalse(self.tm.tasks[0].get("confidential", False))
        self.assertTrue(self.tm.tasks[1]["confidential"])

        # Read raw JSON
        with open(self.db_path, "r") as f:
            raw_data = json.load(f)

        # First task should be plaintext
        self.assertFalse(raw_data[0].get("encrypted", False))
        self.assertEqual(raw_data[0]["title"], "Public task")

        # Second task should be encrypted
        self.assertTrue(raw_data[1]["encrypted"])
        self.assertIn("data", raw_data[1])

    def test_decryption_failure_handling(self):
        """Test handling of corrupted encrypted data"""
        # Manually create corrupted encrypted task
        corrupted_data = [{"id": 1, "encrypted": True, "data": "invalid_base64!!!"}]
        with open(self.db_path, "w") as f:
            json.dump(corrupted_data, f)

        # Capture stderr
        captured_stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_stderr

        tm = TaskManager(db_path=self.db_path)

        sys.stderr = old_stderr
        stderr_output = captured_stderr.getvalue()

        self.assertEqual(len(tm.tasks), 1)
        self.assertEqual(tm.tasks[0]["title"], "[DECRYPTION FAILED]")
        self.assertIn("Error decrypting task", stderr_output)

    def test_missing_encryption_key_generates_warning(self):
        """Test that missing key generates temporary key with warning"""
        if "TASK_ENCRYPTION_KEY" in os.environ:
            del os.environ["TASK_ENCRYPTION_KEY"]

        # Capture stderr
        captured_stderr = StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured_stderr

        # Should auto-generate and warn
        tm = TaskManager(db_path=self.db_path)

        sys.stderr = old_stderr
        stderr_output = captured_stderr.getvalue()

        # Check for warning messages
        self.assertIn("Warning: TASK_ENCRYPTION_KEY not set", stderr_output)
        self.assertIn("Generated temporary key", stderr_output)

        # Key should still work for session
        tm.add_task("Test", confidential=True)
        self.assertEqual(len(tm.tasks), 1)


if __name__ == "__main__":
    unittest.main()
