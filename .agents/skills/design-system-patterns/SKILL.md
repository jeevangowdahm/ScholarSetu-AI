---
name: design-system-patterns
description: Principles for creating enterprise-grade design systems, typography scales, design tokens, color harmony, glassmorphism, micro-interactions, and visual hierarchy.
---

# Design System Patterns Skill

## 1. Design Token Hierarchy
- **Typography Scale**: Base 16px with modular scale 1.25 (Major Third):
  - H1: 3.052rem (48.8px) | H2: 2.441rem (39px) | H3: 1.953rem (31.2px) | Body: 1rem (16px) | Caption: 0.8rem (12.8px)
- **Spacing Rhythm**: 4px/8px standard base unit:
  - `--space-xs: 4px`, `--space-sm: 8px`, `--space-md: 16px`, `--space-lg: 24px`, `--space-xl: 32px`.
- **Elevation System**:
  - Level 1 (Card): `box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)`
  - Level 2 (Hover/Dropdown): `box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)`
  - Level 3 (Modal/Dialog): `box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15), 0 10px 10px -5px rgba(0,0,0,0.04)`

## 2. Glassmorphism & Visual Polish
- Subtle backdrop filters: `backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: rgba(255, 255, 255, 0.85);`
- Distinct borders with alpha channel: `border: 1px solid rgba(255, 255, 255, 0.18);`
