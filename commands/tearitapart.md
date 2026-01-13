---
description: Critical review mode - world-class developer tears your plan apart before you write code
---

# Tear It Apart Mode

Entering CRITICAL REVIEW mode.

1. Read `kernel/banks/TEARITAPART-BANK.md` for methodology
2. Read `kernel/state.md` for current context
3. Read the plan at `.claude/plans/{feature-name}.md`
4. Read research at `.claude/research/{feature-name}-research.md` if exists
5. Apply critical review: question every decision, find long-term issues
6. Create `.claude/reviews/{feature-name}-teardown.md` with findings
7. Update `kernel/state.md` with any patterns discovered

You are a world-class senior engineer who has never seen this codebase. Find what could go wrong.

**Core principle:** Find every potential issue that could cause long-term pain. Not nitpicks - real problems.
