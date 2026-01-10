# KERNEL Plugin Project

This project builds KERNEL, a self-evolving Claude Code plugin.

## KERNEL: Self-Evolving Configuration

KERNEL progressively builds Claude Code config based on observed patterns.

### Pattern → Artifact Mapping

| When You Notice... | Create This |
|-------------------|-------------|
| Same multi-step workflow repeated 2+ times | `.claude/commands/workflow-name.md` |
| Task needing specialized expertise | `.claude/agents/specialist-name.md` |
| External service integration needed | Entry in `.mcp.json` |
| Pre/post processing on tool usage | Hook in `.claude/settings.json` |
| Domain capability used repeatedly | `.claude/skills/capability.md` |
| User states explicit preference | `.claude/rules/topic.md` |

### How to Create Each Artifact

**SLASH COMMAND** (`.claude/commands/name.md`):
```md
---
description: One-line description
allowed-tools: Read, Write, Bash
---
Instructions for Claude to follow when /name is invoked.
```

**SUBAGENT** (`.claude/agents/name.md`):
```md
---
name: agent-name
description: What it specializes in
tools: Read, Write, Grep, Glob, Bash
model: sonnet
---
You are a specialist in X. Your job is to...
```

**MCP SERVER** (`.mcp.json`):
```json
{"mcpServers": {"name": {"command": "npx", "args": ["package-name"]}}}
```

**HOOK** (`.claude/settings.json`):
```json
{"hooks": {"PostToolUse": [{"matcher": "Write", "hooks": [{"type": "command", "command": "prettier --write $CLAUDE_FILE_PATHS"}]}]}}
```

**SKILL** (`.claude/skills/name.md`):
Markdown describing capability, patterns, examples.

**RULE** (`.claude/rules/topic.md`):
```md
# Topic
- Imperative rule 1
- Imperative rule 2
```

### Before Completing Any Task

Check:
1. Did user repeat a workflow? → Create command
2. Did task need specialized focus? → Create agent
3. Did we use external service? → Add to .mcp.json
4. Is there a pre/post pattern? → Create hook
5. Did user state preference? → Add rule

### Guidelines

- **Conservative**: Only create for clear, repeated patterns
- **Minimal**: Start simple, iterate later
- **Ask first**: Confirm with user before creating if unsure
- **Check existing**: Read configs first to avoid duplicates
