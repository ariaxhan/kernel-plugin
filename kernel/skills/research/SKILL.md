---
name: research
description: Deep research and investigation mode. Auto-triggers on "research", "find out", "learn about", "investigate", "deep dive", "what is", "how does", "explore", "understand", or questions requiring substantial information gathering.
---

# Research Mode

Thorough investigation before implementation. Activated when research signals detected.

## Depth Detection

Based on query complexity:
- **Light**: Quick lookup, 1-2 sources
- **Medium**: Compare options, 3-5 sources
- **Deep**: Comprehensive analysis, 5+ sources
- **Exhaustive**: Full landscape survey

## Methodology

### Phase 1: Scope
1. What exactly are we researching?
2. What decisions will this inform?
3. What's the time/depth budget?

### Phase 2: Source Diversity
1. Official documentation
2. GitHub examples/implementations
3. Stack Overflow solutions
4. Blog posts and tutorials
5. Academic papers (if applicable)

### Phase 3: Synthesis
1. Compare approaches
2. Note trade-offs
3. Identify consensus vs controversy
4. Document pitfalls and gotchas

### Phase 4: Recommendation
1. Clear recommendation with rationale
2. Alternatives considered
3. Risks and mitigations

## Output

Write research to `_meta/research/{topic}.md`:
```markdown
# Research: {topic}

## Summary
{1-3 sentences}

## Findings
{detailed findings}

## Recommendation
{what to do and why}

## Sources
{links and references}
```

## Anti-patterns

- Stopping at first result
- Only checking one source type
- Not documenting sources
- Research without clear question
- Over-researching simple topics

## Integration

If project has `kernel/banks/RESEARCH-BANK.md`, load it for deep methodology.
