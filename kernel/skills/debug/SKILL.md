---
name: debug
description: Systematic debugging methodology. Auto-triggers on "bug", "error", "not working", "broken", "failing", "debug", "fix this", "why isn't", "something's wrong", or any description of unexpected behavior.
---

# Debug Mode

Systematic diagnosis and root cause fixing. Activated automatically when debugging signals detected.

## Methodology

**NEVER guess. Always investigate.**

### Phase 1: Reproduce
1. Confirm the error exists
2. Get exact error message/behavior
3. Identify minimal reproduction steps
4. Note: works in X, fails in Y?

### Phase 2: Isolate
1. What changed recently?
2. Binary search: which commit/change introduced it?
3. Smallest code path that triggers issue?
4. Environment-specific? (versions, configs, data)

### Phase 3: Instrument
1. Add logging at key points
2. Check assumptions (values, types, state)
3. Trace execution path
4. Compare expected vs actual at each step

### Phase 4: Root Cause
1. WHY is this happening, not just WHAT
2. Is this a symptom of deeper issue?
3. Why didn't we catch this earlier?

### Phase 5: Fix + Verify
1. Fix the root cause, not the symptom
2. Verify fix works
3. Check for regressions
4. Add test to prevent recurrence

## Anti-patterns

- Random changes hoping something works
- Fixing symptoms instead of causes
- Skipping reproduction ("I saw it once")
- Not checking assumptions
- Fixing without understanding

## Output Behavior

When debugging:
- Write findings to file (not terminal dump)
- Log: hypothesis → test → result
- Terminal: brief status updates only
- Final fix: explain what was wrong and why

## Integration

If project has `kernel/banks/DEBUGGING-BANK.md`, load it for deep methodology.
