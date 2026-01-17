# KERNEL Plugin Meta Index

**Navigation hub for project metadata.** | v2.0.0

---

## Quick Access

| Path | Purpose |
|------|---------|
| [_session.md](./_session.md) | Session context, blockers, decisions |
| [_learnings.md](./_learnings.md) | Change log, problems, patterns |
| [context/active.md](./context/active.md) | Current work focus |
| [research/](./research/) | Investigation outputs |

---

## Structure

```
_meta/
├── INDEX.md              <- You are here
├── _session.md           <- Session tracking (read on start)
├── _learnings.md         <- Learnings log (append-only)
├── context/
│   └── active.md         <- Current work state
└── research/
    └── *.md              <- Investigation outputs
```

---

## Project Stats (v2.0.0)

| Component | Count | Location |
|-----------|-------|----------|
| Commands | 14 | `commands/` |
| Agents | 13 | `kernel/agents/` |
| Banks | 10 | `kernel/banks/` |
| Rules | 11 | `kernel/rules/` |
| Skills | 3 | `kernel/skills/` |

---

## How to Use

1. **Session start**: Read `_session.md` for context
2. **During work**: Update `context/active.md` as you go
3. **When learning**: Append to `_learnings.md` FIRST, then update configs
4. **Research outputs**: Write to `research/` directory
5. **Session end**: Update `_session.md`, archive `active.md` if needed

---

## Related

- `kernel/state.md` - KERNEL's project reality tracker
- `kernel/agents/` - Specialized agent templates
- `kernel/skills/` - Auto-triggered capabilities
- `kernel/rules/` - Foundational constraints
- `kernel/banks/` - Methodology templates
- `.claude/CLAUDE.md` - Project philosophy

---

*This index helps navigate the _meta system. Keep it current.*
