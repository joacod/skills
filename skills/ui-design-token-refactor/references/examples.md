# Examples and templates

## Example user prompts this skill should handle

- "Clean up our CSS and move hardcoded colors into tokens."
- "Refactor this Tailwind UI so future agents can update the design consistently."
- "Add light and dark themes without duplicating component styles."
- "Our stylesheet is huge; organize it into a token-based design system."
- "Review this PR for design-token and CSS architecture issues."
- "Create a Tailwind v4 token setup for our brand colors and semantic utilities."

## Output template for an audit-only task

```markdown
# UI style audit

## Executive summary
[One paragraph: current styling state, risk, and recommended migration path]

## Findings
1. [Finding with examples and file paths]
2. [Finding with examples and file paths]
3. [Finding with examples and file paths]

## Recommended token architecture
[Primitive/semantic/component token plan]

## Migration plan
1. [First safe PR]
2. [Second safe PR]
3. [Third safe PR]

## Risks
[Potential regressions, browser support, theme concerns]
```

## Output template for a code refactor

```markdown
## Summary
[What changed and why]

## Token architecture
- Primitive tokens: [summary]
- Semantic tokens: [summary]
- Component tokens: [summary]

## Files changed
- `path/to/file`: [change]

## Validation
- `[command]`: [result]

## Remaining design debt
- [Specific next task]
```

## Vanilla CSS before/after

### Before

```css
.pricing-card {
  background: #ffffff;
  color: #111827;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  padding: 24px;
}

.pricing-card__eyebrow {
  color: #2563eb;
  font-size: 14px;
  font-weight: 600;
}
```

### After

```css
:root {
  --color-bg-surface: #ffffff;
  --color-text: #111827;
  --color-border-subtle: #e5e7eb;
  --color-primary: #2563eb;
  --radius-card: 16px;
  --shadow-surface: 0 8px 24px rgba(15, 23, 42, 0.08);
  --space-card: 24px;
  --font-size-sm: 0.875rem;
  --font-weight-semibold: 600;
}

.pricing-card {
  background: var(--color-bg-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-surface);
  padding: var(--space-card);
}

.pricing-card__eyebrow {
  color: var(--color-primary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
}
```

## Component token before/after

### Before

```css
.button--primary {
  background: #2563eb;
  color: #fff;
}

.button--primary:hover {
  background: #1d4ed8;
}

.button--danger {
  background: #dc2626;
  color: #fff;
}
```

### After

```css
.button {
  --button-bg: var(--color-primary);
  --button-bg-hover: var(--color-primary-hover);
  --button-fg: var(--color-on-primary);

  background: var(--button-bg);
  color: var(--button-fg);
}

.button:hover {
  background: var(--button-bg-hover);
}

.button[data-variant="danger"] {
  --button-bg: var(--color-danger);
  --button-bg-hover: var(--color-danger-hover);
  --button-fg: var(--color-on-danger);
}
```

## Tailwind before/after

### Before

```tsx
export function StatCard() {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 text-gray-900 shadow-sm dark:border-gray-800 dark:bg-gray-900 dark:text-white">
      <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Revenue</p>
      <p className="mt-2 text-3xl font-semibold text-gray-900 dark:text-white">$42k</p>
    </div>
  );
}
```

### After

```tsx
export function StatCard() {
  return (
    <div className="rounded-card border border-subtle bg-surface p-6 text-fg shadow-surface">
      <p className="text-sm font-medium text-muted">Revenue</p>
      <p className="mt-2 text-3xl font-semibold text-fg">$42k</p>
    </div>
  );
}
```

The improved version makes theme behavior a token concern instead of repeating light/dark classes in each component.

## Tailwind v4 token bridge example

```css
@import "tailwindcss";
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));

@theme {
  --spacing: 0.25rem;
  --radius-card: 0.75rem;
  --shadow-surface: 0 1px 2px rgb(0 0 0 / 0.08), 0 8px 24px rgb(0 0 0 / 0.08);
}

:root {
  --app-bg: white;
  --app-surface: white;
  --app-fg: #111827;
  --app-muted: #6b7280;
  --app-border: #e5e7eb;
  --app-primary: #2563eb;
  --app-on-primary: white;
}

[data-theme="dark"] {
  --app-bg: #030712;
  --app-surface: #111827;
  --app-fg: #f9fafb;
  --app-muted: #9ca3af;
  --app-border: #374151;
  --app-primary: #60a5fa;
  --app-on-primary: #030712;
}

@theme inline {
  --color-canvas: var(--app-bg);
  --color-surface: var(--app-surface);
  --color-fg: var(--app-fg);
  --color-muted: var(--app-muted);
  --color-subtle: var(--app-border);
  --color-primary: var(--app-primary);
  --color-on-primary: var(--app-on-primary);
}
```

## Token README starter

```markdown
# Design tokens

## Source of truth
Tokens live in `src/styles/tokens/`. Components should use semantic or component tokens, not hardcoded values.

## Token levels
- Primitive: raw scales, e.g. `--color-blue-500`, `--space-4`.
- Semantic: UI meaning, e.g. `--color-bg-surface`, `--color-text-muted`.
- Component: local recipes, e.g. `--button-bg`, `--card-padding`.

## Adding a token
1. Reuse an existing token if possible.
2. Add a primitive only when the raw value belongs to a shared scale.
3. Add or update semantic tokens for themeable UI meaning.
4. Use semantic/component tokens in components.
5. Check contrast for color pairs.
```
