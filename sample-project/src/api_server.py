#!/usr/bin/env python3
"""
Mock REST API server for TaskMgr sync
"""
from flask import Flask, request, jsonify
from datetime import datetime, timezone
from typing import Dict

app = Flask(__name__)

# In-memory storage (ephemeral)
tasks_db: Dict[int, Dict] = {}
next_id = 1


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Fetch all tasks"""
    return jsonify(list(tasks_db.values())), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task"""
    global next_id
    task_data = request.get_json()

    # Use client-provided ID if available, otherwise generate
    if "id" in task_data:
        task_id = task_data["id"]
        # Update next_id if needed
        if task_id >= next_id:
            next_id = task_id + 1
    else:
        task_id = next_id
        task_data["id"] = task_id
        next_id += 1

    task_data["synced_at"] = datetime.now(timezone.utc).isoformat()
    tasks_db[task_id] = task_data
    return jsonify(task_data), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update a task"""
    if task_id not in tasks_db:
        return jsonify({"error": "Task not found"}), 404

    task_data = request.get_json()
    task_data["id"] = task_id
    task_data["synced_at"] = datetime.now(timezone.utc).isoformat()
    tasks_db[task_id] = task_data
    return jsonify(task_data), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task"""
    if task_id not in tasks_db:
        return jsonify({"error": "Task not found"}), 404

    del tasks_db[task_id]
    return jsonify({"message": "Task deleted"}), 200


@app.route("/sync", methods=["GET"])
def sync():
    """Full sync endpoint"""
    return (
        jsonify(
            {
                "tasks": list(tasks_db.values()),
                "server_time": datetime.now(timezone.utc).isoformat(),
            }
        ),
        200,
    )


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return (
        jsonify({"status": "healthy", "tasks_count": len(tasks_db)}),
        200,
    )


if __name__ == "__main__":
    print("=" * 60)
    print("TaskMgr API Server")
    print("=" * 60)
    print("Running on: http://localhost:5000")
    print("Endpoints:")
    print("  GET    /tasks        - List all tasks")
    print("  POST   /tasks        - Create task")
    print("  PUT    /tasks/<id>   - Update task")
    print("  DELETE /tasks/<id>   - Delete task")
    print("  GET    /sync         - Full sync")
    print("  GET    /health       - Health check")
    print("=" * 60)
    print()
    app.run(debug=True, port=5000)
