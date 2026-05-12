# Core principles for token-based UI styling

## Goal

Make UI styling easy for future agents to change safely by replacing scattered raw values with a small, documented token system.

A good token system is not just a variable dump. It separates raw scales from product meaning and from component recipes.

## Token hierarchy

Use three levels by default.

| Level | Purpose | Example | Allowed consumers |
|---|---|---|---|
| Primitive tokens | Raw scales with no product meaning | `--color-blue-500`, `--space-4`, `--radius-md` | Other tokens, Tailwind theme variables, rare low-level utilities |
| Semantic tokens | UI meaning and theme behavior | `--color-bg-surface`, `--color-text-muted`, `--color-primary-hover` | Components, pages, utilities |
| Component tokens | Local component recipe values | `--button-bg`, `--card-padding`, `--dialog-shadow` | Only the component or component family |

Use semantic tokens for most component styling. Primitive tokens can exist, but they should not leak everywhere because they make themes and brand changes harder.

## Naming model

Use kebab-case. Keep names predictable and stable.

### Primitive token names

- Colors: `--color-gray-50`, `--color-gray-950`, `--color-blue-500`
- Spacing: `--space-0`, `--space-1`, `--space-2`, `--space-4`, `--space-6`, `--space-8`
- Typography: `--font-family-sans`, `--font-size-sm`, `--font-size-base`, `--line-height-tight`, `--font-weight-semibold`
- Radius: `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-full`
- Shadow: `--shadow-sm`, `--shadow-md`, `--shadow-lg`
- Motion: `--duration-fast`, `--duration-normal`, `--ease-standard`, `--ease-emphasized`
- Layout: `--breakpoint-md`, `--container-lg`, `--z-dropdown`, `--z-modal`

### Semantic token names

Use `--category-target-role-state` or `--category-role-state`.

Recommended color roles:

```css
--color-bg;
--color-bg-surface;
--color-bg-elevated;
--color-bg-inverse;
--color-text;
--color-text-muted;
--color-text-subtle;
--color-text-inverse;
--color-border;
--color-border-subtle;
--color-border-strong;
--color-primary;
--color-primary-hover;
--color-primary-active;
--color-on-primary;
--color-danger;
--color-danger-hover;
--color-on-danger;
--color-success;
--color-warning;
--color-info;
--color-focus-ring;
```

Recommended non-color semantic roles:

```css
--space-page-x;
--space-section-y;
--space-control-x;
--space-control-y;
--radius-control;
--radius-card;
--shadow-surface;
--shadow-popover;
--duration-interaction;
--ease-interaction;
```

### Component token names

Scope component tokens inside the component selector when possible:

```css
.card {
  --card-bg: var(--color-bg-surface);
  --card-fg: var(--color-text);
  --card-border: var(--color-border-subtle);
  --card-radius: var(--radius-card);
}
```

Use component tokens when a component has variants, internal recipes, or repeated values. Do not create component tokens for trivial one-rule components.

## Token categories to cover

Start with the categories that produce the most duplicate code:

1. Color
2. Spacing
3. Typography
4. Radius
5. Shadow/elevation
6. Motion
7. Borders/strokes
8. Opacity
9. Z-index/layering
10. Breakpoints/container sizes

Do not delay a useful migration waiting for a perfect full system. Colors and spacing usually provide the fastest payoff.

## Source of truth decision

Choose the lightest source of truth that solves the project problem.

### CSS-first tokens

Best for most web-only apps.

- Store primitive and semantic tokens as CSS custom properties.
- Use cascade layers to control ordering.
- Document names in `tokens/README.md` or equivalent.
- Add optional generated utilities only when the team needs them.

### Tailwind theme variables

Best for Tailwind v4 projects where utility classes are the styling API.

- Put primitive utility-generating values in `@theme`.
- Put semantic runtime theme values in `:root` and theme selectors.
- Optionally expose semantic tokens as Tailwind utilities via `@theme inline`.

### JSON/DTCG token source

Best when tokens must sync across design tools, documentation, native apps, multiple packages, or generated CSS/Tailwind outputs.

- Use the Design Tokens Community Group format when supported by the toolchain.
- Keep CSS output generated and do not hand-edit generated files.
- Use Style Dictionary or an equivalent transform when multiple output formats are needed.
- Document whether JSON is canonical and CSS is generated, or CSS is canonical and JSON is documentation only.

Example DTCG-style structure to adapt to the toolchain:

```json
{
  "color": {
    "$type": "color",
    "blue": {
      "500": {
        "$value": {
          "colorSpace": "srgb",
          "components": [0.231, 0.51, 0.965],
          "hex": "#3b82f6"
        },
        "$description": "primary brand blue"
      }
    }
  },
  "dimension": {
    "$type": "dimension",
    "space": {
      "4": {
        "$value": { "value": 1, "unit": "rem" },
        "$description": "base spacing step"
      }
    }
  }
}
```

When a tool accepts shorthand values such as `"$value": "#3b82f6"`, confirm that this is a tool-specific convenience and not necessarily portable to every DTCG-aware tool.

## Color guidance

- Prefer semantic color pairs: background plus foreground, container plus on-container, action plus on-action.
- Every interactive role should have hover, active, focus, disabled, and selected treatment where relevant.
- Use OKLCH for new color scales when browser support and team familiarity allow it; it is easier to build perceptually consistent scales than with hex-only editing.
- Preserve existing brand colors unless the task includes redesign.
- Always test contrast for the actual foreground/background pairs used in the UI.

## Spacing guidance

Use a predictable spacing scale. A 4px rhythm is a practical default:

```css
--space-0: 0;
--space-1: 0.25rem;
--space-2: 0.5rem;
--space-3: 0.75rem;
--space-4: 1rem;
--space-5: 1.25rem;
--space-6: 1.5rem;
--space-8: 2rem;
--space-10: 2.5rem;
--space-12: 3rem;
--space-16: 4rem;
```

Use semantic spacing for repeated layout decisions:

```css
--space-page-x: clamp(var(--space-4), 4vw, var(--space-8));
--space-section-y: clamp(var(--space-10), 8vw, var(--space-16));
--space-control-x: var(--space-4);
--space-control-y: var(--space-2);
```

## Typography guidance

Separate raw type primitives from semantic text roles.

```css
--font-size-sm: 0.875rem;
--font-size-base: 1rem;
--font-size-lg: 1.125rem;
--font-size-xl: 1.25rem;
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;

--text-body-size: var(--font-size-base);
--text-body-line-height: var(--line-height-normal);
--text-heading-size: clamp(2rem, 4vw, 4rem);
--text-heading-line-height: 1.05;
```

## What not to tokenize

Avoid tokens for:

- One-off art direction that is unlikely to repeat.
- Values that depend on content and should remain fluid.
- Fine alignment nudges that hide layout bugs.
- Values from third-party widgets unless they are part of your integration layer.
- Every Tailwind class in an existing file before you understand the design pattern.

## Agent handoff documentation

Whenever tokens are added or changed, update a local token README or handoff note with:

- Token categories and naming rules.
- How to add a new token.
- How to add a new theme.
- Which files are generated versus manually maintained.
- Examples of correct component usage.
