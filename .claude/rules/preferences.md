# Project Preferences

<!-- KERNEL adds preferences here as patterns are observed -->

## Current Preferences

### Date and Time Formatting

1. **Display Format**: Always show dates in "Jan 15, 2026" format (not ISO format like "2026-01-15")
   - Applied to: list views, stats, exports, user-facing output
   - Implementation: Use `strftime("%b %d, %Y")` for display

2. **Timestamp Storage**: All timestamps use UTC with explicit timezone info
   - Format: ISO 8601 with timezone (`2026-01-10T11:09:21.317490+00:00`)
   - Applied to: `created_at`, `completed_at` fields
   - Implementation: Use `datetime.now(timezone.utc).isoformat()`

### Data Safety

3. **Automatic Backups**: tasks.json is automatically backed up before every modification
   - Backup location: `tasks.json.backup` (same directory)
   - Triggered on: every `_save_tasks()` call
   - Implementation: `shutil.copy2()` before writing new data
