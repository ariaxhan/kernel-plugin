---
description: Update KERNEL templates to latest version from plugin
allowed-tools: Read, Write, Glob, Bash
---

# Update KERNEL Templates

Manually refresh KERNEL templates in your project to match the latest plugin version.

## When to Use

- Plugin was updated and you want latest templates
- Templates were modified and you want to reset to defaults
- New banks/commands were added to the plugin

## What This Does

1. **Preserves your customizations**:
   - Keeps `.claude/CLAUDE.md` (your tier, stack, constraints)
   - Keeps `.claude/rules/` (your project rules)
   - Keeps `.claude/agents/` and `.claude/skills/` (your custom artifacts)

2. **Updates from plugin**:
   - Re-copies `kernel/banks/` (latest methodology banks)
   - Re-copies `kernel/commands/` (latest mode commands)
   - Re-copies `kernel/hooks/` (latest hook templates)
   - Updates plugin version reference

## Process

### Step 1: Locate Plugin

Find the KERNEL plugin installation:
1. `~/.claude/plugins/kernel/`
2. Or wherever the plugin is installed

### Step 2: Read Current Config

Check existing `.claude/CLAUDE.md` to preserve:
- TIER
- STACK
- DOMAIN
- PROJECT CONSTRAINTS (user-customized section)

### Step 3: Copy Latest Templates

**From kernel/banks/ → project root or .claude/banks/**:
- PLANNING-BANK.md
- DEBUGGING-BANK.md
- DISCOVERY-BANK.md
- REVIEW-BANK.md
- DOCUMENTATION-BANK.md

**From kernel/commands/ → .claude/commands/**:
- discover.md
- plan.md
- debug.md
- review.md
- docs.md
- branch.md
- ship.md
- parallelize.md
- handoff.md

**From kernel/hooks/ → .claude/hooks/** (if they exist):
- pattern-capture.md
- post-write.md
- pre-complete.md

### Step 4: Report Changes

Show:
- Which files were updated
- Plugin version (from .claude-plugin/plugin.json)
- What was preserved (your customizations)

## Example Output

```
KERNEL Update Complete

Plugin version: 1.1.0

Updated templates:
✓ kernel/banks/ (5 banks)
✓ .claude/commands/ (9 commands)
✓ kernel/hooks/ (3 hooks)

Preserved:
✓ .claude/CLAUDE.md (your tier, stack, constraints)
✓ .claude/rules/ (your project rules)
✓ .claude/agents/ (your custom agents)
✓ .claude/skills/ (your custom skills)
```

## Notes

- This does NOT re-run tier/stack detection
- This does NOT modify your custom artifacts
- This IS a safe operation - only updates templates
- Run `/kernel-init` if you want full re-initialization
