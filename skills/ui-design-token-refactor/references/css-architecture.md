# CSS architecture for design-token refactors

Use this reference for vanilla CSS, CSS modules, Sass/Less, and mixed CSS projects.

## Recommended file structure

Use a structure close to this, adapting names to the existing project conventions:

```text
src/
  styles/
    main.css
    reset.css
    tokens/
      index.css
      colors.css
      spacing.css
      typography.css
      radius.css
      shadows.css
      motion.css
    base/
      index.css
      typography.css
      forms.css
    components/
      index.css
      button.css
      card.css
      dialog.css
    utilities/
      index.css
      layout.css
```

Keep the entry point boring and predictable:

```css
@layer reset, tokens, base, components, utilities, overrides;

@import "./reset.css" layer(reset);
@import "./tokens/index.css" layer(tokens);
@import "./base/index.css" layer(base);
@import "./components/index.css" layer(components);
@import "./utilities/index.css" layer(utilities);
```

Reserve `overrides` for temporary migration or third-party integration fixes. Remove entries from it as the system improves.

## Layer purpose

| Layer | Purpose | Guidance |
|---|---|---|
| `reset` | Normalize browser defaults | Minimal reset, box sizing, media defaults |
| `tokens` | Custom properties and themes | No component selectors except theme roots/selectors |
| `base` | Element defaults | `body`, headings, links, forms, selection, focus defaults |
| `components` | Component classes | `.button`, `.card`, `.dialog`, component recipes |
| `utilities` | Small single-purpose helpers | Layout utilities, visually hidden, wrappers |
| `overrides` | Temporary or third-party overrides | Keep small and documented |

Layer order should do most of the cascade work. Avoid winning conflicts through high specificity.

## Token entry point

Example `tokens/index.css`:

```css
@import "./colors.css";
@import "./spacing.css";
@import "./typography.css";
@import "./radius.css";
@import "./shadows.css";
@import "./motion.css";
```

Example `tokens/colors.css`:

```css
:root {
  color-scheme: light;

  /* Primitives */
  --color-gray-50: oklch(0.985 0.002 247.839);
  --color-gray-100: oklch(0.967 0.003 264.542);
  --color-gray-500: oklch(0.551 0.027 264.364);
  --color-gray-900: oklch(0.21 0.034 264.665);
  --color-gray-950: oklch(0.13 0.028 261.692);
  --color-blue-500: oklch(0.623 0.214 259.815);
  --color-blue-600: oklch(0.546 0.245 262.881);
  --color-red-600: oklch(0.577 0.245 27.325);

  /* Semantic */
  --color-bg: var(--color-gray-50);
  --color-bg-surface: white;
  --color-bg-elevated: white;
  --color-text: var(--color-gray-950);
  --color-text-muted: var(--color-gray-500);
  --color-border: oklch(0.872 0.01 258.338);
  --color-primary: var(--color-blue-500);
  --color-primary-hover: var(--color-blue-600);
  --color-on-primary: white;
  --color-danger: var(--color-red-600);
  --color-focus-ring: var(--color-blue-500);
}

[data-theme="dark"] {
  color-scheme: dark;
  --color-bg: var(--color-gray-950);
  --color-bg-surface: var(--color-gray-900);
  --color-bg-elevated: oklch(0.25 0.03 264.665);
  --color-text: var(--color-gray-50);
  --color-text-muted: oklch(0.707 0.022 261.325);
  --color-border: oklch(0.373 0.034 259.733);
  --color-primary: oklch(0.707 0.165 254.624);
  --color-primary-hover: oklch(0.809 0.105 251.813);
  --color-on-primary: var(--color-gray-950);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]):not([data-theme="dark"]) {
    color-scheme: dark;
    --color-bg: var(--color-gray-950);
    --color-bg-surface: var(--color-gray-900);
    --color-bg-elevated: oklch(0.25 0.03 264.665);
    --color-text: var(--color-gray-50);
    --color-text-muted: oklch(0.707 0.022 261.325);
    --color-border: oklch(0.373 0.034 259.733);
    --color-primary: oklch(0.707 0.165 254.624);
    --color-primary-hover: oklch(0.809 0.105 251.813);
    --color-on-primary: var(--color-gray-950);
  }
}
```

