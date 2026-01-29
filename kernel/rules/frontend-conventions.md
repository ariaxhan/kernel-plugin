# Frontend Conventions

**Frontend implementation guidance. Extends design-philosophy concepts.**

<!--
TO EVOLVE: Update with project-specific frontend patterns as they emerge.
This template provides universal frontend conventions.
Customize for your project's framework, styling solution, and design system.
-->

---

## Before Writing Frontend Code

### 1. Understand the Project Context

```
BEFORE touching CSS or components:
→ What framework is this project using?
→ What styling solution is already in place?
→ What design tokens/variables exist?
→ What's the existing component pattern?

MATCH THE PROJECT. Don't introduce new patterns.
```

### 2. Understand the User Flow

```
BEFORE designing a feature:
→ What is the user trying to accomplish?
→ What's the shortest path to that goal?
→ What state changes will they see?
→ What errors might they encounter?

DESIGN FOR THE FLOW. Not for the component.
```

---

## Styling Conventions

### System Fonts First

Unless the project has a specific font choice, use system fonts:

```css
/* Preferred stack */
font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Monospace */
font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace;
```

If the project uses a custom font, use it. **Never default to Inter or Geist** (AI aesthetic signatures).

### Color Strategy

```
PALETTE RULES:
- Most UI is neutral (grays, blacks, whites)
- 1 primary color for interactive elements
- 1-2 semantic colors (success, error, warning)
- Color communicates meaning, not decoration

AVOID (AI SIGNATURES):
- Purple-to-blue gradients
- Exact Tailwind default colors (#3B82F6, #6366F1, etc.)
- Rainbow palettes with no hierarchy
```

### Spacing System

Use consistent spacing scales. If the project has a system, use it. If not:

```css
/* 4px base unit */
--space-1: 4px;   /* tight */
--space-2: 8px;   /* default */
--space-3: 12px;  /* comfortable */
--space-4: 16px;  /* section */
--space-6: 24px;  /* large */
--space-8: 32px;  /* major */
```

---

## Component Patterns

### Interactive Elements

```
BUTTONS:
- Clear affordance (looks clickable)
- Hover/focus/active states
- Disabled state is obviously disabled
- Loading state if action is async

INPUTS:
- Clear boundaries
- Focus state is obvious
- Error state shows inline
- Labels are always visible (not placeholder-only)
```

### Feedback Patterns

```
PREFER:
- Inline feedback (near the action)
- State changes in place
- Undo over confirm
- Progressive disclosure

AVOID:
- Toasts for routine actions
- Modals for non-critical confirmations
- Alerts that interrupt flow
```

### Loading States

```
UNDER 200ms: Show nothing (feels instant)
200ms-1s: Subtle indicator (spinner, opacity change)
OVER 1s: Meaningful loading state (skeleton, progress)
```

---

## CSS Techniques (Encouraged)

```css
/* CSS Grid for 2D layouts */
display: grid;
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));

/* Flexbox for 1D alignment */
display: flex;
align-items: center;
gap: var(--space-2);

/* Smooth but fast transitions */
transition: opacity 150ms ease, transform 150ms ease;

/* Focus-visible for keyboard users */
:focus-visible { outline: 2px solid var(--focus-color); }

/* Modern CSS: :has(), container queries, color-mix */
.card:has(.error) { border-color: var(--error); }
@container (min-width: 400px) { ... }
background: color-mix(in srgb, var(--primary) 10%, transparent);
```

---

## Performance Checklist

```
□ No layout shifts (reserve space for dynamic content)
□ Images have dimensions or aspect-ratio
□ Fonts are preloaded or system fonts
□ Animations use transform/opacity (GPU-accelerated)
□ CSS is scoped (no global pollution)
□ Bundle size is monitored
```

---

## Code Review Lens

When reviewing frontend code, check:

1. **Does it match project conventions?** (Not introducing new patterns)
2. **Is the styling systematic?** (Using tokens, not magic numbers)
3. **Are interactions discoverable?** (Affordances clear)
4. **Is it accessible?** (Keyboard, screen reader, contrast)
5. **Is it fast?** (No unnecessary re-renders, efficient CSS)
6. **Could it be simpler?** (Complexity earns its place)

---

⚠️ **TEMPLATE NOTICE**
This file provides universal frontend conventions.
Customize for your project's specific framework and design system.
Remove sections that don't apply. Add project-specific patterns as they emerge.
