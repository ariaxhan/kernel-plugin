# TaskMgr Architecture Documentation

## System Overview

TaskMgr is a Python-based CLI task manager with three core subsystems:

1. **Storage Layer** - JSON-based persistence with encryption support
2. **Sync Layer** - REST API client for cloud synchronization
3. **Presentation Layer** - CLI interface with formatted output

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│  (main function, argument parsing, user interaction)         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   TaskManager Class                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Storage    │  │  Encryption  │  │  API Sync    │      │
│  │  Management  │  │    (Fernet)  │  │  (requests)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────┬───────────────────┬───────────────────┘
                      │                   │
        ┌─────────────▼──────┐   ┌────────▼────────┐
        │   tasks.json       │   │  API Server     │
        │  (local storage)   │   │  (Flask mock)   │
        └────────────────────┘   └─────────────────┘
```

## Data Flow

### 1. Task Creation Flow

```
User Input
   │
   ▼
main() parses args
   │
   ▼
TaskManager.add_task()
   │
   ├──► Generate next ID (max existing ID + 1)
   ├──► Validate priority
   ├──► Create task dict with UTC timestamp
   ├──► Append to self.tasks list
   │
   ▼
_save_tasks()
   │
   ├──► Check each task for confidential flag
   ├──► If confidential: _encrypt_task()
   │     └──► JSON.dumps(task) → Fernet.encrypt() → base64
   ├──► Create backup (tasks.json.backup)
   ├──► Write to temp file (tasks.json.tmp)
   └──► Atomic rename (tmp → tasks.json)
   │
   ▼
_sync_push("create", task)
   │
   ├──► If sync_enabled == False: return
   ├──► POST to {api_url}/tasks
   ├──► If success: silent
   └──► If failure: warn user, continue
   │
   ▼
Print confirmation to user
```

### 2. Startup/Load Flow

```
TaskManager.__init__()
   │
   ▼
_get_encryption_key()
   │
   ├──► Read TASK_ENCRYPTION_KEY env var
   ├──► If not set: auto-generate + warn
   └──► Return Fernet instance
   │
   ▼
_load_tasks()
   │
   ├──► Read tasks.json
   ├──► Parse JSON
   ├──► For each task:
   │     ├──► If task["encrypted"] == true:
   │     │     └──► _decrypt_task() → Fernet.decrypt() → JSON.loads()
   │     └──► Else: use as-is
   └──► Return tasks list
   │
   ▼
_sync_pull() (if sync_enabled)
   │
   ├──► GET {api_url}/sync
   ├──► If success:
   │     ├──► Merge server tasks (server-wins)
   │     └──► _save_tasks()
   └──► If failure: warn, continue in offline mode
```

### 3. Update/Delete Flow

```
User command (complete/delete)
   │
   ▼
Find task by ID
   │
   ▼
Modify/remove from self.tasks
   │
   ▼
_save_tasks()
   │
   ▼
_sync_push("update"/"delete", task)
```

## Storage Layer

### File Format

**tasks.json** contains an array of task objects:

```json
[
  {
    "id": 1,
    "title": "Public task",
    "priority": "high",
    "due_date": "2026-01-15",
    "completed": false,
    "created_at": "2026-01-10T12:00:00+00:00",
    "confidential": false
  },
  {
    "id": 2,
    "encrypted": true,
    "data": "gAAAAABl4xY2xQ..."
  }
]
```

### Atomic Write Strategy

To prevent data corruption:

1. Create backup: `tasks.json` → `tasks.json.backup`
2. Write to temp file: `tasks.json.tmp`
3. Atomic rename: `tasks.json.tmp` → `tasks.json`
4. On failure: restore from backup

### Backup Files

- `.backup` - Created before every successful write
- `.corrupt` - Created when JSON parse fails on load
- `.tmp` - Temporary write target (deleted on completion)

## Encryption Layer

### Algorithm

**Fernet (AES-128-CBC + HMAC-SHA256)**

- Symmetric encryption (same key for encrypt/decrypt)
- Authenticated encryption (prevents tampering)
- URL-safe base64 encoding

### Key Management

```python
Priority:
1. TASK_ENCRYPTION_KEY environment variable
2. Auto-generate (temporary, session-only)

Warnings:
- Auto-generated keys print warning to stderr
- Lost keys = permanent data loss
```

### Encryption Process

```python
# Encrypt
task_json = json.dumps(task)                    # Serialize to JSON
encrypted_bytes = fernet.encrypt(task_json.encode())  # Encrypt
encrypted_str = encrypted_bytes.decode()         # Base64 string
wrapper = {
    "id": task["id"],
    "encrypted": true,
    "data": encrypted_str
}

# Decrypt
encrypted_bytes = wrapper["data"].encode()      # Base64 string
decrypted_bytes = fernet.decrypt(encrypted_bytes)  # Decrypt
task_json = decrypted_bytes.decode()             # JSON string
task = json.loads(task_json)                     # Deserialize
```

### Decryption Failure Handling

When decryption fails (wrong key, corrupted data):

```python
{
    "id": 2,
    "title": "[DECRYPTION FAILED]",
    "priority": "medium",
    "completed": false,
    "created_at": "",
    "confidential": true
}
```

## Sync Layer

### API Client (TaskManager)

**Configuration:**
- `TASKMGR_API_URL` env var (default: `http://localhost:5000`)
- `enable_sync` constructor parameter (default: `True`)

