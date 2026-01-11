---
description: Unified planning and execution pipeline - from idea to working code
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, AskUserQuestion
---

# Build Command

Unified pipeline: **Idea → Plan → Implement → Validate → Done**

Use this for any project idea, prompt, or existing plan. Handles the full cycle.

---

## PHASE 0: INPUT DETECTION

Analyze what user provided:

**A) Raw idea/prompt** → Go to Phase 1 (Planning)
**B) Existing plan file** → Go to Phase 2 (Execution)
**C) Partial implementation** → Assess state, resume from appropriate phase

```
If .claude/plans/ contains relevant plan:
  → Ask: "Found existing plan. Resume execution or start fresh?"

If kernel/state.md mentions in-progress work:
  → Ask: "Found in-progress work. Continue or start new?"
```

---

## PHASE 1: PLANNING

### 1.1 Goal Extraction

Parse the input to extract:
```
GOAL: [What are we building?]
CONSTRAINTS: [Limitations, requirements, must-haves]
INPUTS: [What do we have to work with?]
OUTPUTS: [What should exist when done?]
DONE-WHEN: [How do we know it's complete?]
```

### 1.2 Assumption Extraction

List ALL assumptions across:
- Tech stack (languages, frameworks, versions)
- File locations (where code lives, where to create)
- Naming conventions (casing, patterns)
- Error handling approach
- Test expectations
- Dependencies

**STOP and confirm assumptions with user before proceeding.**

### 1.3 Investigation

Before designing:
```
1. Search for existing patterns: Glob + Grep for similar implementations
2. Read relevant files: Understand current architecture
3. Check dependencies: What's available? What needs installing?
4. Find working examples: Copy patterns, don't invent
```

### 1.4 Interface Design

Define contracts BEFORE implementation:
```
- Function signatures (inputs, outputs, errors)
- Data structures (types, schemas)
- API contracts (endpoints, payloads)
- File structure (what goes where)
```

### 1.5 Mental Simulation

Walk through the implementation mentally:
```
1. Trace happy path end-to-end
2. Identify edge cases
3. Spot potential failures
4. Verify integration points connect
```

### 1.6 Plan Output

Write plan to `.claude/plans/{feature-name}.md`:

```markdown
# Plan: {Feature Name}

## Goal
{goal statement}

## Done-When
- [ ] {criterion 1}
- [ ] {criterion 2}

## Assumptions (Confirmed)
{list confirmed assumptions}

## Implementation Steps
1. [ ] {step 1 - specific, actionable}
2. [ ] {step 2}
3. [ ] {step 3}
...

## Validation Steps
1. [ ] {test/check 1}
2. [ ] {test/check 2}

## Rollback Plan
{how to undo if things go wrong}

---
Created: {timestamp}
Status: READY FOR EXECUTION
```

**Ask user: "Plan ready. Proceed with execution?"**

---

## PHASE 2: EXECUTION

### 2.1 Setup

```
1. Create/switch to feature branch (if not on one)
2. Load plan into TodoWrite for tracking
3. Read kernel/state.md for context
4. Verify prerequisites (dependencies, tools)
```

### 2.2 Iterative Implementation

For each step in the plan:

```
BEFORE:
  - Mark step as in_progress in todo
  - State what you're about to do
  - Identify files to modify/create

DURING:
  - Make minimal, focused changes
  - One logical unit per commit
  - Follow existing patterns exactly

AFTER:
  - Verify change works (run relevant test/check)
  - Mark step as completed
  - Commit with conventional message
  - Update plan file with progress
```

### 2.3 Integration Checkpoints

After every 2-3 steps:
```
- Run test suite (if exists)
- Check for type errors (if typed language)
- Verify no regressions
- Confirm integration points still work
```

---

## PHASE 3: VALIDATION

### 3.1 Automated Checks

Run all applicable:
```bash
# Detect and run project's test suite
[ -f package.json ] && npm test
[ -f pyproject.toml ] && pytest
[ -f Cargo.toml ] && cargo test
[ -f go.mod ] && go test ./...

# Detect and run linters
[ -f .eslintrc* ] && npm run lint
[ -f pyproject.toml ] && ruff check . || flake8
[ -f rustfmt.toml ] && cargo fmt --check

# Detect and run type checks
[ -f tsconfig.json ] && npx tsc --noEmit
[ -f pyproject.toml ] && mypy . || true
```

### 3.2 Manual Verification

Walk through done-when criteria:
```
For each criterion in plan:
  - Verify it's actually met
  - Document how it was verified
  - If not met, add remediation step
```

### 3.3 Edge Case Check

```
Test at least 3 edge cases:
1. Empty/null input
2. Boundary conditions
3. Error/failure path
```

---

## PHASE 4: COMPLETION

### 4.1 Update State

Update `kernel/state.md`:
```
- What was built
- Key decisions made
- Any technical debt introduced
- Follow-up items (if any)
```

### 4.2 Update Plan

Mark plan as complete:
```markdown
---
Status: COMPLETED
Completed: {timestamp}
---
```

### 4.3 Final Report

Output summary:
```
BUILD COMPLETE

Feature: {name}
Branch: {branch-name}
Commits: {count}

Files Changed:
  - {file1}: {what changed}
  - {file2}: {what changed}

Validation:
  - Tests: {pass/fail/skip}
  - Lint: {pass/fail/skip}
  - Types: {pass/fail/skip}
  - Done-when: {all criteria met}

Next Steps:
  - [ ] Review changes: git diff main
  - [ ] Create PR: /ship
  - [ ] {any follow-up items}
```

---

## FAILURE HANDLING

### If implementation fails:
```
1. STOP immediately
2. Document what failed and why
3. Rollback to last known good state
4. Update plan with findings
5. Ask user: "Continue with modified approach or pause?"
```

### If tests fail:
```
1. Identify failing test
2. Diagnose: is it the code or the test?
3. Fix the root cause (not symptoms)
4. Re-run full validation
```

### If blocked:
```
1. Document the blocker
2. List what's needed to unblock
3. Ask user for input
4. Do NOT guess or work around silently
```

---

## USAGE EXAMPLES

```
# From raw idea
/build "Add user authentication with JWT"

# From existing plan
/build .claude/plans/auth-feature.md

# Resume interrupted work
/build --resume

# Quick mode (skip confirmations)
/build --quick "Add a logout button"
```

---

## BEHAVIOR FLAGS

- **Default**: Full flow with confirmations at each phase gate
- **--quick**: Skip assumption confirmation, minimal prompts
- **--plan-only**: Stop after Phase 1, don't execute
- **--resume**: Detect and continue in-progress work
- **--validate-only**: Skip to Phase 3, run checks on current state
