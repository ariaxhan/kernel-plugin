# KERNEL Git Workflow Architecture

## Core Principles

1. **Never work on main** - All work happens on intention-focused branches
2. **GitHub is the changelog** - Commit history IS the documentation of change
3. **Branches have purpose** - Every branch declares its intention upfront
4. **Auto-commit on completion** - No orphaned work, no forgotten commits
5. **Push with intention** - Auto-push when ready, with approval gate

---

## Branch Naming Convention

```
<type>/<scope>-<description>

Types:
  feat/     - New feature
  fix/      - Bug fix
  docs/     - Documentation only
  refactor/ - Code restructure, no behavior change
  test/     - Test additions/changes
  chore/    - Maintenance, deps, config
  exp/      - Experiment (may be discarded)

Examples:
  feat/auth-oauth-login
  fix/api-rate-limit-crash
  docs/readme-installation
  refactor/db-connection-pool
  exp/try-new-cache-strategy
```

---

## Hooks Architecture

### 1. Session Start Hook

```yaml
# .claude/settings.json
hooks:
  SessionStart:
    - type: command
      command: kernel-git-check
```

**kernel-git-check** does:
- Verify not on main/master
- If on main: prompt to create branch or switch
- Show current branch intention
- Show uncommitted changes from last session

### 2. Pre-Write Hook (Protection)

```yaml
hooks:
  PreToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: kernel-branch-guard
```

**kernel-branch-guard** does:
- Block writes to main (configurable)
- Warn if branch intention doesn't match file being modified
- Track files modified this session

### 3. Post-Write Hook (Auto-Stage)

```yaml
hooks:
  PostToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: git add $CLAUDE_FILE_PATHS
```

### 4. Session End / Task Complete Hook

```yaml
hooks:
  TaskComplete:
    - type: command
      command: kernel-auto-commit
```

**kernel-auto-commit** does:
- Generate commit message from work done
- Commit staged changes
- If `auto_push` enabled: push to origin
- If `auto_pr` enabled: create draft PR

---

## Commands

### /branch - Create Focused Branch

```markdown
---
description: Create intention-focused branch
allowed-tools: Bash, AskUserQuestion
---

1. If uncommitted changes exist, commit first
2. Ask for branch type (feat/fix/docs/refactor/test/chore/exp)
3. Ask for scope (module/area affected)
4. Ask for description (2-4 words)
5. Create branch: `git checkout -b <type>/<scope>-<description>`
6. Record intention in state.md
7. Push branch: `git push -u origin <branch>`
```

### /commit - Smart Commit

```markdown
---
description: Generate commit from session work
allowed-tools: Bash, Read
---

1. Read git diff --staged
2. Read session context (what was accomplished)
3. Generate conventional commit message:
   - type(scope): description
   - Body with bullet points of changes
   - Refs if applicable
4. Show message, ask for approval
5. Commit
6. If auto_push: push
```

### /ship - Push and PR

```markdown
---
description: Ship branch - push and create PR
allowed-tools: Bash
---

1. Ensure all changes committed
2. Push to origin
3. Generate PR description from commit history
4. Create PR via gh cli
5. Return PR URL
6. Optionally: switch back to main, create new branch for next task
```

### /sync - Update from Main

```markdown
---
description: Sync branch with main
allowed-tools: Bash
---

1. Stash any uncommitted changes
2. Fetch origin
3. If on feature branch: rebase onto main
4. If conflicts: report and pause
5. Pop stash
6. Report status
```

---

## State Schema Addition

```yaml
# In kernel/state.md

## Git Workflow State
current_branch: null
branch_intention: null       # What this branch is for
branch_created: null         # ISO date
files_modified_session: []   # Files touched this session
commits_this_branch: 0
last_commit: null            # ISO date
auto_commit: true            # Auto-commit on task complete
auto_push: false             # Requires explicit /ship
require_branch: true         # Block work on main
```

---

## Settings

```json
{
  "kernel": {
    "git": {
      "require_branch": true,
      "auto_stage": true,
      "auto_commit": true,
      "auto_push": false,
      "commit_style": "conventional",
      "branch_prefixes": ["feat", "fix", "docs", "refactor", "test", "chore", "exp"],
      "protected_branches": ["main", "master", "production"],
      "co_author": "Claude <noreply@anthropic.com>"
    }
  }
}
```

---

## Workflow Example

```
User: "Add OAuth authentication"

KERNEL:
  1. Detects on main → prompts to create branch
  2. User confirms → creates feat/auth-oauth
  3. Work happens on branch
  4. Each file write auto-staged
  5. Task complete → auto-commit with message:
     "feat(auth): add OAuth authentication

     - Add OAuth provider configuration
     - Implement token exchange flow
     - Add session management
     - Update user model with OAuth fields

     Co-Authored-By: Claude <noreply@anthropic.com>"
  6. User says "ship it" or runs /ship
  7. Push + PR created
  8. KERNEL asks: "Create new branch for next task?"
```

---

## Integration with /parallelize

When `/parallelize` creates worktrees:

```
main-repo/                    # Stay on main for coordination
├── ../repo-feat-oauth/       # Worktree on feat/auth-oauth
├── ../repo-feat-billing/     # Worktree on feat/billing-stripe
└── ../repo-feat-notify/      # Worktree on feat/notify-email

Each worktree:
- Has its own branch with focused intention
- Auto-commits independently
- Ships independently
- Merges to main via PR
```

---

## Changelog Generation

Since git IS the changelog:

```bash
# Generate changelog from git history
git log main..HEAD --pretty=format:"- %s" --reverse

# Or for release notes:
git log v1.0.0..v1.1.0 --pretty=format:"### %s%n%b" --reverse
```

**KERNEL can auto-generate:**
- CHANGELOG.md from git history
- Release notes from tags
- PR descriptions from branch commits

---

## Safety Rails

1. **Protected branch detection** - Never push directly to main/master/production
2. **Uncommitted work warning** - Alert on session start if stale changes
3. **Branch age tracking** - Warn if branch older than 7 days without merge
4. **Conflict detection** - Check for conflicts before work starts
5. **Force push prevention** - Never force push unless explicitly requested

---

## Questions for Design

1. Should auto-commit happen after each task or only on session end?
2. Should we track "work sessions" as a concept separate from branches?
3. How granular should commit messages be? (per-file vs per-task vs per-session)
4. Should we integrate with GitHub Issues for branch linking?
5. What's the approval UX for auto-push? (confirm each time vs trust mode)

---

## Implementation Priority

1. **Phase 1**: Branch protection + /branch command
2. **Phase 2**: Auto-stage + /commit command
3. **Phase 3**: /ship command + PR generation
4. **Phase 4**: Full hooks integration
5. **Phase 5**: Changelog generation from history
