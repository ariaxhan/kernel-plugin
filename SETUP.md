# KERNEL Setup Guide

This guide walks you through installing KERNEL for Claude Code.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
   - [Method 1: Via Plugin Menu (Recommended)](#method-1-via-plugin-menu-recommended)
   - [Method 2: Programmatic Installation](#method-2-programmatic-installation)
3. [Enabling the Plugin](#enabling-the-plugin)
4. [Initializing KERNEL](#initializing-kernel)
5. [Configuration](#configuration)
6. [Optional: Claude Docs MCP Server](#optional-claude-docs-mcp-server)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Claude Code CLI v1.0.33+**: Plugins require version 1.0.33 or later
  ```bash
  claude --version
  ```

---

## Installation

### Method 1: Via Plugin Menu (Recommended)

This is the most reliable installation method.

**Step 1: Open the Plugin Menu**

In Claude Code, type:
```
/plugin
```

**Step 2: Navigate to Marketplaces**

Use arrow keys or tab to navigate:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Plugins  Discover   Installed   Marketplaces  (←/→ or tab to cycle)    │
└─────────────────────────────────────────────────────────────────────────┘
```

Select **Marketplaces**.

**Step 3: Add the KERNEL Marketplace**

Select **+ Add Marketplace**:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ Manage marketplaces                                                     │
│                                                                         │
│ ❯ + Add Marketplace                                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

**Step 4: Enter the Marketplace URL**

When prompted, enter the full GitHub URL:
```
┌─ Add Marketplace ───────────────────────────────────────────────────────┐
│                                                                         │
│ Enter marketplace source:                                               │
│ Examples:                                                               │
│  • owner/repo (GitHub)                                                  │
│  • git@github.com:owner/repo.git (SSH)                                  │
│  • https://example.com/marketplace.json                                 │
│  • ./path/to/marketplace                                                │
│                                                                         │
│     https://github.com/ariaxhan/kernel-plugin                           │
╰─────────────────────────────────────────────────────────────────────────╯
```

Enter:
```
https://github.com/ariaxhan/kernel-plugin
```

**Step 5: Enable the Plugin**

After adding the marketplace, navigate to **Discover** or **Installed** and enable the KERNEL plugin:
```
┌─────────────────────────────────────────────────────────────────────────┐
│ User                                                                    │
│                                                                         │
│ ❯ kernel Plugin · kernel-marketplace · ✔ enabled                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Method 2: Programmatic Installation

For teams or automated setups, add the marketplace to your settings.

**Option A: User-level (applies to all your projects)**

Edit `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "kernel-marketplace": {
      "source": {
        "source": "github",
        "repo": "ariaxhan/kernel-plugin"
      }
    }
  },
  "enabledPlugins": {
    "kernel@kernel-marketplace": {}
  }
}
```

**Option B: Project-level (for team sharing)**

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "kernel-marketplace": {
      "source": {
        "source": "github",
        "repo": "ariaxhan/kernel-plugin"
      }
    }
  },
  "enabledPlugins": {
    "kernel@kernel-marketplace": {}
  }
}
```

When team members trust the repository folder, Claude Code will prompt them to install the marketplace.

**Note**: The `extraKnownMarketplaces` method only works in interactive mode. It does not work in CI/CD or headless (`-p`) mode.

---

## Enabling the Plugin

After installation, verify the plugin is enabled:

1. Run `/plugin` in Claude Code
2. Go to **Installed** tab
3. Confirm **kernel Plugin** shows **✔ enabled**

If not enabled, select it and enable it.

---

## Initializing KERNEL

After installation, initialize KERNEL in your project:

```bash
# 1. Open your project in Claude Code
cd /path/to/your/project
claude

# 2. Run the initialization command
/kernel-init
```

### What Initialization Does

1. **Analyzes Your Project**: Detects stack, tier (T1/T2/T3), and domain
2. **Creates Directory Structure**:
   ```
   .claude/
   ├── commands/      # Slash commands
   ├── agents/        # Specialist sub-agents
   ├── skills/        # Domain capabilities
   └── rules/         # User preferences
   ```
3. **Generates `.claude/CLAUDE.md`**: Customized configuration with coding rules
4. **Creates Starter Files**: Settings, rules, and templates

### Initialization Output

```
KERNEL Initialization Complete

Detection Summary:
- TIER: 2 (Production-grade)
- STACK: TypeScript, React, Node.js
- DOMAIN: Web Application

Files Created:
- .claude/CLAUDE.md (customized)
- .claude/settings.json
- .claude/agents/
- .claude/skills/
- .claude/rules/preferences.md
```

---

## Configuration

### Customizing Your Tier

Edit `.claude/CLAUDE.md` and change the TIER value:

```markdown
TIER: 1  # Hackathon - ship fast, works once
TIER: 2  # Production - maintainable (default)
TIER: 3  # Critical - zero tolerance, audit trails
```

### Adding Project Constraints

Edit the `PROJECT CONSTRAINTS` section in `.claude/CLAUDE.md`:

```markdown
## PROJECT CONSTRAINTS

- All API endpoints must include rate limiting
- Database queries must use parameterized statements
- No dependencies without security audit
```

### Creating Custom Commands

Add files to `.claude/commands/`:

```markdown
---
description: Run tests and lint before committing
allowed-tools: Bash, Read
---

# Pre-Commit Check

1. Run the test suite: `npm test`
2. Run the linter: `npm run lint`
3. Report any failures
4. If all pass, confirm ready to commit
```

Save as `.claude/commands/pre-commit.md`, then use with `/pre-commit`.

### Creating Custom Agents

Add files to `.claude/agents/`:

```markdown
---
name: api-designer
description: Designs RESTful API endpoints following project conventions
tools: Read, Write, Grep, Glob
model: sonnet
---

You are an API design specialist. When asked to design an endpoint:

1. Review existing endpoints in `src/routes/`
2. Follow the established naming conventions
3. Include request/response types
4. Add validation schemas
5. Document in OpenAPI format
```

Save as `.claude/agents/api-designer.md`.

### Adding User Preferences

Edit `.claude/rules/preferences.md`:

```markdown
# Project Preferences

## Code Style
- Use functional components over class components
- Prefer named exports over default exports
- Use async/await over .then() chains

## Naming
- React components: PascalCase
- Utilities: camelCase
- Constants: SCREAMING_SNAKE_CASE
```

---

## Optional: Claude Docs MCP Server

KERNEL includes an MCP server for accessing Claude Code documentation.

### Installation

```bash
# Install Python dependency
pip3 install requests

# Make executable (macOS/Linux)
chmod +x claude-docs-server.py
```

### Configuration

Add to your `.mcp.json`:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "claude-docs": {
      "command": "python3",
      "args": ["/path/to/kernel-plugin/claude-docs-server.py"]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "claude-docs": {
      "command": "python",
      "args": ["C:\\path\\to\\kernel-plugin\\claude-docs-server.py"]
    }
  }
}
```

---

## Troubleshooting

### Marketplace not appearing after adding

**Cause**: Cache or sync issue.

**Fix**: Restart Claude Code and run `/plugin` again.

### "extraKnownMarketplaces" not working

**Cause**: Only works in interactive mode.

**Fix**: Use Method 1 (Plugin Menu) or ensure you're not running in headless mode.

### Plugin shows but won't enable

**Cause**: May need to trust the marketplace first.

**Fix**:
1. Run `/plugin`
2. Go to **Marketplaces**
3. Select the kernel marketplace
4. Accept any trust prompts

### "Command not found: /kernel-init"

**Cause**: Plugin not properly enabled.

**Fix**:
1. Verify plugin is enabled via `/plugin` → **Installed**
2. If not visible, re-add the marketplace

### Initialization detects wrong stack/tier

**Cause**: Project doesn't have standard config files.

**Fix**: After initialization, manually edit `.claude/CLAUDE.md`:
```markdown
TIER: 2
STACK: Your actual stack here
DOMAIN: Your domain here
```

---

## Next Steps

After setup:

1. **Work normally** - KERNEL observes your patterns
2. **Accept or decline** - When KERNEL suggests artifacts, choose what to keep
3. **Iterate** - Edit generated artifacts to refine them
4. **Share** - Commit `.claude/` to version control so your team benefits

For more information, see the [README](README.md).
