---
name: frontend-ui-craft
description: Advanced frontend engineering practices for modern, responsive, accessible web and mobile applications. Covers semantic HTML5, CSS Grid/Flexbox, DOM virtualization, state management, and WCAG 2.1 AA compliance.
---

# Frontend UI Craft Skill

## 1. Core Principles
- **Semantic HTML5**: Always use native semantics (<main>, <section>, <article>, <nav>, <header>, <footer>) before adding ARIA roles.
- **Mobile-First Responsive Layouts**: Design for 320px base viewports first, expanding via min-width media queries (480px, 768px, 1024px, 1280px).
- **Performance & Virtualization**: For lists exceeding 50 items, virtualize DOM nodes to keep 60fps scrolling and sub-100ms INP (Interaction to Next Paint).
- **Accessibility (a11y)**:
  - Enforce contrast ratios >= 4.5:1 for body copy and >= 3:1 for large headings (WCAG AA).
  - Explicit keyboard navigation (tabindex="0", focus rings `outline: 2px solid var(--accent)`).
  - Screen-reader text using `.sr-only` classes and descriptive `aria-label` attributes.

## 2. CSS Architecture
- Use CSS Custom Properties (`:root { --primary: #003366; ... }`) for unified themes and dynamic dark-mode toggling.
- Hardware-accelerate transforms by using `transform: translate3d(x,y,0)` and `will-change` sparingly.
