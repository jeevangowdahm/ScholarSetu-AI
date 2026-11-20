---
name: motion-and-animation
description: High-performance animation techniques for web and apps. Covers CSS keyframes, spring physics, staggered entrances, layout transitions, and reduced-motion media queries.
---

# Motion and Animation Skill

## 1. Performance-First Rules
- Only animate composite properties: `transform` and `opacity`. Never animate `width`, `height`, `top`, or `margin` during user interactions.
- Respect user OS preferences with `@media (prefers-reduced-motion: reduce)`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```

## 2. Animation Orchestration
- **Staggered Entrances**: Apply incremental animation-delays (`calc(var(--index) * 60ms)`) to give cards and lists an organic cascade.
- **Timing Functions**:
  - Entrance: `cubic-bezier(0.16, 1, 0.3, 1)` (Smooth ease-out)
  - Exit: `cubic-bezier(0.7, 0, 0.84, 0)` (Sharp ease-in)
  - Micro-interaction: `cubic-bezier(0.34, 1.56, 0.64, 1)` (Playful spring bounce)
