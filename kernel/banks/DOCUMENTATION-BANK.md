# Documentation Bank

## Philosophy
Every word: liability. Missing concept: also liability. Balance.
Scannable surface, depth on demand. Docs are code.

---

## Two-Axis System

**Kind** (purpose, per doc):
| Kind | Reader |
|------|--------|
| tutorial | "Teach me" |
| how-to | "Help me do X" |
| reference | "Details please" |
| explanation | "Help me understand" |

**Style** (format, per repo - set once):
| Style | Signal |
|-------|--------|
| REFERENCE | APIs, exports, JSDoc |
| PROCEDURAL | CLI, config, setup |
| NARRATIVE | ADRs, architecture |

---

## Frontmatter

```yaml
---
doc_kind: how-to
depends_on: [src/file.ts]
review_cadence: 60
last_reviewed: 2026-01-10
owners: ["@user"]
---
```

## Line 2 Rule

```
# Title
Purpose. Use when: X. Avoid when: Y.
```

---

## Budgets

| Metric | Target | Max |
|--------|--------|-----|
| Lines | 150 | 220 |
| Headings | 8 | 12 |
| Code block | 15 | 30 |
| See Also | 3 | 7 |

Exceed max → document exception in state.md.

---

## Structure

- H1: one (title)
- H2: sections
- H3: sparingly
- H4+: never
- Footer: `## See Also` required
- Names: `kebab-case.md`
- No orphans

---

## Staleness

**Immediate**: depends_on modified
**Cadence**: 60d how-to, 90d reference, 120d explanation
**Release**: version bump, breaking change

---

## Anti-Patterns

- "This document explains..."
- "You might be wondering..."
- Prerequisites > 3
- Inline TOCs

---

## Templates (compact)

**REFERENCE**:
```
# Name
Purpose. Use/Avoid.
## Overview
## API
### func(p) → returns
## See Also
```

**PROCEDURAL**:
```
# Task
Purpose. Use/Avoid.
## Prerequisites (max 3)
## Steps
### 1. Action → result
## Failures
### Error → cause, fix
## See Also
```

**NARRATIVE**:
```
# Concept
Purpose. Use/Avoid.
## Key Points (3 bullets)
## Context
## How It Works
## Tradeoffs
## See Also
```

---

## Slots

### docs_style
[Set once, lock. Record selection rationale in state.md]

### exceptions
[Budget violations with rationale]

---

⚠️ Full templates: `docs/documentation-files/doc-templates.md`
Scripts: `docs/documentation-files/docs-staleness-check.sh`
