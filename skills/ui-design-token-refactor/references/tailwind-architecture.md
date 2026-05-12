# Tailwind architecture for design-token refactors

Use this reference for Tailwind projects. First determine the Tailwind version because Tailwind v4 is CSS-first, while Tailwind v3 relies heavily on `tailwind.config.js`.

## Decision tree

1. If the project uses Tailwind v4 or imports `@import "tailwindcss"`, use the Tailwind v4 approach.
2. If the project uses Tailwind v3 with `tailwind.config.js` or `tailwind.config.ts`, use the Tailwind v3 approach.
3. If the project mixes Tailwind and custom CSS, use Tailwind for the utility API and CSS custom properties for semantic runtime values.
4. If there is already a design-system package, align with its token names instead of inventing parallel names.

## Tailwind v4 approach

Tailwind v4 uses CSS theme variables. Put values that should generate utilities in `@theme`. Put runtime semantic tokens in `:root` and theme selectors. Optionally bridge semantic tokens into utilities with `@theme inline`.

### Recommended entry file

```css
@import "tailwindcss";

@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));

@theme {
  /* Primitive utility-generating tokens */
  --spacing: 0.25rem;

  --font-sans: Inter, ui-sans-serif, system-ui, sans-serif;

  --color-brand-50: oklch(0.97 0.014 254.604);
  --color-brand-100: oklch(0.932 0.032 255.585);
  --color-brand-400: oklch(0.707 0.165 254.624);
  --color-brand-500: oklch(0.623 0.214 259.815);
  --color-brand-600: oklch(0.546 0.245 262.881);
  --color-brand-700: oklch(0.488 0.243 264.376);

  --radius-control: 0.5rem;
  --radius-card: 0.75rem;
  --shadow-surface: 0 1px 2px rgb(0 0 0 / 0.08), 0 8px 24px rgb(0 0 0 / 0.08);
}

:root {
  color-scheme: light;

  /* Semantic runtime tokens */
  --ui-bg: var(--color-white);
  --ui-surface: var(--color-white);
  --ui-fg: var(--color-gray-950);
  --ui-muted: var(--color-gray-600);
  --ui-border: var(--color-gray-200);
  --ui-primary: var(--color-brand-600);
  --ui-primary-hover: var(--color-brand-700);
  --ui-on-primary: var(--color-white);
  --ui-focus-ring: var(--color-brand-500);
}

[data-theme="dark"] {
  color-scheme: dark;
  --ui-bg: var(--color-gray-950);
  --ui-surface: var(--color-gray-900);
  --ui-fg: var(--color-gray-50);
  --ui-muted: var(--color-gray-400);
  --ui-border: var(--color-gray-800);
  --ui-primary: var(--color-brand-500);
  --ui-primary-hover: var(--color-brand-400);
  --ui-on-primary: var(--color-gray-950);
}

@theme inline {
  /* Semantic utility API: bg-surface, text-fg, border-subtle, bg-primary */
  --color-canvas: var(--ui-bg);
  --color-surface: var(--ui-surface);
  --color-fg: var(--ui-fg);
  --color-muted: var(--ui-muted);
  --color-subtle: var(--ui-border);
  --color-primary: var(--ui-primary);
  --color-primary-hover: var(--ui-primary-hover);
  --color-on-primary: var(--ui-on-primary);
  --color-focus: var(--ui-focus-ring);
}
```

This creates a stable semantic utility vocabulary such as `bg-canvas`, `bg-surface`, `text-fg`, `text-muted`, `border-subtle`, `bg-primary`, and `text-on-primary`.

### Tailwind v4 usage pattern

Prefer semantic utilities for product surfaces:

```html
<section class="bg-canvas text-fg">
  <article class="rounded-card border border-subtle bg-surface p-6 shadow-surface">
    <h2 class="text-xl font-semibold text-fg">Usage</h2>
    <p class="mt-2 text-muted">Token-based styling is easier to theme.</p>
    <button class="mt-4 rounded-control bg-primary px-4 py-2 font-medium text-on-primary hover:bg-primary-hover focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus">
      Continue
    </button>
  </article>
</section>
```

Use primitive utilities for layout and spacing when the project already treats Tailwind as the design API:

```html
<div class="mx-auto grid max-w-6xl gap-6 px-4 py-12 md:grid-cols-3">
```

Do not replace every spacing utility with CSS variables unless the team wants a CSS-first component layer. Tailwind's utility scale can be the token API for spacing.

## Tailwind v3 approach

For Tailwind v3, define CSS variables in global CSS and map semantic utilities in `tailwind.config.js` or `tailwind.config.ts`.