**Operations:**
- `_sync_pull()` - Pull tasks from server (startup only)
- `_sync_push(operation, task)` - Push changes to server

**Error Handling:**
- Pull failure (startup): Print warning, continue in offline mode
- Push failure (runtime): Print warning, local save still succeeds

### API Server (Flask Mock)

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create task |
| PUT | `/tasks/<id>` | Update task |
| DELETE | `/tasks/<id>` | Delete task |
| GET | `/sync` | Full sync (returns tasks + server_time) |
| GET | `/health` | Health check |

**Storage:**
- In-memory dictionary (`tasks_db`)
- Ephemeral (resets on server restart)
- No encryption support (expects plaintext tasks)

**Conflict Resolution:**
- Server-wins on startup pull
- Last-write-wins for concurrent updates
- No conflict detection/merging

## Error Handling

### Strategy Matrix

| Error Type | Handling | User Impact |
|------------|----------|-------------|
| Invalid priority | Exit with error message | Command fails |
| Invalid task ID | Print message, continue | Operation skipped |
| JSON parse failure | Backup corrupt file, start fresh | Data preserved |
| Encryption key missing | Auto-generate + warn | Temporary session key |
| Decryption failure | Placeholder task | Corrupted task hidden |
| API server down (startup) | Print warning, offline mode | Local-only operations |
| API server down (runtime) | Print warning, save locally | Sync fails, data safe |
| File write failure | Restore from backup | No data loss |

### Fail-Fast vs Graceful Degradation

**Fail-Fast:**
- Invalid input (priority, task ID)
- Missing required arguments

**Graceful Degradation:**
- API server unavailable
- Encryption key missing
- Decryption failures
- Network errors

## Development Pipeline

### Hook System

**Trigger:** PostToolUse (after Write tool)

**Execution Order:**
1. Black (auto-format) - Modifies file
2. Pylint (lint) - Warns if score < 7.0
3. Mypy (type check) - Warnings only
4. Unittest (if test file) - Runs specific test

**Configuration:** `.claude/settings.json`

### Testing Architecture

**Framework:** Python unittest

**Test Structure:**
```
tests/
├── test_encryption.py    # Fernet encryption/decryption
├── test_sync.py          # API client with mocks
├── test_export.py        # CSV export
└── test_optimize.py      # Database reindexing
```

**Isolation Strategy:**
- Each test creates temp directory
- Separate database file per test
- Mock external dependencies (requests)
- Clean up in tearDown()

## Performance Considerations

### Current Implementation

- **In-memory operations:** All tasks loaded on startup
- **O(n) task lookup:** Linear search by ID
- **File I/O on every change:** Write entire tasks.json
- **No caching:** API calls on every sync

### Scalability Limits

| Metric | Limit | Reason |
|--------|-------|--------|
| Task count | ~10,000 | In-memory list, linear search |
| File size | ~10 MB | Full file rewrite on change |
| Concurrent users | 1 | File-based locking, no transactions |
| API latency | 5s timeout | Blocking HTTP calls |

### Future Optimizations

1. SQLite database (indexed queries, transactions)
2. Delta sync (only changed tasks)
3. Background sync (async API calls)
4. Compression (gzip encrypted data)

## Security Considerations

### Threat Model

**Protected Against:**
- Disk access (encrypted tasks unreadable without key)
- File tampering (HMAC validation)
- Accidental key exposure (env var, not committed)

**NOT Protected Against:**
- Memory dumps (tasks decrypted in RAM)
- Key theft (if env var compromised)
- Side-channel attacks
- API server compromise (sends plaintext)

### Security Best Practices

1. Store encryption keys in secure vault (not env vars)
2. Use HTTPS for API communication
3. Implement API authentication/authorization
4. Rotate encryption keys periodically
5. Audit access to tasks.json and backups

## Deployment Architecture

### Single-User Local Mode

```
User's Machine
├── taskmgr.py (CLI)
├── tasks.json (local storage)
└── No API server
```

### Multi-User Sync Mode

```
User's Machine              Cloud Server
├── taskmgr.py (CLI)   →    ├── api_server.py (Flask)
├── tasks.json (cache) ←    └── tasks_db (in-memory)
```

**Considerations:**
- API server needs persistent storage (replace in-memory dict)
- Add authentication (user-specific task isolation)
- HTTPS for encrypted transport
- Rate limiting and abuse protection

## Extension Points

### Adding New Features

**New task fields:**
1. Add to task dict in `add_task()`
2. Update CSV export in `export_csv()`
3. Add tests in relevant test file

**New commands:**
1. Add method to TaskManager class
2. Add case in `main()` CLI router
3. Update usage message

**New sync backends:**
1. Create new `_sync_push_*()` and `_sync_pull_*()` methods
2. Add config for backend selection
3. Implement adapter interface

## Monitoring & Observability

### Current Logging

- `stderr` for warnings/errors
- `stdout` for user feedback
- No structured logging
- No metrics collection

### Recommended Additions

1. **Structured logging:** JSON logs with timestamps, levels, context
2. **Metrics:** Task counts, sync success/failure rates, encryption stats
3. **Tracing:** Track request flow through sync layer
4. **Alerting:** Notify on repeated sync failures, encryption errors

## References

- [Cryptography Fernet Spec](https://cryptography.io/en/latest/fernet/)
- [Flask REST API Patterns](https://flask.palletsprojects.com/en/3.0.x/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
