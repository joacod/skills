---
name: ui-design-token-refactor
description: Improve, refactor, review, and systematize web UI styling with CSS design tokens, cascade layers, Tailwind theme variables, semantic color/spacing/typography tokens, dark mode, accessibility checks, and maintainable component styling. Use this skill whenever the user asks to improve CSS, redesign a site, clean up stylesheets, migrate hardcoded values to tokens, organize Tailwind themes/classes, review a PR for design-token or CSS architecture issues, create or update a design system, add light/dark themes, or make future UI changes easier for agents.
---

# UI design token refactor

Use this skill to turn ad hoc CSS or Tailwind styling into a maintainable, token-based UI system that another agent can safely update later.

## Default workflow

1. Discover the project styling stack before changing code.
   - Check for `package.json`, Tailwind version/config, CSS entry points, CSS modules, Sass/Less, component libraries, Storybook, design-system packages, and theme toggles.
   - Identify whether the codebase is primarily vanilla CSS, CSS modules, Sass, Tailwind v4, Tailwind v3, or mixed.

2. Run or perform a style audit.
   - When repository files are available, prefer the bundled `scripts/audit_style_tokens.py` script to inventory raw colors, dimensions, typography values, and Tailwind utility patterns. Run it from the skill package or by absolute path, for example: `python /path/to/ui-design-token-refactor/scripts/audit_style_tokens.py <project-root> --output style-token-audit.md`.
   - Supplement the script with manual inspection of representative components and global styles.

3. Choose the implementation path.
   - For vanilla CSS, CSS modules, Sass, or mixed CSS, read `references/css-architecture.md`.
   - For Tailwind projects, read `references/tailwind-architecture.md`.
   - For naming, token hierarchy, and source-of-truth decisions, read `references/core-principles.md`.
   - For incremental migration steps, read `references/refactor-playbook.md`.
   - Before final handoff, read `references/review-checklist.md`.

4. Define or extend the token system before refactoring components.
   - Use primitive tokens for raw scales.
   - Use semantic tokens for product meaning and theme switching.
   - Use component tokens only for local component recipes and overrides.
   - Keep primitives out of component styles unless the project explicitly uses Tailwind utility primitives as its public API.

5. Refactor incrementally.
   - Add tokens first without changing visuals.
   - Replace hardcoded values in one surface or component family at a time.
   - Preserve existing behavior, responsive layout, and interaction states unless the user asks for a redesign.
   - Prefer small, reviewable diffs over broad visual rewrites.

6. Validate and report.
   - Run available checks: build, typecheck, lint, tests, Storybook build, visual regression, or at least targeted manual review.
   - Check accessible color pairs, focus states, hover/active/disabled states, and dark mode if applicable.
   - End with a concise handoff: what changed, files touched, token decisions, remaining token debt, and recommended next PRs.

## Core rules

- Treat tokens as the source of truth for color, spacing, typography, radius, shadow, motion, opacity, z-index, and breakpoint decisions.
- Prefer semantic names in components: `--color-bg-surface`, `--color-text-muted`, `--color-border-subtle`, `--color-primary`, `--space-4`, `--radius-md`.
- Use component tokens for reusable components when local indirection improves maintainability: `--button-bg`, `--card-border`, `--modal-shadow`.
- Implement dark mode by overriding semantic tokens, not by duplicating every component rule.
- Use cascade layers to make global CSS predictable: reset/theme or tokens/base/components/utilities/overrides.
- Avoid `!important`, ID selectors, and highly specific selectors unless required to override third-party CSS.
- Do not add a token for every one-off value. First decide whether the value belongs to an existing scale, a semantic role, a component token, or should remain local.
- Do not introduce a new dependency or token build pipeline unless the project needs cross-platform outputs, Figma/design-tool sync, or generated Tailwind/native/mobile artifacts.
- Preserve brand identity. Improve structure and consistency unless the user explicitly requests a new visual direction.

## Output format for code work

When finishing a styling refactor, include:

```markdown
## Summary
[What changed and why]

## Token architecture
[Primitive, semantic, and component token decisions]

## Files changed
- `path`: change summary

## Validation
[Commands run and results, or why they were unavailable]

## Remaining design debt
[Short list of next improvements]
```

For audit-only or PR-review tasks, use the audit template in `references/examples.md` instead of implying code was changed.

## Reference map

- `references/core-principles.md`: token hierarchy, naming, categories, and source-of-truth decisions.
- `references/css-architecture.md`: CSS custom properties, cascade layers, CSS modules, Sass, and component CSS patterns.
- `references/tailwind-architecture.md`: Tailwind v4 `@theme`, Tailwind v3 config patterns, dark mode, and utility mapping.
- `references/refactor-playbook.md`: practical migration sequence for existing sites.
- `references/review-checklist.md`: acceptance checklist for accessibility, maintainability, and handoff quality.
- `references/examples.md`: before/after examples and reusable output templates.
- `references/research-basis.md`: source notes behind the recommendations.
