# KERNEL Setup Guide

This guide walks you through installing and configuring KERNEL for Claude Code.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
   - [macOS Installation](#macos-installation)
   - [Windows Installation](#windows-installation)
3. [Initializing KERNEL](#initializing-kernel)
4. [Configuration](#configuration)
5. [Optional: Claude Docs MCP Server](#optional-claude-docs-mcp-server)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- **Claude Code CLI**: KERNEL is a plugin for Claude Code
  ```bash
  # Verify Claude Code is installed
  claude --version
  ```

- **Git**: For cloning the repository
  ```bash
  git --version
  ```

### Optional

- **Python 3.8+**: Only needed if using the Claude Docs MCP server
  ```bash
  # macOS/Linux
  python3 --version

  # Windows
  python --version
  ```

- **pip**: For installing Python dependencies
  ```bash
  # macOS/Linux
  pip3 --version

  # Windows
  pip --version
  ```

---

## Installation Methods

Choose your operating system and installation method.

---

## macOS Installation

### Method A: Global Installation (Recommended)

Install KERNEL globally so it's available for all your projects.

```bash
# 1. Create Claude plugins directory if it doesn't exist
mkdir -p ~/.claude/plugins

# 2. Clone KERNEL into the plugins directory
git clone https://github.com/yourusername/kernel-plugin.git ~/.claude/plugins/kernel

# 3. Copy the prompt bank to your global Claude config
cp ~/.claude/plugins/kernel/kernel/CODING-PROMPT-BANK.MD ~/.claude/CODING-PROMPT-BANK.MD
```

Now you can run `/kernel-init` in any project.

### Method B: Per-Project Installation

Install KERNEL directly into a specific project.

```bash
# 1. Navigate to your project
cd /path/to/your/project

# 2. Create the .claude directory structure
mkdir -p .claude/commands .claude/agents .claude/skills .claude/rules

# 3. Copy KERNEL files
cp /path/to/kernel-plugin/.claude/commands/kernel-init.md .claude/commands/
cp /path/to/kernel-plugin/kernel/CODING-PROMPT-BANK.MD ./

# 4. Initialize (see next section)
```

### Method C: Manual Setup (No Git)

If you can't use git, manually create the files:

1. Create `.claude/commands/kernel-init.md` with the content from this repository
2. Create `CODING-PROMPT-BANK.MD` in your project root or `~/.claude/`
3. Run `/kernel-init` in Claude Code

---

## Windows Installation

### Method A: Global Installation (Recommended)

Install KERNEL globally so it's available for all your projects.

**Using PowerShell:**

```powershell
# 1. Create Claude plugins directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\plugins"

# 2. Clone KERNEL into the plugins directory
git clone https://github.com/yourusername/kernel-plugin.git "$env:USERPROFILE\.claude\plugins\kernel"

# 3. Copy the prompt bank to your global Claude config
Copy-Item "$env:USERPROFILE\.claude\plugins\kernel\kernel\CODING-PROMPT-BANK.MD" "$env:USERPROFILE\.claude\CODING-PROMPT-BANK.MD"
```

**Using Command Prompt (cmd):**

```cmd
:: 1. Create Claude plugins directory if it doesn't exist
mkdir "%USERPROFILE%\.claude\plugins"

:: 2. Clone KERNEL into the plugins directory
git clone https://github.com/yourusername/kernel-plugin.git "%USERPROFILE%\.claude\plugins\kernel"

:: 3. Copy the prompt bank to your global Claude config
copy "%USERPROFILE%\.claude\plugins\kernel\kernel\CODING-PROMPT-BANK.MD" "%USERPROFILE%\.claude\CODING-PROMPT-BANK.MD"
```

**Using Git Bash (recommended for Windows):**

```bash
# 1. Create Claude plugins directory if it doesn't exist
mkdir -p ~/.claude/plugins

# 2. Clone KERNEL into the plugins directory
git clone https://github.com/yourusername/kernel-plugin.git ~/.claude/plugins/kernel

# 3. Copy the prompt bank to your global Claude config
cp ~/.claude/plugins/kernel/kernel/CODING-PROMPT-BANK.MD ~/.claude/CODING-PROMPT-BANK.MD
```

### Method B: Per-Project Installation

Install KERNEL directly into a specific project.

**Using PowerShell:**

```powershell
# 1. Navigate to your project
cd C:\path\to\your\project

# 2. Create the .claude directory structure
New-Item -ItemType Directory -Force -Path ".claude\commands", ".claude\agents", ".claude\skills", ".claude\rules"

# 3. Copy KERNEL files
Copy-Item "C:\path\to\kernel-plugin\.claude\commands\kernel-init.md" ".claude\commands\"
Copy-Item "C:\path\to\kernel-plugin\kernel\CODING-PROMPT-BANK.MD" ".\"

# 4. Initialize (see next section)
```

**Using Command Prompt (cmd):**

```cmd
:: 1. Navigate to your project
cd C:\path\to\your\project

:: 2. Create the .claude directory structure
mkdir .claude\commands .claude\agents .claude\skills .claude\rules

:: 3. Copy KERNEL files
copy "C:\path\to\kernel-plugin\.claude\commands\kernel-init.md" ".claude\commands\"
copy "C:\path\to\kernel-plugin\kernel\CODING-PROMPT-BANK.MD" "."

:: 4. Initialize (see next section)
```

### Method C: Manual Setup (No Git)

If you can't use git, manually create the files:

1. Create `.claude\commands\kernel-init.md` with the content from this repository
2. Create `CODING-PROMPT-BANK.MD` in your project root or `%USERPROFILE%\.claude\`
3. Run `/kernel-init` in Claude Code

### Windows Path Notes

- Use `%USERPROFILE%` in cmd or `$env:USERPROFILE` in PowerShell instead of `~`
- Windows paths use backslashes (`\`), but Git Bash accepts forward slashes (`/`)
- The `.claude` directory works the same on Windows as on macOS/Linux

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

1. **Locates the Prompt Bank**: Searches for `CODING-PROMPT-BANK.MD` in:
   - Project root
   - `~/.claude/CODING-PROMPT-BANK.MD`
   - Plugin location

2. **Analyzes Your Project**: Detects:
   - Stack (language, framework, tools)
   - Tier (T1 hackathon, T2 production, T3 critical)
   - Domain (API, CLI, library, app)

3. **Creates Directory Structure**:
   ```
   .claude/
   ├── commands/      # Slash commands
   ├── agents/        # Specialist sub-agents
   ├── skills/        # Domain capabilities
   └── rules/         # User preferences
   ```

4. **Generates `.claude/CLAUDE.md`**: A customized configuration with:
   - Selected coding rules from the prompt bank
   - Project-specific constraints
   - KERNEL artifact templates

5. **Creates Starter Files**:
   - `.claude/settings.json` (hooks configuration)
   - `.claude/rules/preferences.md` (user preferences)
   - `.mcp.json` (if not exists)

### Initialization Output

After running `/kernel-init`, you'll see a summary:

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

KERNEL includes an MCP server that provides access to Claude Code documentation.

### macOS Installation

```bash
# 1. Navigate to the kernel plugin
cd ~/.claude/plugins/kernel  # or your project directory

# 2. Install Python dependencies
pip3 install requests

# 3. Make the server executable
chmod +x claude-docs-server.py
```

**Configuration** - Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "claude-docs": {
      "command": "python3",
      "args": ["/Users/yourusername/.claude/plugins/kernel/claude-docs-server.py"]
    }
  }
}
```

### Windows Installation

**Using PowerShell:**

```powershell
# 1. Navigate to the kernel plugin
cd "$env:USERPROFILE\.claude\plugins\kernel"

# 2. Install Python dependencies
pip install requests
```

**Using Command Prompt:**

```cmd
:: 1. Navigate to the kernel plugin
cd "%USERPROFILE%\.claude\plugins\kernel"

:: 2. Install Python dependencies
pip install requests
```

**Configuration** - Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "claude-docs": {
      "command": "python",
      "args": ["C:\\Users\\yourusername\\.claude\\plugins\\kernel\\claude-docs-server.py"]
    }
  }
}
```

**Note for Windows**: Use `python` instead of `python3`, and use double backslashes (`\\`) in JSON paths, or forward slashes (`/`) which also work on Windows.

### Usage

Once configured, Claude Code can fetch documentation:

```
"What are the available hooks in Claude Code?"
→ Fetches and summarizes the hooks documentation
```

### Available Documentation Pages

The server can fetch these pages from docs.anthropic.com:

- `overview`, `quickstart`, `memory`
- `common-workflows`, `ide-integrations`
- `mcp`, `github-actions`, `sdk`
- `hooks`, `settings`, `slash-commands`
- `cli-reference`, `interactive-mode`
- `troubleshooting`, `security`, `costs`

---

## Troubleshooting

### "Command not found: /kernel-init"

**Cause**: The command file isn't in the right location.

**Fix**:
```bash
# Verify the file exists
ls -la .claude/commands/kernel-init.md

# If missing, copy it
cp ~/.claude/plugins/kernel/.claude/commands/kernel-init.md .claude/commands/
```

### "Could not find CODING-PROMPT-BANK.MD"

**Cause**: The prompt bank file isn't in any of the search locations.

**Fix**:
```bash
# Option 1: Copy to project root
cp ~/.claude/plugins/kernel/kernel/CODING-PROMPT-BANK.MD ./

# Option 2: Copy to global location
cp ~/.claude/plugins/kernel/kernel/CODING-PROMPT-BANK.MD ~/.claude/
```

### "KERNEL creates too many artifacts"

**Cause**: KERNEL is being too aggressive.

**Fix**: KERNEL should always ask before creating. If it's not:
1. Check `.claude/CLAUDE.md` has the "Ask first" guideline
2. Re-run `/kernel-init` to reset the configuration

### "MCP server not connecting"

**Cause**: Python path or permissions issue.

**Fix (macOS):**
```bash
# 1. Verify Python works
python3 --version

# 2. Check script permissions
chmod +x claude-docs-server.py

# 3. Test the server directly
echo '{"method": "tools/list"}' | python3 claude-docs-server.py

# 4. Use absolute path in .mcp.json
```

**Fix (Windows PowerShell):**
```powershell
# 1. Verify Python works
python --version

# 2. Test the server directly
echo '{"method": "tools/list"}' | python claude-docs-server.py

# 3. Ensure the path in .mcp.json uses double backslashes or forward slashes
```

**Fix (Windows cmd):**
```cmd
:: 1. Verify Python works
python --version

:: 2. Test the server directly
echo {"method": "tools/list"} | python claude-docs-server.py
```

### "Initialization detects wrong stack/tier"

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
