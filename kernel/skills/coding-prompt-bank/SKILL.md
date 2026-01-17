---
name: coding-prompt-bank
description: Base rules and behaviors for AI coding agents. Trigger on starting a coding project, "use my coding rules", "coding agent setup", "initialize project", "new codebase", or when providing instructions to any coding agent.
---

# Coding Prompt Bank

Core philosophy and tier-based requirements for AI coding.

## Philosophy

```
CORRECTNESS > SPEED
Working first attempt beats fast iteration + debug.
Mental simulation catches 80% of bugs before execution.

EVERY LINE IS LIABILITY
Config > code. Native > custom. Existing > new.
Delete what doesn't earn its place.

PARSE, DON'T READ
Grep. Find. Read signatures first.
Never ask for overview—discover it.
```

## Project Tiers

### Tier 1: Hackathon/Prototype
- Speed matters most
- Skip tests unless critical path
- Minimal documentation
- Technical debt acceptable

### Tier 2: Default/MVP (most projects)
- Balance speed and quality
- Core path tests required
- Basic documentation
- Reasonable architecture

### Tier 3: Production/Enterprise
- Quality over speed
- Comprehensive tests (80%+ coverage)
- Full documentation
- Robust error handling
- Security review required

## Universal Rules

1. **Investigate before implement** - Search for existing patterns
2. **Type everything** - TypeScript strict, Python type hints
3. **Config over code** - Magic numbers in config files
4. **Fail fast** - Validate early, clear error messages
5. **Atomic commits** - One logical change per commit

## Default Behaviors

### When Implementing
1. Research existing solutions first
2. Define interfaces before implementation
3. Write tests for core logic
4. Document public APIs

### When Debugging
1. Reproduce first
2. Isolate the problem
3. Fix root cause, not symptom
4. Add regression test

### Before Completing
1. Run type checker
2. Run linter
3. Run tests
4. Review changes

## Integration

Loaded automatically on project initialization. Tier detected from:
- `package.json` keywords
- README indicators
- User specification
