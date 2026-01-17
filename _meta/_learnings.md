# KERNEL Plugin Learnings

tokens: ~400 | type: log | append-only

---

**Living log of everything we learn while developing this plugin.** Every insight, pattern, gotcha, and fix gets captured here then routed to appropriate configs.

## Format

```markdown
## {date}
**Context:** {feature/component}
**Type:** pattern | gotcha | fix | optimization | problem
**Changed:** {file path or N/A}
**What:** {brief description}
**Why:** {rationale}
**Applied to:** {which rules/banks/configs updated}
```

## Learnings

<!-- append new learnings here, newest at top -->

## 2026-01-17 (v2.0.0 Release)

**Context:** Major version release
**Type:** pattern
**Changed:** 32 files, +2048 lines
**What:** Released v2.0.0 with agents, skills, comprehensive rules, and new commands
**Why:** KERNEL needed to be a complete development intelligence system, not just configuration scaffolding. CodingVault had proven patterns (19 agents, 5 rules, 6 commands, 3 skills) that were missing from KERNEL.
**Applied to:**
- `kernel/agents/` - 13 new agent templates
- `kernel/skills/` - 3 skill templates (debug, research, coding-prompt-bank)
- `kernel/rules/` - 4 new rules (self-evolution, commit-discipline, investigation-first, fail-fast)
- `commands/` - 3 new commands (validate, iterate, tearitapart)
- `README.md` - Complete rewrite for v2.0.0
- `RELEASE_NOTES.md` - v2.0.0 release notes

---

## 2026-01-17 (v1.6.0)

**Context:** Session tracking
**Type:** pattern
**Changed:** Created _meta/ structure
**What:** Aligned with CodingVault _meta system for session tracking and learnings
**Why:** Need centralized logging of changes, problems, decisions. Session context must persist across conversations.
**Applied to:** _meta/_session.md, _meta/_learnings.md, _meta/context/active.md, _meta/INDEX.md, .claude/CLAUDE.md

---

## 2026-01-17 (Agent Patterns)

**Context:** Agent design
**Type:** pattern
**Changed:** kernel/agents/*.md
**What:** Two-tier agent model: Haiku for fast validation, Opus for deep analysis
**Why:** Fast agents (test-runner, type-checker, lint-fixer) should use cheaper/faster model. Deep analysis (code-reviewer, security-scanner, debugger-deep) needs reasoning power.
**Applied to:** All 13 agents have explicit `model: haiku` or `model: opus` in frontmatter

---

## 2026-01-17 (Auto-Sync Pattern)

**Context:** Session management
**Type:** pattern
**Changed:** kernel/agents/git-sync.md, kernel/agents/metadata-sync.md
**What:** Two agents auto-spawn at end of every response: @git-sync and @metadata-sync
**Why:** Eliminates manual git commits and metadata updates. State is always current with zero lag.
**Applied to:** git-sync.md, metadata-sync.md agents

---

*This file is the source of truth for project evolution. When we learn, we log here FIRST, then update configs.*
