# KERNEL Plugin Structure (v2.0.0)

**Complete project structure after v2.0.0 release.**

---

## Overview

KERNEL v2.0.0 is a complete development intelligence system with:
- 14 commands
- 13 agents
- 10 banks
- 11 rules
- 3 skills

---

## Full Structure

```
kernel-plugin/
├── .claude/                    # Project-level config
│   ├── CLAUDE.md              # Philosophy + session protocol
│   ├── rules/
│   │   └── preferences.md
│   └── settings.json
├── .claude-plugin/            # Plugin metadata
│   ├── plugin.json            # v2.0.0
│   └── marketplace.json
├── _meta/                     # Session tracking
│   ├── INDEX.md
│   ├── _session.md
│   ├── _learnings.md
│   ├── context/
│   │   └── active.md
│   └── research/
│       └── current-structure.md
├── commands/                  # 14 commands
│   ├── kernel-init.md
│   ├── kernel-user-init.md
│   ├── build.md
│   ├── docs.md
│   ├── branch.md
│   ├── ship.md
│   ├── parallelize.md
│   ├── release.md
│   ├── kernel-status.md
│   ├── kernel-prune.md
│   ├── handoff.md
│   ├── validate.md           # NEW in v2.0.0
│   ├── iterate.md            # NEW in v2.0.0
│   └── tearitapart.md        # NEW in v2.0.0
├── kernel/
│   ├── CLAUDE.md
│   ├── state.md
│   ├── agents/               # 13 agents (NEW in v2.0.0)
│   │   ├── test-runner.md
│   │   ├── type-checker.md
│   │   ├── lint-fixer.md
│   │   ├── build-validator.md
│   │   ├── dependency-auditor.md
│   │   ├── git-historian.md
│   │   ├── git-sync.md
│   │   ├── metadata-sync.md
│   │   ├── code-reviewer.md
│   │   ├── security-scanner.md
│   │   ├── test-generator.md
│   │   ├── api-documenter.md
│   │   ├── perf-profiler.md
│   │   ├── refactor-scout.md
│   │   ├── migration-planner.md
│   │   ├── frontend-stylist.md
│   │   ├── media-handler.md
│   │   ├── database-architect.md
│   │   └── debugger-deep.md
│   ├── skills/               # 3 skills (NEW in v2.0.0)
│   │   ├── debug/
│   │   │   └── SKILL.md
│   │   ├── research/
│   │   │   └── SKILL.md
│   │   └── coding-prompt-bank/
│   │       └── SKILL.md
│   ├── banks/                # 10 banks
│   │   ├── BUILD-BANK.md
│   │   ├── CODING-PROMPT-BANK.md
│   │   ├── DEBUGGING-BANK.md
│   │   ├── DISCOVERY-BANK.md
│   │   ├── DOCUMENTATION-BANK.md
│   │   ├── ITERATION-BANK.md
│   │   ├── PLANNING-BANK.md
│   │   ├── RESEARCH-BANK.md
│   │   ├── REVIEW-BANK.md
│   │   └── TEARITAPART-BANK.md
│   ├── rules/                # 11 rules
│   │   ├── methodology.md
│   │   ├── assumptions.md
│   │   ├── invariants.md
│   │   ├── patterns.md
│   │   ├── decisions.md
│   │   ├── preferences.md
│   │   ├── arbiter-syntax.md
│   │   ├── self-evolution.md      # NEW in v2.0.0
│   │   ├── commit-discipline.md   # NEW in v2.0.0
│   │   ├── investigation-first.md # NEW in v2.0.0
│   │   └── fail-fast.md           # NEW in v2.0.0
│   ├── hooks/
│   │   ├── pattern-capture.md
│   │   ├── post-write.md
│   │   ├── pre-complete.md
│   │   └── scripts/
│   │       └── precompact-arbiter.py
│   └── tools/
│       └── arbiter.py
├── sample-project/
├── memory/
│   └── config_registry.jsonl
├── CLAUDE.md
├── README.md
├── SETUP.md
├── CONFIG-TYPES.md
└── RELEASE_NOTES.md
```

---

## Agent Categories

### Fast Validation (Haiku)
| Agent | Purpose |
|-------|---------|
| test-runner | Run tests after code changes |
| type-checker | Validate types |
| lint-fixer | Auto-fix lint issues |
| build-validator | Verify builds |
| dependency-auditor | Check CVEs |
| git-historian | Analyze git history |
| git-sync | Auto-commit and push |
| metadata-sync | Update active.md |

### Deep Analysis (Opus)
| Agent | Purpose |
|-------|---------|
| code-reviewer | Find issues before commit |
| security-scanner | Find vulnerabilities |
| test-generator | Generate test cases |
| api-documenter | Update API docs |
| perf-profiler | Profile bottlenecks |
| refactor-scout | Find improvements |
| migration-planner | Plan transitions |
| frontend-stylist | Design UI styles |
| media-handler | Process media |
| database-architect | Design schemas |
| debugger-deep | Root cause analysis |

---

*Analysis conducted 2026-01-17 after v2.0.0 release*
