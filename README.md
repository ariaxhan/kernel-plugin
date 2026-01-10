# KERNEL

**Self-Evolving Configuration for Claude Code**

KERNEL is a Claude Code plugin that progressively builds your project configuration based on observed patterns. Instead of manually creating commands, agents, and rules, KERNEL watches how you work and suggests artifacts that automate your workflows.

## What KERNEL Does

When you work with Claude Code, patterns emerge:
- You repeat the same multi-step workflow
- You need specialized expertise for certain tasks
- You integrate external services
- You state preferences about how things should be done

KERNEL captures these patterns and creates the appropriate Claude Code artifacts:

| Pattern | Artifact Created |
|---------|------------------|
| Repeated workflow | `.claude/commands/workflow-name.md` |
| Specialized task | `.claude/agents/specialist-name.md` |
| External service | Entry in `.mcp.json` |
| Pre/post processing | Hook in `.claude/settings.json` |
| Domain capability | `.claude/skills/capability.md` |
| Explicit preference | `.claude/rules/topic.md` |

## Quick Start

### 1. Install the Plugin

**macOS / Linux / Git Bash:**
```bash
# Clone into your Claude Code plugins directory
git clone https://github.com/yourusername/kernel-plugin.git ~/.claude/plugins/kernel

# Or copy directly into an existing project
cp -r kernel-plugin/.claude/commands/kernel-init.md your-project/.claude/commands/
cp kernel-plugin/kernel/CODING-PROMPT-BANK.MD your-project/
```

**Windows (PowerShell):**
```powershell
# Clone into your Claude Code plugins directory
git clone https://github.com/yourusername/kernel-plugin.git "$env:USERPROFILE\.claude\plugins\kernel"

# Or copy directly into an existing project
Copy-Item "kernel-plugin\.claude\commands\kernel-init.md" "your-project\.claude\commands\"
Copy-Item "kernel-plugin\kernel\CODING-PROMPT-BANK.MD" "your-project\"
```

See [SETUP.md](SETUP.md) for detailed installation instructions.

### 2. Initialize KERNEL in Your Project

```bash
cd your-project
claude

# Inside Claude Code, run:
/kernel-init
```

This analyzes your project and creates a customized `.claude/CLAUDE.md` with:
- Detected tier (T1 hackathon, T2 production, T3 critical)
- Stack-specific coding rules
- KERNEL artifact templates

### 3. Work Normally

As you work, KERNEL observes patterns and asks before creating artifacts:

```
"I noticed you've run this 3-step deployment workflow twice.
Should I create a /deploy command for it?"
```

## Features

### Coding Prompt Bank

KERNEL includes `CODING-PROMPT-BANK.MD`, a curated set of coding principles:

- **Core Philosophy**: Parse don't read, correctness over speed, minimal code
- **Execution Laws**: Investigate first, single source of truth, fail fast
- **Validation Protocols**: Pre-write and pre-commit checklists
- **Complexity Tiers**: T1 (hackathon), T2 (production), T3 (critical)

During initialization, KERNEL selects only the relevant sections based on your project's stack and tier.

### Artifact Types

**Commands** (`/command-name`)
```markdown
---
description: One-line description
allowed-tools: Read, Write, Bash
---
Instructions for Claude when /command-name is invoked.
```

**Agents** (Specialized sub-agents)
```markdown
---
name: agent-name
description: What it specializes in
tools: Read, Write, Grep, Glob, Bash
model: sonnet
---
You are a specialist in X. Your job is to...
```

**MCP Servers** (External integrations)
```json
{"mcpServers": {"name": {"command": "npx", "args": ["package-name"]}}}
```

**Hooks** (Pre/post processing)
```json
{"hooks": {"PostToolUse": [{"matcher": "Write", "hooks": [{"type": "command", "command": "prettier --write $CLAUDE_FILE_PATHS"}]}]}}
```

**Skills** (Domain capabilities)
Markdown files describing patterns and examples for specific domains.

**Rules** (User preferences)
Imperative rules grouped by topic that Claude follows.

### Included Components

- **`/kernel-init`** - Initialize KERNEL for any project
- **`test-maintainer` agent** - Generates and maintains tests following project conventions
- **Claude Docs MCP Server** - Fetches latest Claude Code documentation

## Project Structure

```
kernel-plugin/
├── .claude/
│   ├── CLAUDE.md              # Project config (KERNEL-generated)
│   ├── commands/
│   │   └── kernel-init.md     # Initialization command
│   ├── agents/                 # Specialist agents
│   ├── skills/                 # Domain capabilities
│   ├── rules/
│   │   └── preferences.md     # User preferences
│   └── settings.json          # Hooks configuration
├── kernel/
│   ├── CODING-PROMPT-BANK.MD  # Base coding rules
│   ├── commands/
│   │   └── init.md            # Init command template
│   └── agents/
│       └── test-maintainer.md # Test specialist agent
├── .mcp.json                   # MCP server configuration
├── claude-docs-server.py       # Documentation MCP server
├── README.md                   # This file
└── SETUP.md                    # Detailed setup guide
```

## Philosophy

KERNEL follows these principles:

1. **Conservative**: Only create artifacts for clear, repeated patterns
2. **Minimal**: Start simple, iterate later
3. **Ask First**: Confirm with user before creating if unsure
4. **Check Existing**: Read configs first to avoid duplicates

Configuration should grow organically from actual usage, not speculation.

## Requirements

- Claude Code CLI installed and configured
- Git (for cloning)
- Python 3.8+ (for Claude Docs MCP server, optional)

## Platform Support

KERNEL works on both **macOS** and **Windows**. See [SETUP.md](SETUP.md) for platform-specific installation instructions including:
- PowerShell commands for Windows
- Command Prompt (cmd) alternatives
- Git Bash compatibility
- Path configuration differences

## License

MIT

## Contributing

Contributions welcome. Please read the coding rules in `CODING-PROMPT-BANK.MD` before submitting PRs.
