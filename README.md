# KERNEL

**Project Intelligence for Claude Code** | v2.0.0

KERNEL is a Claude Code plugin that creates tailored configuration for your project. It analyzes your codebase and builds configuration that fits - coding rules from your patterns, commands for workflows you repeat, agents for specialized tasks, hooks for tools you use. Methodology is applied automatically based on context, and session state persists across conversations.

---

## Why KERNEL?

Claude Code is powerful, but every project is different. KERNEL bridges this gap by:

1. **Analyzing your project** - stack, patterns, conventions
2. **Creating tailored config** - only what this project needs
3. **Spawning specialized agents** - test-runner, code-reviewer, security-scanner
4. **Applying methodology automatically** - no commands to remember
5. **Tracking session state** - context survives across conversations
6. **Evolving over time** - configuration grows as patterns emerge

---

## Quick Start

### 1. Install the Plugin

```
/install-plugin https://github.com/ariaxhan/kernel-plugin
```

### 2. Initialize Your Project

```bash
cd your-project
claude

# Inside Claude Code:
/kernel-init
```

KERNEL analyzes your project and creates:
- `.claude/CLAUDE.md` - Project-specific coding rules
- `.claude/agents/` - Specialized agents for your stack
- `.claude/rules/` - Patterns discovered in your codebase
- `_meta/` - Session tracking structure

### 3. Work Normally

Methodology applies automatically:
- **Implementing a feature?** KERNEL plans and researches first
- **Fixing a bug?** KERNEL debugs systematically
- **Writing code?** KERNEL spawns test-runner and type-checker
- **Before completing?** KERNEL reviews for correctness

No commands to remember. Just work.

---

## Agents (13)

KERNEL includes specialized agents that spawn proactively based on context.

### Fast Validation (Haiku)

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `test-runner` | Code written | Run tests, report failures |
| `type-checker` | TS/Python changes | Validate types |
| `lint-fixer` | Any code | Auto-fix lint issues |
| `build-validator` | Significant changes | Verify builds |
| `dependency-auditor` | package.json changes | Check CVEs, outdated |
| `git-historian` | "why" questions | Analyze git history |
| `git-sync` | End of response | Auto-commit and push |
| `metadata-sync` | End of response | Update active.md |

### Deep Analysis (Opus)

| Agent | Trigger | Purpose |
|-------|---------|---------|
| `code-reviewer` | Before commit | Find issues |
| `security-scanner` | Auth/input code | Find vulnerabilities |
| `test-generator` | New function | Generate tests |
| `api-documenter` | API changes | Update docs |
| `perf-profiler` | "slow" mentions | Profile bottlenecks |
| `refactor-scout` | "improve" mentions | Find opportunities |
| `migration-planner` | Major changes | Plan transitions |
| `frontend-stylist` | UI/CSS work | Design styles |
| `media-handler` | Image/video/audio | Process media |
| `database-architect` | Schema work | Design data layer |
| `debugger-deep` | Complex bugs | Root cause analysis |

Agents spawn automatically. Don't wait for permission.

---

## Skills (3)

Auto-triggered capabilities based on keywords.

| Skill | Triggers | Purpose |
|-------|----------|---------|
| `debug` | "bug", "error", "broken", "fix" | Systematic debugging methodology |
| `research` | "research", "investigate", "learn about" | Deep investigation mode |
| `coding-prompt-bank` | Project init, "coding rules" | Base AI coding philosophy |

---

## Commands (14)

### Setup
| Command | Purpose |
|---------|---------|
| `/kernel-init` | Initialize KERNEL for a project |
| `/kernel-user-init` | Set up user-level defaults |

### Development
| Command | Purpose |
|---------|---------|
| `/build` | Full pipeline: idea → research → plan → implement → validate |
| `/iterate` | Continuous improvement on existing code |
| `/tearitapart` | Critical review before implementing |
| `/validate` | Pre-commit gate: types + lint + tests |
| `/docs` | Documentation mode |

### Git Workflow
| Command | Purpose |
|---------|---------|
| `/branch` | Create worktree for isolated work |
| `/ship` | Commit, push, create PR |
| `/parallelize` | Set up multiple worktrees |
| `/release` | Version bump, tag, push |

### Maintenance
| Command | Purpose |
|---------|---------|
| `/kernel-status` | Show config health |
| `/kernel-prune` | Remove stale config entries |
| `/handoff` | Generate session continuation brief |

---

## Rules (11)

Foundational constraints applied across all work.

| Rule | Purpose |
|------|---------|
| `self-evolution` | **CRITICAL** - Update system when learning discovered |
| `commit-discipline` | Atomic, frequent, small commits |
| `investigation-first` | Search before implementing |
| `fail-fast` | Exit early, clear errors |
| `assumptions` | Extract and verify before executing |
| `methodology` | Auto-detect and apply approach |
| `invariants` | Non-negotiable contracts |
| `patterns` | Discovered coding patterns |
| `decisions` | Architecture decision log |
| `preferences` | Formatting, presentation, tool choices |
| `arbiter-syntax` | Pre-compact arbitration rules |

