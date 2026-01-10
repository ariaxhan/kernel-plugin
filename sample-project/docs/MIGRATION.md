# Migration Guide

This guide helps you upgrade TaskMgr from v1.0 (basic version) to v2.0 (encryption + sync).

## Version Compatibility

| Version | Features | tasks.json Format |
|---------|----------|-------------------|
| v1.0 | Basic CRUD, CSV export, optimize | Plaintext only |
| v2.0 | + Encryption, REST sync, dev pipeline | Mixed plaintext/encrypted |

**Data Format Compatibility:**
- v2.0 can read v1.0 files (backward compatible)
- v1.0 CANNOT read encrypted tasks in v2.0 files
- Plaintext tasks remain compatible across versions

## Pre-Migration Checklist

Before upgrading, ensure:

- [ ] Backup `tasks.json` manually: `cp tasks.json tasks.json.pre-v2`
- [ ] Complete any in-progress tasks (avoid data loss)
- [ ] Export current tasks: `python src/taskmgr.py export pre-upgrade.csv`
- [ ] Document your current workflow (for validation after upgrade)
- [ ] Check Python version: `python3 --version` (requires 3.8+)

## Migration Steps

### Option 1: Clean Install (Recommended)

Best for new users or if you have few tasks.

```bash
# 1. Export existing tasks
python src/taskmgr.py export tasks-backup.csv

# 2. Backup tasks.json
cp tasks.json tasks.json.v1-backup

# 3. Install new dependencies
pip install -r requirements-dev.txt

# 4. Test new version
python src/taskmgr.py list
python src/taskmgr.py add "Test task v2" high

# 5. Import old tasks manually if needed
# (Add tasks one by one, marking confidential ones with --confidential)
```

### Option 2: In-Place Upgrade

Best if you have many existing tasks.

```bash
# 1. Backup tasks.json
cp tasks.json tasks.json.v1-backup

# 2. Install new dependencies
pip install -r requirements-dev.txt

# 3. Verify tasks load correctly
python src/taskmgr.py list

# 4. Tasks load successfully? You're done!
# All existing tasks work as plaintext tasks in v2.0
```

**Note:** Existing v1.0 tasks will NOT be encrypted automatically. Only new tasks marked with `--confidential` will be encrypted.

### Option 3: Encrypt Existing Tasks

If you want to encrypt existing tasks retroactively:

```bash
# 1. Generate and save encryption key
export TASK_ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
echo "export TASK_ENCRYPTION_KEY=\"$TASK_ENCRYPTION_KEY\"" >> ~/.bashrc

# 2. Backup tasks
cp tasks.json tasks.json.before-encryption

# 3. Create a migration script (or manually re-add confidential tasks)
# Read tasks.json, identify confidential tasks, delete them, re-add with --confidential
```

**Warning:** There is no automated encryption migration script. You must manually identify and re-add confidential tasks.

## New Features Setup

### Encryption

**1. Generate encryption key:**

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**2. Save key to environment:**

```bash
# Add to ~/.bashrc or ~/.zshrc
export TASK_ENCRYPTION_KEY="your-generated-key-here"

# Reload shell config
source ~/.bashrc  # or source ~/.zshrc
```

**3. Test encryption:**

```bash
python src/taskmgr.py add "Secret project" high --confidential
cat tasks.json  # Should see encrypted data
python src/taskmgr.py list  # Should show decrypted task
```

### REST API Sync

**1. Start API server:**

```bash
# In a separate terminal
python src/api_server.py
```

**2. Verify sync works:**

```bash
# Add a task (should auto-sync)
python src/taskmgr.py add "Synced task" medium

# Check server received it
curl http://localhost:5000/tasks
```

**3. (Optional) Configure custom API URL:**

```bash
export TASKMGR_API_URL="http://your-server.com:5000"
```

### Development Pipeline

**1. Verify tools installed:**

```bash
python3 -m black --version
python3 -m pylint --version
python3 -m mypy --version
```

**2. Test hooks:**

```bash
# Create a test Python file
echo "x=1" > test_hook.py

# Use Claude Code Write tool to edit it
# (Hooks should auto-format, lint, and type-check)
```