### Global CSS

```css
:root {
  --color-bg: #ffffff;
  --color-bg-surface: #ffffff;
  --color-text: #111827;
  --color-text-muted: #4b5563;
  --color-border: #e5e7eb;
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-on-primary: #ffffff;
}

[data-theme="dark"] {
  --color-bg: #030712;
  --color-bg-surface: #111827;
  --color-text: #f9fafb;
  --color-text-muted: #9ca3af;
  --color-border: #374151;
  --color-primary: #60a5fa;
  --color-primary-hover: #93c5fd;
  --color-on-primary: #111827;
}
```

### Config mapping

```js
// tailwind.config.js
module.exports = {
  darkMode: ["class", "[data-theme='dark']"],
  theme: {
    extend: {
      colors: {
        canvas: "var(--color-bg)",
        surface: "var(--color-bg-surface)",
        fg: "var(--color-text)",
        muted: "var(--color-text-muted)",
        subtle: "var(--color-border)",
        primary: "var(--color-primary)",
        "primary-hover": "var(--color-primary-hover)",
        "on-primary": "var(--color-on-primary)",
      },
      borderRadius: {
        control: "var(--radius-control)",
        card: "var(--radius-card)",
      },
      boxShadow: {
        surface: "var(--shadow-surface)",
      },
    },
  },
};
```

If the project needs Tailwind opacity modifiers such as `bg-primary/80`, store RGB channel variables too:

```css
:root {
  --color-primary-rgb: 37 99 235;
}
```

```js
colors: {
  primary: "rgb(var(--color-primary-rgb) / <alpha-value>)",
}
```

## Dark mode strategy

Prefer one theme attribute on the document root:

```html
<html data-theme="dark">
```

Tailwind v4:

```css
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
```

Tailwind v3:

```js
darkMode: ["class", "[data-theme='dark']"]
```

Use `color-scheme` so native form controls and scrollbars match the theme:

```html
<html class="scheme-light dark:scheme-dark" data-theme="dark">
```

or in CSS:

```css
:root { color-scheme: light; }
[data-theme="dark"] { color-scheme: dark; }
```

## Component variants

For React projects, keep variant logic in components and token values in CSS/Tailwind. Tools like `clsx`, `cva`, or existing project helpers can compose classes, but do not add them just for a refactor.

Example variant map:

```ts
const buttonStyles = {
  base: "inline-flex items-center justify-center rounded-control px-4 py-2 font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus disabled:pointer-events-none disabled:opacity-55",
  variants: {
    primary: "bg-primary text-on-primary hover:bg-primary-hover",
    secondary: "border border-subtle bg-surface text-fg hover:bg-canvas",
    ghost: "bg-transparent text-fg hover:bg-surface",
  },
};
```

## Refactoring Tailwind classes

### Before

```tsx
<div className="rounded-xl border border-gray-200 bg-white p-6 text-gray-900 shadow-sm dark:border-gray-800 dark:bg-gray-900 dark:text-white">
  <p className="text-sm text-gray-500 dark:text-gray-400">Account status</p>
</div>
```

### After

```tsx
<div className="rounded-card border border-subtle bg-surface p-6 text-fg shadow-surface">
  <p className="text-sm text-muted">Account status</p>
</div>
```

The after version removes repeated light/dark pairs from every component. Theme behavior lives in tokens.

## When to use `@apply`

Use `@apply` sparingly.

Good uses:

- Styling third-party markup you do not control.
- Consolidating a repeated component recipe when the project already permits CSS composition.
- Vue/Svelte component style blocks that need token-aligned utilities.

Avoid using `@apply` to hide ordinary Tailwind classes everywhere. It can make the utility API harder to inspect and refactor.

## Common Tailwind mistakes

- Creating semantic tokens but continuing to use `text-gray-900 dark:text-white` throughout components.
- Defining tokens in `:root` but not exposing them to Tailwind utilities where the team expects utility classes.
- Overusing arbitrary values such as `bg-[#123456]`, `p-[17px]`, or `rounded-[11px]` after a scale exists.
- Mixing multiple dark mode mechanisms without a single source of truth.
- Replacing all layout utilities with custom CSS before understanding why the project uses Tailwind.
- Removing Tailwind defaults too early. In v4, namespace resets such as `--color-*: initial` are powerful but can break many existing utilities.

## Agent migration guidance

1. Add semantic utilities while preserving old classes.
2. Refactor one component family to prove the vocabulary.
3. Update docs with the semantic class names.
4. Replace repeated hardcoded utility pairs.
5. Only then consider tightening the primitive Tailwind theme.
