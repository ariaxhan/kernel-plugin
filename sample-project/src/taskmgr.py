#!/usr/bin/env python3
"""
TaskMgr - A simple task management CLI
"""
import csv
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional

from cryptography.fernet import Fernet
import requests


class TaskManager:
    VALID_PRIORITIES = {"high", "medium", "low"}
    PRIORITY_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}

    def __init__(self, db_path: str = "tasks.json", enable_sync: bool = True):
        self.db_path = Path(db_path)
        self.fernet = self._get_encryption_key()
        self.api_url = os.environ.get("TASKMGR_API_URL", "http://localhost:5000")
        self.sync_enabled = enable_sync
        self.tasks: List[Dict] = self._load_tasks()

        # Pull from server on startup
        if self.sync_enabled:
            self._sync_pull()

    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file, decrypting as needed"""
        if self.db_path.exists():
            try:
                with open(self.db_path, "r") as f:
                    raw_tasks = json.load(f)

                # Decrypt encrypted tasks
                tasks = []
                for task in raw_tasks:
                    if task.get("encrypted"):
                        tasks.append(self._decrypt_task(task))
                    else:
                        tasks.append(task)
                return tasks
            except json.JSONDecodeError as e:
                # Backup corrupt file
                corrupt_path = self.db_path.with_suffix(".json.corrupt")
                shutil.copy2(self.db_path, corrupt_path)
                print(
                    f"Warning: Corrupt JSON file backed up to {corrupt_path}",
                    file=sys.stderr,
                )
                print(f"Error: {e}", file=sys.stderr)
                return []
            except IOError as e:
                print(f"Error reading tasks file: {e}", file=sys.stderr)
                return []
        return []

    def _save_tasks(self):
        """Save tasks to JSON file with automatic backup, encrypting confidential ones"""
        backup_path = self.db_path.with_suffix(".json.backup")
        temp_path = self.db_path.with_suffix(".json.tmp")

        try:
            # Encrypt confidential tasks before saving
            tasks_to_save = []
            for task in self.tasks:
                if task.get("confidential"):
                    tasks_to_save.append(self._encrypt_task(task))
                else:
                    tasks_to_save.append(task)

            # Create backup if file exists
            if self.db_path.exists():
                shutil.copy2(self.db_path, backup_path)

            # Save to temporary file first
            with open(temp_path, "w") as f:
                json.dump(tasks_to_save, f, indent=2)

            # Atomic rename
            temp_path.replace(self.db_path)

        except (IOError, OSError) as e:
            print(f"Error saving tasks: {e}", file=sys.stderr)
            # Cleanup temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            # Restore from backup if save failed
            if backup_path.exists() and not self.db_path.exists():
                shutil.copy2(backup_path, self.db_path)
            raise

    def _format_date(self, date_str: Optional[str]) -> str:
        """Format ISO date string to 'Jan 15, 2026' format"""
        if not date_str:
            return ""
        try:
            # Parse ISO format date (YYYY-MM-DD)
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%b %d, %Y")
        except (ValueError, AttributeError):
            return date_str

    def _get_encryption_key(self) -> Fernet:
        """Get or generate encryption key from environment"""
        key = os.environ.get("TASK_ENCRYPTION_KEY")
        if not key:
            # Auto-generate and warn
            key = Fernet.generate_key().decode()
            print(
                "Warning: TASK_ENCRYPTION_KEY not set. Generated temporary key.",
                file=sys.stderr,
            )
            print(
                "Confidential tasks will only be accessible in this session.",
                file=sys.stderr,
            )
        return Fernet(key.encode() if isinstance(key, str) else key)

    def _encrypt_task(self, task: Dict) -> Dict:
        """Encrypt task data, returning encrypted wrapper"""
        task_json = json.dumps(task)
        encrypted_data = self.fernet.encrypt(task_json.encode()).decode()
        return {"id": task["id"], "encrypted": True, "data": encrypted_data}

    def _decrypt_task(self, encrypted_wrapper: Dict) -> Dict:
        """Decrypt task from encrypted wrapper"""
        try:
            decrypted_bytes = self.fernet.decrypt(
                encrypted_wrapper["data"].encode()
            )
            return json.loads(decrypted_bytes.decode())
        except Exception as e:
            print(
                f"Error decrypting task {encrypted_wrapper['id']}: {e}",
                file=sys.stderr,
            )
            # Return placeholder for corrupted encrypted tasks
            return {
                "id": encrypted_wrapper["id"],
                "title": "[DECRYPTION FAILED]",
                "priority": "medium",
                "completed": False,
                "created_at": "",
                "confidential": True,
            }

    def _sync_pull(self):
        """Pull tasks from server on startup"""
        try:
            response = requests.get(f"{self.api_url}/sync", timeout=5)
            response.raise_for_status()
            server_data = response.json()

            # Merge strategy: Server tasks overwrite local if present
            server_tasks = server_data.get("tasks", [])

            if server_tasks:
                print(
                    f"Synced {len(server_tasks)} tasks from server",
                    file=sys.stderr,
                )
                self.tasks = server_tasks
                self._save_tasks()

        except requests.RequestException as e:
            print(f"Warning: Could not sync with server: {e}", file=sys.stderr)
            print("Operating in offline mode", file=sys.stderr)

    def _sync_push(self, operation: str, task_data: Dict):
        """Push changes to server"""
        if not self.sync_enabled:
            return

        try:
            if operation == "create":
                response = requests.post(
                    f"{self.api_url}/tasks", json=task_data, timeout=5
                )
            elif operation == "update":
                response = requests.put(
                    f"{self.api_url}/tasks/{task_data['id']}",
                    json=task_data,
                    timeout=5,
                )
            elif operation == "delete":
                response = requests.delete(
                    f"{self.api_url}/tasks/{task_data['id']}", timeout=5
                )

            response.raise_for_status()

        except requests.RequestException as e:
            print(f"Warning: Sync failed: {e}", file=sys.stderr)
            print("Changes saved locally only", file=sys.stderr)

    def add_task(
        self,
        title: str,
        priority: str = "medium",
        due_date: Optional[str] = None,
        confidential: bool = False,
    ):
        """Add a new task"""
        # Validate priority
        if priority not in self.VALID_PRIORITIES:
            print(
                f"Error: Invalid priority '{priority}'. Must be one of: {', '.join(sorted(self.VALID_PRIORITIES))}",
                file=sys.stderr,
            )
            sys.exit(1)

        # Generate next ID based on max existing ID
        next_id = max([t["id"] for t in self.tasks], default=0) + 1

        task = {
            "id": next_id,
            "title": title,
            "priority": priority,
            "due_date": due_date,
            "completed": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "confidential": confidential,
        }
        self.tasks.append(task)
        self._save_tasks()

        # Sync to server
        self._sync_push("create", task)

        print(f"Task added: {title}")

    def list_tasks(self, show_completed: bool = False):
        """List all tasks"""
        filtered = self.tasks if show_completed else [t for t in self.tasks if not t["completed"]]

        if not filtered:
            print("No tasks found.")
            return

        for task in filtered:
            status = "✓" if task["completed"] else "○"
            priority_icon = self.PRIORITY_ICONS.get(task["priority"], "⚪")
            due_date_formatted = self._format_date(task.get("due_date"))
            due = f" (due: {due_date_formatted})" if due_date_formatted else ""
            print(f"{status} [{task['id']}] {priority_icon} {task['title']}{due}")

    def complete_task(self, task_id: int):
        """Mark a task as completed"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now(timezone.utc).isoformat()
                self._save_tasks()

                # Sync to server
                self._sync_push("update", task)

                print(f"Task {task_id} completed!")
                return
        print(f"Task {task_id} not found.")

    def delete_task(self, task_id: int):
        """Delete a task"""
        # Find task before deleting for sync
        deleted = [t for t in self.tasks if t["id"] == task_id]

        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self._save_tasks()

        # Sync to server
        if deleted:
            self._sync_push("delete", deleted[0])

        print(f"Task {task_id} deleted.")

    def stats(self):
        """Show task statistics"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t["completed"]])
        pending = total - completed

        print(f"\n📊 Task Statistics:")
        print(f"   Total: {total}")
        print(f"   Completed: {completed}")
        print(f"   Pending: {pending}")

        if total > 0:
            print(f"   Completion rate: {(completed/total)*100:.1f}%")

    def export_csv(self, filename: str = "tasks_export.csv"):
        """Export tasks to CSV file"""
        if not self.tasks:
            print("No tasks to export.")
            return

        try:
            with open(filename, "w", newline="") as csvfile:
                fieldnames = [
                    "id",
                    "title",
                    "priority",
                    "due_date",
                    "completed",
                    "created_at",
                    "completed_at",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for task in self.tasks:
                    row = {
                        "id": task["id"],
                        "title": task["title"],
                        "priority": task["priority"],
                        "due_date": task.get("due_date", ""),
                        "completed": task["completed"],
                        "created_at": task["created_at"],
                        "completed_at": task.get("completed_at", ""),
                    }
                    writer.writerow(row)

            print(f"Tasks exported to {filename} ({len(self.tasks)} tasks)")
        except IOError as e:
            print(f"Error exporting to CSV: {e}", file=sys.stderr)
            sys.exit(1)

    def optimize_db(self):
        """Reindex task IDs to remove gaps"""
        if not self.tasks:
            print("No tasks to optimize.")
            return

        # Sort tasks by current ID to maintain order
        self.tasks.sort(key=lambda x: x["id"])

        # Track old IDs for reporting
        old_ids = [task["id"] for task in self.tasks]
        gaps_found = False

        # Reindex sequentially
        for new_id, task in enumerate(self.tasks, start=1):
            if task["id"] != new_id:
                gaps_found = True
            task["id"] = new_id

        self._save_tasks()

        if gaps_found:
            print(f"Database optimized: Reindexed {len(self.tasks)} tasks")
            print(f"Old IDs: {old_ids}")
            print(f"New IDs: {[task['id'] for task in self.tasks]}")
        else:
            print(f"Database already optimized: No gaps found in {len(self.tasks)} tasks")


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: taskmgr.py [add|list|complete|delete|stats|export|optimize] [args...]")
        sys.exit(1)

    tm = TaskManager()
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: taskmgr.py add <title> [priority] [due_date] [--confidential]")
            sys.exit(1)
        title = sys.argv[2]
        priority = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else "medium"
        due_date = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else None
        confidential = "--confidential" in sys.argv
        tm.add_task(title, priority, due_date, confidential)

    elif command == "list":
        show_completed = "--all" in sys.argv
        tm.list_tasks(show_completed)

    elif command == "complete":
        if len(sys.argv) < 3:
            print("Usage: taskmgr.py complete <task_id>")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: Task ID must be a number, got '{sys.argv[2]}'", file=sys.stderr)
            sys.exit(1)
        tm.complete_task(task_id)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: taskmgr.py delete <task_id>")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: Task ID must be a number, got '{sys.argv[2]}'", file=sys.stderr)
            sys.exit(1)
        tm.delete_task(task_id)

    elif command == "stats":
        tm.stats()

    elif command == "export":
        filename = sys.argv[2] if len(sys.argv) > 2 else "tasks_export.csv"
        tm.export_csv(filename)

    elif command == "optimize":
        tm.optimize_db()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
