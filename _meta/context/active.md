# Active Work

**Current focus and in-progress tasks.**

## Status: In Progress — v4.0.0

Major update mirroring local CodingVault config improvements.

## Completed This Session

- [x] Rewrite CLAUDE.md with compact Unicode syntax (Ψ, →, ≠, Σ, Φ, Ω, Ξ, Δ, ∇, Γ)
- [x] Integrate NEXUS features (model routing, magic keywords, autonomy rules, parallel-first)
- [x] Add hooks system (SessionStart + PostToolUse) to settings.json
- [x] Add /design command
- [x] Add /repo-init command
- [x] Add frontend-conventions rule
- [x] Swap worktree-parallelization for coding-prompt-bank skill
- [x] Version bump all plugin.json files to 4.0.0
- [x] Update marketplace.json description
- [x] Rewrite README.md for v4.0.0 with full documentation
- [x] Refresh _meta files
- [x] Update kernel/state.md

## Pending

- [ ] Clean up stale files (CONFIG-TYPES.md, SETUP.md if they exist)
- [ ] Copy frontend-conventions to kernel/rules/ template
- [ ] Create GitHub release v4.0.0
- [ ] Push to remote

## Key Changes (v3.0.0 → v4.0.0)

| Area | Change |
|------|--------|
| CLAUDE.md | Verbose markdown → compact Unicode syntax (~800 tokens) |
| Model routing | None → 5-tier (Ollama/Gemini/Sonnet/Opus/Haiku) |
| Hooks | Empty → SessionStart + PostToolUse |
| Magic keywords | None → ulw, ralph, eco |
| Autonomy | None → ACT/PAUSE/ASK boundaries |
| Commands | 14 → 16 (+design, +repo-init) |
| Rules | 12 → 13 (+frontend-conventions) |
| Skills | worktree-parallelization → coding-prompt-bank |
| README | v2.0.0 docs → v4.0.0 with syntax guide |

---

*Updated 2026-01-28*
