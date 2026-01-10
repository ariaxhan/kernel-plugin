---
doc_kind: explanation
depends_on: []
review_cadence: 90
last_reviewed: 2026-01-10
owners: ["@ariaxhan"]
---

# Context Levels in Claude Code

Understanding the three levels of context and how they interact.

## The Three Levels

Claude Code operates with a hierarchy of configuration contexts:

```
System (global)
  ↓
User (all your projects)
  ↓
Project (specific project)
```

Each level can override or extend the previous level.

---

## 1. System Level (Global)

**Location**: Claude Code installation directory
**Purpose**: Default behavior for all users on the system
**Managed by**: Claude Code developers (not you)

**What's here**:
- Core tool definitions (Read, Write, Bash, etc.)
- Default model settings
- System-wide security constraints

**Access**: Read-only, cannot modify

**View**:
```bash
# Installation location varies by system
# macOS/Linux: typically in /usr/local/bin/claude or similar
# You rarely need to look at this
```

---

## 2. User Level (Your Personal Defaults)

**Location**: `~/.claude/`
**Purpose**: Your preferences across ALL projects
**Managed by**: You

**What belongs here**:
- Your personal coding style preferences
- MCP servers you use across projects
- Plugins you always want enabled
- Your personal CLAUDE.md (baseline philosophy)
- Reusable commands/agents/skills you use everywhere

**Structure**:
```
~/.claude/
├── settings.json         # Your global settings
├── CLAUDE.md             # Your baseline coding philosophy
├── commands/             # Commands available in all projects
├── agents/               # Agents available in all projects
├── skills/               # Skills available in all projects
└── rules/                # Rules you follow in all projects
```

**View current user settings**:
```bash
# See all files
ls -la ~/.claude/

# View settings
cat ~/.claude/settings.json

# View your baseline philosophy
cat ~/.claude/CLAUDE.md
```

**Example user-level settings** (`~/.claude/settings.json`):
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
  },
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"]
    }
  }
}
```

**Example user-level CLAUDE.md** (`~/.claude/CLAUDE.md`):
```markdown
# My Coding Baseline

**Personal Philosophy**:
- Clarity over cleverness
- Tests before implementation
- Comments explain why, not what
- Commit often, push daily

**Tools I Use**:
- TypeScript strict mode
- Prettier for formatting
- ESLint for linting
- Jest for testing

**Conventions**:
- camelCase for functions
- PascalCase for classes
- kebab-case for files
```

---

## 3. Project Level (Project-Specific)

**Location**: `<project>/.claude/` or `<project>/kernel/` (KERNEL style)
**Purpose**: Project-specific overrides and additions
**Managed by**: Project team (committed to git)

**What belongs here**:
- Project-specific tier, stack, domain
- Project architecture constraints
- Project-specific commands/agents/skills
- Project conventions (different from your personal defaults)
- Team-shared configuration

**KERNEL uses**:
```
project/
├── CLAUDE.md             # Project-specific philosophy
└── kernel/
    ├── state.md          # Project world model
    ├── banks/            # Methodology banks (copied from plugin)
    ├── commands/         # All commands (copied from plugin)
    ├── hooks/            # Hook templates
    └── rules/            # Project-specific rules
```

**View current project context**:
```bash
# See what's in the project
ls -la .claude/  # or kernel/

# View project philosophy
cat CLAUDE.md

# View project state
cat kernel/state.md

# View project rules
ls -la kernel/rules/
```

**Example project-level CLAUDE.md**:
```markdown
# E-Commerce API

TIER: 2 (Production-grade)
STACK: TypeScript, Express, PostgreSQL
DOMAIN: REST API

**PROJECT CONSTRAINTS**:
- All endpoints must have rate limiting
- Database queries must use parameterized statements
- Secrets via AWS Secrets Manager only
- No direct database access (use ORM)

