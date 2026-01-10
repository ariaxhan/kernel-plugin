# Documentation Templates

## REFERENCE Style Template

```markdown
---
doc_kind: reference
depends_on:
  - src/path/to/source.ts
review_cadence: 90
last_reviewed: YYYY-MM-DD
owners: ["@username"]
---

# Component Name
One-sentence purpose. Use when: [specific need]. Avoid when: [anti-use case].

## Overview

Brief context. What this does, why it exists. 2-3 paragraphs max.

## API

### functionName(param1, param2)

Brief description of what this does.

**Parameters:**
- `param1` (type): Description
- `param2` (type, optional): Description. Default: `value`

**Returns:** type - Description

**Example:**
\`\`\`typescript
const result = functionName('value', { option: true });
\`\`\`

### anotherFunction()

[Repeat pattern]

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `key` | string | `null` | What it controls |

## See Also

- [Related component](./related.md)
- [Parent module](../index.md)
- [How to use this](../how-to/use-component.md)
```

---

## PROCEDURAL Style Template

```markdown
---
doc_kind: how-to
depends_on:
  - src/cli/command.ts
  - config/schema.json
review_cadence: 60
last_reviewed: YYYY-MM-DD
owners: ["@username"]
---

# Task Name
One-sentence goal. Use when: [situation]. Avoid when: [wrong situation].

## Prerequisites

- Requirement 1
- Requirement 2
- [Setup guide](./setup.md) completed

## Steps

### 1. First Action

What to do. Why (brief).

\`\`\`bash
command --flag value
\`\`\`

Expected: Description of successful result.

### 2. Second Action

What to do.

\`\`\`bash
next-command
\`\`\`

Expected: What you should see.

### 3. Verify

How to confirm success.

## Common Failures

### Error: Specific message

**Cause:** Why this happens.
**Fix:** What to do.

### Error: Another message

**Cause:** Why.
**Fix:** Steps to resolve.

## See Also

- [Next task](./next-task.md)
- [Related reference](../reference/component.md)
- [Troubleshooting](./troubleshooting.md)
```

---

## NARRATIVE Style Template

```markdown
---
doc_kind: explanation
depends_on: []
review_cadence: 120
last_reviewed: YYYY-MM-DD
owners: ["@username"]
---

# Concept Name
One-sentence essence. Use when: [need mental model]. Avoid when: [just need to do X].

## Key Points

- Point 1: Core insight (one line)
- Point 2: Second insight (one line)
- Point 3: Third insight (one line)

## Context

Why this exists. What problem it solves. Historical context if relevant.

The relationship to other concepts. How it fits in the larger system.

## How It Works

Mechanics explained. Diagrams if they add clarity.

Walk through the flow or process. Use concrete examples.

## Tradeoffs

What we chose and why:
- Decision 1: Rationale
- Decision 2: Rationale

What we didn't choose:
- Alternative A: Why not
- Alternative B: Why not

## See Also

- [Related concept](./related-concept.md)
- [Implementation details](../reference/implementation.md)
- [How to apply this](../how-to/apply-concept.md)
```

---

## Reading Path Template

```markdown
---
doc_kind: how-to
depends_on: []
review_cadence: 60
last_reviewed: YYYY-MM-DD
owners: ["@username"]
---

# Path: [Goal]
Curated path for [audience] who want to [outcome].

## Start Here

Brief orientation. What you'll learn.

## Steps

1. **[First milestone](../how-to/first.md)** - What you'll accomplish
2. **[Second milestone](../reference/second.md)** - What you'll learn
3. **[Third milestone](../how-to/third.md)** - Final capability

## After This Path

You can now:
- Capability 1
- Capability 2

Next paths:
- [Advanced path](./advanced.md)
- [Related path](./related.md)
```

---

## Index Template

```markdown
# Documentation

## Quick Links

- [Quickstart](./paths/quickstart.md) - Get running in 5 minutes
- [Concepts](./paths/concepts.md) - Understand the mental model
- [Troubleshooting](./paths/troubleshooting.md) - Fix common issues

## Tutorials

- [Getting Started](./tutorials/getting-started.md)

## How-To Guides

- [Task A](./how-to/task-a.md)
- [Task B](./how-to/task-b.md)

## Reference

- [API](./reference/api.md)
- [Configuration](./reference/config.md)
- [CLI](./reference/cli.md)

## Explanation

- [Architecture](./explanation/architecture.md)
- [Design Decisions](./explanation/decisions.md)

---

[Maintenance Log](./MAINTENANCE.md)
```
