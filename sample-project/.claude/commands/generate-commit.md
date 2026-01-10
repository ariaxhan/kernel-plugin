---
description: Generate conventional commit message from staged changes
allowed-tools: Bash, Read
---

Generate a conventional commit message by analyzing staged changes:

1. Run `git diff --cached --stat` to see files changed
2. Run `git diff --cached` to see actual changes
3. Run `git log --oneline -10` to understand existing commit message style

Analyze the changes and generate a commit message following this format:

```
<type>(<scope>): <subject>

- Detailed change 1
- Detailed change 2
- Detailed change 3

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Type options:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `test`: Adding/updating tests
- `docs`: Documentation updates
- `style`: Formatting changes
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Scope**: Module or component affected (e.g., `encryption`, `sync`, `export`, `cli`)

**Subject**: Concise summary (imperative mood, lowercase, no period)

**Details**: Bullet points explaining WHY, not WHAT (changes are self-evident in diff)

**Guidelines:**
- Focus on user-facing impact and motivation
- Keep subject under 72 characters
- Use present tense ("add" not "added")
- Reference issue numbers if applicable
- Explain breaking changes if any

After generating, display the commit message and ask if the user wants to create the commit with this message.