**TEAM CONVENTIONS**:
- API versioning: /v1/, /v2/
- Error codes: APP-XXX format
- Logging: JSON structured logs
- Tests: >80% coverage required
```

---

## How Contexts Merge

Configuration flows from System → User → Project, with each level able to override or extend the previous:

```
System (base)
  + User (your additions/overrides)
    + Project (team additions/overrides)
      = Final Context
```

### Example Merge

**System** provides:
- Core tools (Read, Write, Bash)
- Default model (sonnet)

**User** adds:
- CLAUDE.md with "Always write tests first"
- Enabled KERNEL plugin
- Personal MCP server (postgres)

**Project** adds:
- CLAUDE.md with "TIER: 3, zero tolerance for errors"
- Project-specific commands (/deploy)
- Project rules (no direct DB access)

**Final context** Claude sees:
- ✅ Core tools (from System)
- ✅ Default model (from System)
- ✅ "Always write tests first" (from User)
- ✅ KERNEL plugin enabled (from User)
- ✅ Postgres MCP (from User)
- ✅ "TIER: 3" philosophy **overrides** user baseline (from Project)
- ✅ `/deploy` command (from Project)
- ✅ No direct DB access (from Project)

### Override Rules

1. **settings.json**: Project settings **merge with** user settings
   - Both MCP servers available
   - Both plugins enabled
   - Project hooks override user hooks (same matcher)

2. **CLAUDE.md**: Project CLAUDE.md **replaces** user CLAUDE.md
   - Only project philosophy is active
   - User philosophy ignored in this project

3. **Commands/Agents/Skills**: Both levels **available**
   - User commands: `/my-personal-command`
   - Project commands: `/project-specific-command`
   - Both work

4. **Rules**: Both levels **active**
   - User rules apply
   - Project rules also apply
   - If conflict, project wins

---

## View All Active Context

To see what Claude sees in the current session:

### 1. Check User Context

```bash
# User settings
cat ~/.claude/settings.json

# User philosophy
cat ~/.claude/CLAUDE.md

# User commands available everywhere
ls ~/.claude/commands/

# User MCP servers
jq '.mcpServers' ~/.claude/settings.json
```

### 2. Check Project Context

```bash
# Project philosophy (overrides user)
cat CLAUDE.md

# Project state
cat kernel/state.md

# Project commands
ls kernel/commands/

# Project settings
cat .claude/settings.json  # if exists
```

### 3. See Merged MCP Servers

```bash
# User-level
jq '.mcpServers' ~/.claude/settings.json

# Project-level
jq '.mcpServers' .mcp.json

# Both are active in this project
```

### 4. See All Available Commands

```bash
# User commands
ls ~/.claude/commands/

# Project commands (KERNEL)
ls kernel/commands/

# Plugin commands (KERNEL)
# Available after plugin installed
```

---

## Management Best Practices

### What Goes Where?

| Type | User Level | Project Level |
|------|-----------|---------------|
| **Personal coding style** | ✅ Yes | ❌ No |
| **Project architecture** | ❌ No | ✅ Yes |
| **Tier/Stack/Domain** | ❌ No | ✅ Yes (in CLAUDE.md) |
| **MCP servers for personal use** | ✅ Yes | ❌ No |
| **MCP servers team needs** | ❌ No | ✅ Yes |
| **Commands you use everywhere** | ✅ Yes | ❌ No |
| **Commands project-specific** | ❌ No | ✅ Yes |
| **KERNEL plugin** | ✅ Yes (enable once) | ✅ Yes (run /init per project) |
| **General coding principles** | ✅ Yes | ❌ No |
| **Project constraints** | ❌ No | ✅ Yes |

### KERNEL Context Strategy

KERNEL follows this pattern:

**User level** (`~/.claude/`):
- Enable KERNEL plugin once
- Keep empty or minimal (let projects define themselves)

**Project level** (`kernel/`):
- Run `/init` to create project-specific config
- Customize CLAUDE.md for project tier/stack
- Add project-specific rules as they emerge
- Commit to git so team shares context

**Why**: Projects vary widely (tier, stack, domain). User level stays lean, project level captures reality.

---

## Common Scenarios

### Scenario 1: New Project, First Time

```bash
# 1. Enable KERNEL at user level (once)
/plugin  # Install KERNEL plugin

