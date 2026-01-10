# TaskMgr - Task Management CLI

A secure, cloud-synced command-line task manager with encryption support and JSON storage.

## Features

- **Core Task Management**: Add, list, complete, and delete tasks
- **Priority Levels**: High, medium, low with visual indicators
- **Due Dates**: Track deadlines with formatted display
- **Statistics**: Completion tracking and analytics
- **CSV Export**: Export tasks to CSV format
- **Database Optimization**: Reindex task IDs to remove gaps
- **🔐 Encryption**: End-to-end encryption for confidential tasks
- **☁️ REST API Sync**: Auto-sync tasks with remote server
- **⚡ Development Pipeline**: Automated code quality checks

## Installation

```bash
# Install dependencies
pip install -r requirements-dev.txt
```

## Quick Start

### Basic Usage

```bash
# Add a task
python src/taskmgr.py add "Buy groceries" high 2026-01-15

# List tasks
python src/taskmgr.py list

# Complete a task
python src/taskmgr.py complete 1

# View statistics
python src/taskmgr.py stats

# Export to CSV
python src/taskmgr.py export [filename]  # Default: tasks_export.csv

# Optimize database
python src/taskmgr.py optimize  # Reindex task IDs to remove gaps
```

## Security & Encryption

### Setting Up Encryption

TaskMgr uses Fernet (AES-128-CBC + HMAC) for encrypting confidential tasks.

**Generate and set encryption key:**

```bash
# Generate a new encryption key
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Set environment variable (add to ~/.bashrc or ~/.zshrc for persistence)
export TASK_ENCRYPTION_KEY="your-generated-key-here"
```

**⚠️ SECURITY WARNINGS:**
- **Never commit encryption keys to version control**
- Store keys in environment variables or secure key management systems
- If you lose the encryption key, encrypted tasks cannot be recovered
- Auto-generated keys are temporary (session-only)

### Using Confidential Tasks

```bash
# Add a confidential task (will be encrypted on disk)
python src/taskmgr.py add "Company merger plans" high --confidential

# View encrypted task (requires TASK_ENCRYPTION_KEY)
python src/taskmgr.py list
```

**How it works:**
- Confidential tasks are encrypted before saving to `tasks.json`
- Entire task object (title, priority, dates) is encrypted
- Stored format: `{"id": 1, "encrypted": true, "data": "gAAAAAB..."}`
- Automatically decrypted when loaded (if key is available)
- Failed decryption shows `[DECRYPTION FAILED]` placeholder

## REST API Sync

### Setting Up Sync

TaskMgr can automatically sync tasks with a remote REST API server.

**Start the mock API server:**

```bash
# In a separate terminal
python src/api_server.py

# Server starts at http://localhost:5000
```

**Configure sync URL (optional):**

```bash
# Default is http://localhost:5000
export TASKMGR_API_URL="http://your-server.com:5000"
```

### Sync Behavior

- **Startup Pull**: Tasks are pulled from server when TaskMgr starts
- **Auto-Push**: Changes (add/complete/delete) are pushed immediately
- **Offline Mode**: Works gracefully when server is unavailable
- **Conflict Resolution**: Server-wins strategy on startup pull

**Examples:**

```bash
# Add task (auto-syncs to server)
python src/taskmgr.py add "Deploy new feature" high

# Complete task (syncs update to server)
python src/taskmgr.py complete 1

# Server unavailable? No problem - saves locally with warning
# Warning: Sync failed: Connection refused
# Changes saved locally only
```

### API Endpoints

The mock server provides:
- `GET /tasks` - List all tasks
- `POST /tasks` - Create task
- `PUT /tasks/<id>` - Update task
- `DELETE /tasks/<id>` - Delete task
- `GET /sync` - Full sync with server timestamp
- `GET /health` - Health check

## Development

### Code Quality Pipeline

TaskMgr uses Claude Code hooks for automated quality checks:

**Auto-executed on every file write:**
1. **Black** - Code formatting (--line-length 100)
2. **Pylint** - Code quality linting (fails if score < 7.0)
3. **Mypy** - Static type checking (warnings only)
4. **Tests** - Auto-run when test files modified

### Running Tests

```bash
# Run all tests
python3 -m unittest discover -s tests -p "test_*.py" -v

# Or use the Claude Code command
# (In Claude Code CLI, type: /test-all)

# Expected test modules:
# - test_encryption.py (6 tests)
# - test_sync.py (6 tests)
# - test_export.py (6 tests)
# - test_optimize.py (8 tests)
# Total: 26+ tests
```

### Commit Message Generation

```bash
# Use Claude Code command to generate conventional commit messages
# (In Claude Code CLI, type: /generate-commit)
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TASK_ENCRYPTION_KEY` | Fernet encryption key for confidential tasks | Auto-generated (temporary) |
| `TASKMGR_API_URL` | REST API server URL for sync | `http://localhost:5000` |

## File Structure

```
sample-project/
├── src/
│   ├── taskmgr.py          # Main task manager
│   └── api_server.py       # Mock REST API server
├── tests/
│   ├── test_encryption.py  # Encryption tests
│   ├── test_sync.py        # API sync tests
│   ├── test_export.py      # CSV export tests
│   └── test_optimize.py    # Database optimization tests
├── .claude/
│   ├── commands/           # Custom Claude Code commands
│   └── settings.json       # Pipeline hooks configuration
├── tasks.json              # Task database (auto-created)
└── requirements-dev.txt    # Python dependencies
```

## Data Format

**Plaintext task:**
```json
{
  "id": 1,
  "title": "Public task",
  "priority": "high",
  "due_date": "2026-01-15",
  "completed": false,
  "created_at": "2026-01-10T12:00:00+00:00",
  "confidential": false
}
```

**Encrypted task (on disk):**
```json
{
  "id": 2,
  "encrypted": true,
  "data": "gAAAAABl4xY2..."
}
```

## Troubleshooting

**Decryption failed errors:**
- Ensure `TASK_ENCRYPTION_KEY` environment variable is set
- Verify you're using the same key that encrypted the tasks
- Check for corrupted data in `tasks.json`

**Sync not working:**
- Verify API server is running: `curl http://localhost:5000/health`
- Check `TASKMGR_API_URL` is correct
- TaskMgr works offline - sync failures are non-blocking

**Tests failing:**
- Install dev dependencies: `pip install -r requirements-dev.txt`
- Check Python version (requires 3.8+)
- Ensure no `tasks.json` exists in test directory

## KERNEL Integration

This project uses KERNEL to progressively build Claude Code configuration based on observed patterns.

See `.claude/CLAUDE.md` for coding rules and project constraints.