---

## Knowledge Banks (10)

Methodology templates that apply automatically based on context.

| Bank | When It Applies |
|------|-----------------|
| **PLANNING-BANK** | Before implementing features |
| **DEBUGGING-BANK** | When fixing bugs or errors |
| **RESEARCH-BANK** | Before writing new functionality |
| **REVIEW-BANK** | Before completing any task |
| **DISCOVERY-BANK** | First time in unfamiliar codebase |
| **ITERATION-BANK** | When refactoring or improving |
| **TEARITAPART-BANK** | Before implementing complex plans |
| **DOCUMENTATION-BANK** | When working on docs |
| **BUILD-BANK** | Full implementation pipeline |
| **CODING-PROMPT-BANK** | Core philosophy, tier requirements |

Banks are referenced automatically. You don't invoke them.

---

## Session Tracking

KERNEL maintains context across sessions with the `_meta/` structure:

```
_meta/
├── INDEX.md              # Navigation hub
├── _session.md           # Session context (blockers, decisions, infrastructure)
├── _learnings.md         # Change log (append-only, dated entries)
├── context/
│   └── active.md         # Current work state
└── research/
    └── *.md              # Investigation outputs
```

### Session Protocol

```
SESSION START:
1. Read _meta/_session.md for context
2. Read _meta/context/active.md for current work
3. Check kernel/state.md for project reality

DURING:
- Update active.md as you work
- Log learnings to _meta/_learnings.md immediately
- Spawn agents proactively

SESSION END:
- Update _meta/_session.md
- Commit and push (auto via @git-sync)
```

---

## Project Structure

```
kernel-plugin/
├── _meta/                 # Session tracking
│   ├── INDEX.md
│   ├── _session.md
│   ├── _learnings.md
│   ├── context/
│   └── research/
├── commands/              # 14 explicit commands
│   ├── kernel-init.md
│   ├── build.md
│   ├── validate.md
│   ├── iterate.md
│   ├── tearitapart.md
│   └── ...
├── kernel/
│   ├── agents/            # 13 agent templates
│   │   ├── test-runner.md
│   │   ├── code-reviewer.md
│   │   └── ...
│   ├── skills/            # 3 skill templates
│   │   ├── debug/
│   │   ├── research/
│   │   └── coding-prompt-bank/
│   ├── banks/             # 10 methodology banks
│   │   ├── PLANNING-BANK.md
│   │   ├── DEBUGGING-BANK.md
│   │   └── ...
│   ├── rules/             # 11 rule templates
│   │   ├── self-evolution.md
│   │   ├── commit-discipline.md
│   │   └── ...
│   └── state.md
├── sample-project/        # Example showing KERNEL in action
├── CONFIG-TYPES.md        # When to use each artifact type
└── SETUP.md               # Detailed installation guide
```

---

## Philosophy

### Automatic Methodology

KERNEL doesn't require you to type `/plan` or `/debug`. It detects context and applies the right approach:

| You're doing... | KERNEL automatically... |
|-----------------|-------------------------|
| Implementing new feature | Researches, plans, defines interfaces first |
| Fixing a bug | Reproduces, isolates, finds root cause |
| Refactoring | Understands deeply before changing |
| Writing code | Spawns test-runner, type-checker |
| Completing work | Reviews against requirements |

### Tailored, Not Templated

Every artifact is created because your project needs it:

```
Good: "Created test-runner because project has pytest"
Bad:  "Created test-runner because the template includes it"
```

### Self-Evolution

When you learn something, KERNEL captures it:

```
Learn → Log to _meta/_learnings.md → Update configs → Commit
```

Patterns compound. Mistakes don't repeat.

---

## Configuration Types

| I want Claude to... | Create... |
|---------------------|-----------|
| Follow rules on all tasks | `.claude/CLAUDE.md` or `.claude/rules/` |
| Run workflow when I say `/name` | `.claude/commands/name.md` |
| Auto-run on file write | Hook in `.claude/settings.json` |
| Delegate to specialist | `.claude/agents/name.md` |
| Auto-trigger on keywords | `.claude/skills/name/SKILL.md` |
| Connect to external service | `.mcp.json` entry |

See [CONFIG-TYPES.md](CONFIG-TYPES.md) for the complete guide.

---

## Requirements

- Claude Code CLI **v1.0.33+**
- Python 3.8+ (optional, for arbiter)

Works on macOS, Linux, and Windows.

---

## License

MIT

---

## Author

Aria Han — [github.com/ariaxhan](https://github.com/ariaxhan)