# 2. In new project, initialize
cd my-new-project
/init

# Result:
# - User: KERNEL plugin enabled
# - Project: CLAUDE.md, kernel/state.md, banks, commands created
```

### Scenario 2: Joining Existing Project

```bash
# 1. Clone project
git clone https://github.com/team/project
cd project

# 2. Trust the project (if .claude/ exists)
# Claude Code will prompt

# 3. Start Claude
claude

# Result:
# - Your user settings active
# - Project settings active
# - Both contexts merged
```

### Scenario 3: Personal MCP Server for All Projects

```bash
# Add to ~/.claude/settings.json
{
  "mcpServers": {
    "my-database": {
      "command": "npx",
      "args": ["-y", "@me/my-db-server"]
    }
  }
}

# Now available in ALL projects
# No need to configure per-project
```

### Scenario 4: Project Needs Specific MCP Server

```bash
# Add to project/.mcp.json (committed to git)
{
  "mcpServers": {
    "team-database": {
      "command": "npx",
      "args": ["-y", "@company/postgres-server"]
    }
  }
}

# Now available for all team members in this project
```

---

## Inspect Active Context (Commands)

Create a command to show current context:

**User**: `~/.claude/commands/show-context.md`
```markdown
---
description: Show all active context levels
allowed-tools: Read, Bash
---

# Show Context

Display user and project context currently active.

## User Context
```bash
echo "=== USER SETTINGS ==="
cat ~/.claude/settings.json 2>/dev/null || echo "No user settings"

echo -e "\n=== USER CLAUDE.md ==="
cat ~/.claude/CLAUDE.md 2>/dev/null || echo "No user CLAUDE.md"

echo -e "\n=== USER COMMANDS ==="
ls ~/.claude/commands/ 2>/dev/null || echo "No user commands"
```

## Project Context
```bash
echo -e "\n=== PROJECT CLAUDE.md ==="
cat CLAUDE.md 2>/dev/null || echo "No project CLAUDE.md"

echo -e "\n=== PROJECT STATE ==="
cat kernel/state.md 2>/dev/null || echo "No project state"

echo -e "\n=== PROJECT COMMANDS ==="
ls kernel/commands/ 2>/dev/null || echo "No project commands"
```

## Active MCP Servers
```bash
echo -e "\n=== USER MCP SERVERS ==="
jq '.mcpServers // {}' ~/.claude/settings.json 2>/dev/null || echo "No user MCP"

echo -e "\n=== PROJECT MCP SERVERS ==="
jq '.mcpServers // {}' .mcp.json 2>/dev/null || echo "No project MCP"
```
```

Now you can run `/show-context` in any project to see all active layers.

---

## Troubleshooting

### "Why isn't my user CLAUDE.md being used?"

Project CLAUDE.md **replaces** user CLAUDE.md. This is intentional - projects define their own tier/stack.

**Solution**: Keep user CLAUDE.md minimal (general principles). Let projects define specifics.

### "My user command isn't working in this project"

Check if project has same command name - project commands override user commands.

**Solution**: Use unique names for user commands (e.g., `/my-deploy` vs `/deploy`).

### "MCP server not showing up"

1. Check user settings: `cat ~/.claude/settings.json`
2. Check project settings: `cat .mcp.json`
3. Restart Claude Code after changes

### "Which CLAUDE.md is active?"

If project has `CLAUDE.md`, that's active (user ignored).
If no project CLAUDE.md, user CLAUDE.md is active.

**Check**:
```bash
# Project has CLAUDE.md?
ls CLAUDE.md

# If yes: project is active
# If no: user ~/.claude/CLAUDE.md is active
```

---

## See Also

- [README.md](../README.md) - KERNEL overview
- [COMMANDS.md](./COMMANDS.md) - Command reference
- [CONFIG-TYPES.md](../CONFIG-TYPES.md) - Artifact types guide
- Claude Code docs - Settings and configuration
