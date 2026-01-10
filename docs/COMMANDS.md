---
doc_kind: reference
depends_on: [commands/*.md, kernel/commands/*.md]
review_cadence: 30
last_reviewed: 2026-01-10
owners: ["@ariaxhan"]
---

# KERNEL Commands Reference

Complete reference for all KERNEL plugin commands. Commands are invoked with `/command-name` in Claude Code.

## Core Commands

### `/kernel-init`

Initialize KERNEL for any project.

**Purpose**: Analyzes your project and creates customized `.claude/CLAUDE.md` with detected tier, stack-specific coding rules, and KERNEL artifact templates.

**What it does**:
1. Detects project tier (T1 hackathon, T2 production, T3 critical)
2. Identifies stack (TypeScript, Python, Go, etc.)
3. Determines domain (API, CLI, library, app)
4. Creates directory structure (`.claude/commands/`, `.claude/agents/`, `.claude/skills/`, `.claude/rules/`)
5. Generates customized `.claude/CLAUDE.md`
6. Copies baseline artifacts (banks, commands, skills)

**When to use**: First time setting up KERNEL in a project.

**Example**:
```
/kernel-init
```

**Output**: Project analysis summary and list of created files.

---

### `/kernel-status`

Show KERNEL config health and staleness report.

**Purpose**: Display health status of all KERNEL configuration artifacts, showing which are active, stale, or new.

**What it shows**:
- Total config entries
- Active entries (referenced in last 7 days)
- Stale entries (no reference for 30+ days)
- New entries (< 7 days old)
- Reference counts per entry

**When to use**: Regular health checks to identify unused configuration.

**Example**:
```
/kernel-status
```

**Output**: Config health summary with statistics.

---

### `/kernel-prune`

Review and remove stale KERNEL config entries.

**Purpose**: Identify stale configuration artifacts (commands, agents, skills, rules) and prompt for removal.

**What it does**:
1. Scans all KERNEL artifacts
2. Identifies entries not referenced in 30+ days
3. Presents each stale entry with metadata
4. Prompts for confirmation before removal
5. Logs all removals for audit trail

**When to use**: Periodic cleanup to remove unused configuration.

**Example**:
```
/kernel-prune
```

**Output**: Interactive prompts for each stale entry.

---

## Methodology Commands

### `/discover`

Map codebase, find tooling, extract conventions.

**Purpose**: Activate discovery mode to systematically explore and document the project structure, tooling, and conventions.

**What it does**:
1. Reads `kernel/banks/DISCOVERY-BANK.md` for methodology
2. Reads `kernel/state.md` for current context
3. Inventories files and directories
4. Detects available tooling (linters, test runners, build tools)
5. Extracts naming conventions and patterns
6. Updates `kernel/state.md` with discoveries

**When to use**:
- First time exploring an unfamiliar codebase
- Before starting work on a new project
- When project structure has changed significantly

**Example**:
```
/discover
```

**Output**: Updated `kernel/state.md` with repo map, tooling inventory, and conventions.

---

### `/plan`

Get-it-right-first-time planning mode.

**Purpose**: Activate planning mode for systematic task analysis before implementation.

**What it does**:
1. Reads `kernel/banks/PLANNING-BANK.md` for methodology
2. Reads `kernel/state.md` for current context
3. Guides through: goal understanding, assumption extraction, pattern investigation, interface definition, mental simulation
4. Updates `kernel/state.md` with discoveries

**When to use**:
- Before implementing new features
- When approaching complex changes
- When multiple approaches are possible
- To avoid costly debugging cycles

**Example**:
```
/plan
```

**Output**: Structured implementation plan with verified assumptions.

---

### `/debug`

Systematic diagnosis and root cause fixing.

**Purpose**: Activate debugging mode for methodical problem diagnosis.

**What it does**:
1. Reads `kernel/banks/DEBUGGING-BANK.md` for methodology
2. Reads `kernel/state.md` for current context
3. Applies systematic debugging: reproduce, isolate, hypothesize, verify, fix
4. Updates `kernel/state.md` with findings

**When to use**:
- When encountering bugs or unexpected behavior
- When errors are intermittent or unclear
- For systematic root cause analysis

**Example**:
```
/debug
```

**Output**: Diagnosis with root cause and verified fix.

---

### `/review`

Correctness, consistency, completeness validation.

**Purpose**: Activate review mode for code quality validation.

**What it does**:
1. Reads `kernel/banks/REVIEW-BANK.md` for methodology
2. Reads `kernel/state.md` for current context
3. Applies review criteria: correctness, consistency, completeness, conventions, security
4. Reports findings with severity levels

**When to use**:
- Before committing code
- During PR review
- After implementing features
- For quality assurance

**Example**:
```
/review
```

**Output**: Review report with identified issues and recommendations.

---

### `/docs`

Documentation audit, generation, and maintenance.

**Purpose**: Activate documentation mode for systematic doc management.

**What it does**:
1. Reads `kernel/banks/DOCUMENTATION-BANK.md` for methodology
2. Reads `kernel/state.md` for current context (including `docs_style`)
3. If `docs_style` missing, detects from repo signals (REFERENCE, PROCEDURAL, or NARRATIVE)
4. Audits existing docs for: completeness, staleness, budget violations, orphans
5. Generates or refactors docs following style templates
6. Updates frontmatter and maintenance logs

**When to use**:
- Setting up documentation structure
- Auditing existing docs for issues
- Generating new documentation
- Ensuring docs stay current

**Example**:
```
/docs
```

**Output**: Documentation audit report with issues and fixes applied.

---

## Git Workflow Commands

### `/branch`

Create intention-focused branch for work.

**Purpose**: Create a properly named git branch based on the type of work.

**What it does**:
1. Checks current git status
2. Prompts for branch type (feat, fix, docs, refactor, test, chore)
3. Prompts for description
4. Creates and checks out branch with format: `<type>/<description>`
5. Updates `kernel/state.md` with branch metadata

**When to use**: Before starting any new work (NEVER WORK ON MAIN).

**Example**:
```
/branch
```

**Output**: New branch created and checked out.

---

### `/ship`

Ship branch - commit, push, and create PR.

**Purpose**: Complete the git workflow by committing changes, pushing, and opening a PR.

**What it does**:
1. Runs `git status` and `git diff` to analyze changes
2. Reviews commit history for message style
3. Generates commit message following conventions
4. Stages and commits changes
5. Pushes branch to remote
6. Creates PR with summary and test plan

**When to use**: When work is complete and ready for review.

**Example**:
```
/ship
```

**Output**: Commit created, branch pushed, PR URL returned.

---

### `/parallelize`

Set up git worktrees for parallel development.

**Purpose**: Configure git worktrees to work on multiple branches simultaneously.

**What it does**:
1. Detects if task benefits from parallel development
2. Creates worktree structure
3. Sets up separate directories for each branch
4. Provides guidance on coordination

**When to use**:
- Working on multiple related features
- Need to test changes in isolation
- Want to switch contexts without stashing

**Example**:
```
/parallelize
```

**Output**: Worktree structure created with setup instructions.

---

### `/handoff`

Generate context handoff for session continuation.

**Purpose**: Create a structured handoff brief for seamless conversation continuation across sessions or AI systems.

**What it does**:
1. Summarizes current work and context
2. Documents decisions made
3. Lists pending tasks
4. Captures important state
5. Provides continuation guidance

**When to use**:
- Ending a work session
- Switching to different task
- Preparing for team handoff
- Before significant context switch

**Example**:
```
/handoff
```

**Output**: Structured handoff document with context and next steps.

---

## Command Organization

Commands exist in two locations:

1. **Plugin commands** (`commands/*.md`): Core KERNEL commands that work across all projects
   - `/kernel-init`
   - `/kernel-status`
   - `/kernel-prune`

2. **Template commands** (`kernel/commands/*.md`): Methodology commands copied to projects during initialization
   - `/discover`
   - `/plan`
   - `/debug`
   - `/review`
   - `/docs`
   - `/branch`
   - `/ship`
   - `/parallelize`
   - `/handoff`

After running `/kernel-init`, template commands are copied to your project's `.claude/commands/` directory and become available for use.

---

## Command Naming Convention

All KERNEL commands follow these patterns:

- **Core plugin commands**: Prefixed with `kernel-` (e.g., `/kernel-init`, `/kernel-status`)
- **Methodology commands**: Short, verb-based names (e.g., `/plan`, `/debug`, `/review`)
- **Workflow commands**: Action-oriented (e.g., `/branch`, `/ship`)

---

## Adding Custom Commands

You can add project-specific commands by creating `.claude/commands/your-command.md`:

```markdown
---
description: One-line description of what this command does
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Your Command

Instructions for what Claude should do when `/your-command` is invoked.

1. Step by step instructions
2. Use clear, actionable language
3. Reference project-specific paths and conventions
```

Then invoke with `/your-command`.

---

## See Also

- [CONFIG-TYPES.md](../CONFIG-TYPES.md) - When to use commands vs agents vs skills vs rules
- [README.md](../README.md) - KERNEL overview and philosophy
- [SETUP.md](../SETUP.md) - Installation and configuration guide
- `kernel/banks/` - Methodology banks loaded by commands