**3. Run full test suite:**

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## Data Migration Scenarios

### Scenario 1: No Confidential Tasks

**Before (v1.0 tasks.json):**
```json
[
  {"id": 1, "title": "Buy groceries", "priority": "high", "completed": false}
]
```

**After (v2.0 - no changes needed):**
```json
[
  {"id": 1, "title": "Buy groceries", "priority": "high", "completed": false, "confidential": false}
]
```

**Action:** None required. v2.0 adds `confidential: false` field automatically when loading old tasks.

### Scenario 2: Adding Confidential Tasks

**Before (v1.0):**
```json
[
  {"id": 1, "title": "Buy groceries", "priority": "high", "completed": false}
]
```

**After (v2.0 - add confidential task):**
```bash
python src/taskmgr.py add "Company layoffs" high --confidential
```

**Result (tasks.json):**
```json
[
  {"id": 1, "title": "Buy groceries", "priority": "high", "completed": false, "confidential": false},
  {"id": 2, "encrypted": true, "data": "gAAAAABl4xY2..."}
]
```

### Scenario 3: Converting Plaintext to Encrypted

**Manual process:**

```bash
# 1. Note the task details
python src/taskmgr.py list
# ○ [1] 🔴 Sensitive project (due: Jan 15, 2026)

# 2. Delete the plaintext task
python src/taskmgr.py delete 1

# 3. Re-add as confidential
python src/taskmgr.py add "Sensitive project" high 2026-01-15 --confidential
```

## Rollback Procedures

### Rollback to v1.0

If v2.0 causes issues and you need to revert:

**1. Stop using v2.0 features:**
```bash
# Disable sync (if running)
unset TASKMGR_API_URL

# Stop API server (Ctrl+C in server terminal)
```

**2. Restore backup:**
```bash
# Restore pre-upgrade backup
cp tasks.json.v1-backup tasks.json

# Or restore from CSV
python src/taskmgr.py export current-broken.csv  # Save current state
# Delete tasks.json
# Manually recreate tasks from pre-upgrade.csv
```

**3. Downgrade dependencies (if needed):**
```bash
# Uninstall v2.0 dependencies
pip uninstall cryptography flask requests pylint mypy

# Reinstall v1.0 (minimal)
pip install black
```

**4. Verify rollback:**
```bash
python src/taskmgr.py list
python src/taskmgr.py stats
```

### Partial Rollback (Remove Encrypted Tasks)

If encryption causes issues but you want to keep sync:

```bash
# 1. Export all tasks
python src/taskmgr.py export all-tasks.csv

# 2. Edit tasks.json manually - remove encrypted tasks
# Open tasks.json, delete entries with "encrypted": true

# 3. Re-add tasks as plaintext (without --confidential)
python src/taskmgr.py add "Previously encrypted task" high
```

## Common Migration Issues

### Issue 1: Decryption Failed Errors

**Symptom:**
```
Task list shows: [DECRYPTION FAILED]
```

**Causes:**
1. `TASK_ENCRYPTION_KEY` environment variable not set
2. Wrong encryption key (different from when task was created)
3. Corrupted encrypted data in tasks.json

**Solutions:**
```bash
# Check if key is set
echo $TASK_ENCRYPTION_KEY

# If missing, set the correct key
export TASK_ENCRYPTION_KEY="your-original-key"

# If key is lost, delete corrupted tasks and start fresh
# (Data is unrecoverable without the original key)
```

### Issue 2: Sync Failures on Startup

**Symptom:**
```
Warning: Could not sync with server: Connection refused
Operating in offline mode
```

**Causes:**
1. API server not running
2. Wrong `TASKMGR_API_URL`
3. Network connectivity issues

**Solutions:**
```bash
# Start API server
python src/api_server.py  # In separate terminal

# Verify server is running
curl http://localhost:5000/health

# Or disable sync temporarily
# (Use enable_sync=False in code, or ignore warnings)
```

### Issue 3: Missing Dependencies