Use class-based or data-attribute theme selection if the app has a manual toggle. Use `prefers-color-scheme` as a default when no manual choice exists.

## Base styles

Keep base styles semantic and low specificity:

```css
body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-family-sans);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
}

:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

a {
  color: var(--color-primary);
}

a:hover {
  color: var(--color-primary-hover);
}
```

Avoid styling every component through element selectors. Base styles should set safe defaults only.

## Component styles

Use semantic tokens and local component tokens:

```css
.button {
  --button-bg: var(--color-primary);
  --button-fg: var(--color-on-primary);
  --button-border: transparent;
  --button-radius: var(--radius-control);
  --button-padding-x: var(--space-control-x);
  --button-padding-y: var(--space-control-y);

  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  min-height: 2.5rem;
  padding: var(--button-padding-y) var(--button-padding-x);
  border: 1px solid var(--button-border);
  border-radius: var(--button-radius);
  background: var(--button-bg);
  color: var(--button-fg);
  font-weight: var(--font-weight-medium);
  transition: background-color var(--duration-interaction) var(--ease-interaction),
    border-color var(--duration-interaction) var(--ease-interaction),
    color var(--duration-interaction) var(--ease-interaction);
}

.button:hover {
  --button-bg: var(--color-primary-hover);
}

.button[data-variant="secondary"] {
  --button-bg: var(--color-bg-surface);
  --button-fg: var(--color-text);
  --button-border: var(--color-border);
}

.button:disabled,
.button[aria-disabled="true"] {
  opacity: 0.55;
  cursor: not-allowed;
}
```

This pattern lets variants override a small recipe instead of repeating entire declarations.

## CSS modules

For CSS modules, keep tokens global and component recipes local:

```css
/* Button.module.css */
.root {
  --button-bg: var(--color-primary);
  --button-fg: var(--color-on-primary);
  background: var(--button-bg);
  color: var(--button-fg);
}

.secondary {
  --button-bg: var(--color-bg-surface);
  --button-fg: var(--color-text);
}
```

Do not define global tokens inside individual modules unless the module is the canonical source for a component package.

## Sass and Less

Sass/Less can help organize files, but runtime theming requires CSS custom properties.

Prefer:

```scss
.card {
  padding: var(--space-4);
  background: var(--color-bg-surface);
}
```

Avoid using Sass variables as the only source of truth for themeable values:

```scss
// Avoid for themeable values
$brand-blue: #3b82f6;
.button { background: $brand-blue; }
```

A safe compromise is to use Sass maps only to generate CSS custom properties.

## Specificity rules

- Prefer class selectors and `:where()` for low-specificity grouping.
- Avoid IDs in CSS selectors.
- Avoid nesting deeper than two levels.
- Avoid `!important`; use layer order, lower specificity, or a documented `overrides` layer instead.
- Keep third-party overrides isolated and commented with the package/component they patch.

Example low-specificity grouping:

```css
:where(.prose) :where(h1, h2, h3) {
  color: var(--color-text);
  line-height: var(--line-height-tight);
}
```

## Modern CSS features to use carefully

- `@layer`: organize cascade order and reduce specificity fights.
- CSS custom properties: runtime theming and semantic indirection.
- `color-scheme`: align browser-provided UI such as forms and scrollbars with light/dark themes.
- `oklch()`: use for new perceptual color scales when supported by project browser targets.
- `color-mix()`: useful for generated overlays, borders, and state colors; document fallback needs if supporting older browsers.
- `clamp()`: useful for fluid typography and layout spacing.

## Migration-safe pattern

When replacing raw values, add tokens first and use them without changing computed values.

Before:

```css
.card {
  background: #ffffff;
  color: #111827;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
}
```

After:

```css
:root {
  --color-bg-surface: #ffffff;
  --color-text: #111827;
  --color-border-subtle: #e5e7eb;
  --radius-card: 12px;
  --space-card: 24px;
}

.card {
  background: var(--color-bg-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-card);
  padding: var(--space-card);
}
```

Only after the no-visual-change migration should you normalize values to a tighter scale.