**Symptom:**
```
ModuleNotFoundError: No module named 'cryptography'
```

**Solutions:**
```bash
# Install all dependencies
pip install -r requirements-dev.txt

# Or install individually
pip install cryptography flask requests pylint mypy black
```

### Issue 4: Task ID Conflicts After Import

**Symptom:**
Tasks have duplicate IDs after importing from CSV.

**Solutions:**
```bash
# Run database optimization
python src/taskmgr.py optimize

# This will reindex all tasks sequentially
```

### Issue 5: Hooks Not Running

**Symptom:**
Black, Pylint, Mypy don't run after file writes.

**Causes:**
1. `.claude/settings.json` not configured
2. Tools not installed
3. Running outside Claude Code CLI

**Solutions:**
```bash
# Verify tools installed
python3 -m black --version
python3 -m pylint --version
python3 -m mypy --version

# Check settings.json exists
cat .claude/settings.json

# Run tools manually if needed
python3 -m black src/taskmgr.py --line-length 100
python3 -m pylint src/taskmgr.py --score-yes
```

## Testing After Migration

**Validation checklist:**

```bash
# 1. List tasks
python src/taskmgr.py list
# Expected: All tasks visible, no errors

# 2. Add plaintext task
python src/taskmgr.py add "Migration test" medium
# Expected: Task added successfully

# 3. Add confidential task (if using encryption)
python src/taskmgr.py add "Secret test" high --confidential
# Expected: Task added, encrypted on disk

# 4. Complete a task
python src/taskmgr.py complete 1
# Expected: Task marked complete

# 5. Export tasks
python src/taskmgr.py export post-migration.csv
# Expected: CSV file created

# 6. Run tests
python3 -m unittest discover -s tests -p "test_*.py" -v
# Expected: 26+ tests pass

# 7. Check sync (if using API)
curl http://localhost:5000/tasks
# Expected: JSON list of tasks
```

## Best Practices After Migration

1. **Backup regularly:**
   ```bash
   # Add to crontab
   0 0 * * * cp ~/tasks.json ~/backups/tasks-$(date +\%Y\%m\%d).json
   ```

2. **Store encryption key securely:**
   - Use password manager (1Password, LastPass, etc.)
   - Never commit to git
   - Document recovery process

3. **Test disaster recovery:**
   ```bash
   # Simulate data loss
   cp tasks.json tasks.json.test-backup
   rm tasks.json
   # Restore from backup
   cp tasks.json.test-backup tasks.json
   ```

4. **Monitor sync health:**
   ```bash
   # Periodically check server health
   curl http://localhost:5000/health
   ```

5. **Keep dependencies updated:**
   ```bash
   # Check for updates quarterly
   pip list --outdated
   ```

## Getting Help

If migration fails:

1. **Check logs:** Review stderr output for warnings/errors
2. **Consult docs:** Read README.md and ARCHITECTURE.md
3. **Test in isolation:** Create fresh directory, test with sample data
4. **Report issues:** Include error messages, steps to reproduce, environment details

## Appendix: Automated Migration Script

For batch migrations, consider this template:

```python
#!/usr/bin/env python3
"""
Migrate v1.0 tasks.json to v2.0 with selective encryption
"""
import json
import sys
from pathlib import Path

def migrate(input_file, output_file, confidential_ids):
    """
    Migrate tasks, marking specified IDs as confidential

    Args:
        input_file: Path to v1.0 tasks.json
        output_file: Path to save v2.0 tasks.json
        confidential_ids: List of task IDs to mark as confidential
    """
    with open(input_file) as f:
        tasks = json.load(f)

    for task in tasks:
        task["confidential"] = task["id"] in confidential_ids

    with open(output_file, "w") as f:
        json.dump(tasks, f, indent=2)

    print(f"Migrated {len(tasks)} tasks")
    print(f"Marked {len(confidential_ids)} as confidential")

if __name__ == "__main__":
    migrate("tasks.json", "tasks-v2.json", confidential_ids=[2, 5, 7])
```

**Note:** This script only marks tasks as confidential in metadata. Actual encryption happens when TaskMgr saves them.
