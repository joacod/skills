# Refactor playbook

Use this playbook when cleaning up an existing site or app.

## Phase 0: protect behavior

Before refactoring, identify how to verify that the UI still works.

Look for:

- Build command.
- Typecheck command.
- Lint command.
- Unit/integration tests.
- Storybook or component preview.
- Visual regression tooling.
- Screenshot scripts.
- Existing browser support requirements.

If no checks exist, keep changes small and create a focused manual review checklist for the touched screens.

## Phase 1: audit style debt

Use both automated search and manual inspection.

### Automated audit

Run the bundled script when files are available:

```bash
python scripts/audit_style_tokens.py . --output style-token-audit.md
```

The script inventories hardcoded colors, dimensions, font values, shadows, z-index values, Tailwind color utilities, and arbitrary values.

Useful manual searches:

```bash
rg -n "#[0-9a-fA-F]{3,8}|rgb\(|rgba\(|hsl\(|hsla\(|oklch\(|color-mix\(" src
rg -n "\b[0-9]+px\b|\b[0-9]+rem\b|\bfont-size\b|\bline-height\b" src
rg -n "bg-\[[^\]]+\]|text-\[[^\]]+\]|p-\[[^\]]+\]|rounded-\[[^\]]+\]" src
```

### Manual audit

Inspect at least:

- Global stylesheet or Tailwind entry file.
- Layout shell/header/nav/footer.
- Button/link/input components.
- Card/surface components.
- Modal/popover/dropdown components.
- The most visually important page.

Classify values into:

1. Existing system value.
2. New primitive token.
3. New semantic token.
4. New component token.
5. One-off local value.
6. Bug or inconsistency to fix separately.

## Phase 2: design the first token slice

Do not build the entire system first. Start with a useful slice.

Recommended first slice:

- Background surface colors.
- Text colors.
- Border colors.
- Primary action colors.
- Focus ring.
- Base spacing scale.
- Radius scale for controls/cards.

Define token names and examples before code changes.

## Phase 3: add tokens without visual change

Add tokens that match current computed values.

Example:

```css
:root {
  --color-bg-surface: #ffffff;
  --color-text: #111827;
  --color-text-muted: #6b7280;
  --color-border-subtle: #e5e7eb;
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-on-primary: #ffffff;
}
```

At this stage, avoid changing colors to nicer values. First create the indirection. Normalize later.

## Phase 4: migrate one component family

Pick a high-value, repeated component such as buttons, cards, inputs, or page shell.

For each component:

1. Replace raw values with semantic/component tokens.
2. Preserve responsive behavior.
3. Preserve hover, focus, active, disabled, selected, loading, and error states.
4. Remove duplicated dark mode rules when semantic tokens cover them.
5. Check that variants compose by overriding local component tokens instead of repeating full declarations.

Example component migration:

```css
.button {
  --button-bg: var(--color-primary);
  --button-fg: var(--color-on-primary);
  --button-border: transparent;

  background: var(--button-bg);
  color: var(--button-fg);
  border-color: var(--button-border);
}

.button[data-variant="secondary"] {
  --button-bg: var(--color-bg-surface);
  --button-fg: var(--color-text);
  --button-border: var(--color-border-subtle);
}
```

## Phase 5: normalize repeated values

After the first no-visual-change migration, find duplicates and converge them onto scale values.

Examples:

- Convert `11px`, `12px`, and `13px` radii to `--radius-md` or `--radius-lg` when visually acceptable.
- Convert `15px`, `16px`, and `17px` spacing to `--space-4` when layout does not break.
- Convert near-identical grays into semantic roles.

Do not normalize values that intentionally encode hierarchy or layout constraints.

## Phase 6: add or simplify themes

For light/dark themes:

- Override semantic tokens only.
- Avoid duplicating component selectors in dark mode.
- Use a single root selector such as `[data-theme="dark"]` or `.dark`.
- Support `prefers-color-scheme` only if the product wants system default behavior.
- Set `color-scheme` for native UI.

Example:

```css
:root {
  color-scheme: light;
  --color-bg: white;
  --color-text: #111827;
}

[data-theme="dark"] {
  color-scheme: dark;
  --color-bg: #030712;
  --color-text: #f9fafb;
}
```

## Phase 7: update docs

Add or update a token usage note in the repository:

```markdown
# Design tokens

## Source of truth
Tokens live in `src/styles/tokens/`. Component CSS must use semantic or component tokens.

## Adding a color
1. Add or reuse a primitive in `colors.css`.
2. Map it to a semantic token in `:root` and each theme.
3. Use the semantic token in components.
4. Check contrast for every foreground/background pair.

## Naming
- primitive: `--color-blue-500`
- semantic: `--color-bg-surface`
- component: `--button-bg`
```

## Phase 8: validation

Run available checks. A good final response states what was run and what passed.

Recommended order:

1. Formatter/linter.
2. Typecheck/build.
3. Unit/integration tests if relevant.
4. Storybook or component preview build.
5. Visual check of touched pages/components.
6. Contrast checks for new or changed color pairs.

## Migration strategies

### Small codebase

- Create tokens in one CSS file.
- Refactor all common components in one pass.
- Add a token README.

### Large codebase

- Add token foundation in one PR.
- Migrate components in batches.
- Keep temporary compatibility tokens for old names.
- Deprecate old tokens with comments and remove after usage drops.
- Track remaining raw values with audit reports.

### Tailwind-heavy codebase

- Add semantic utility names first.
- Migrate repeated light/dark class pairs.
- Keep Tailwind spacing/layout utilities unless they cause inconsistency.
- Avoid a full rewrite into CSS modules unless requested.

### Legacy Sass codebase

- Generate or define CSS custom properties from Sass maps.
- Replace Sass variables in themeable component rules with CSS variables.
- Keep Sass for file organization and mixins only where useful.

## Handoff template

Use this after code changes:

```markdown
## Summary
- Added token foundation for colors, spacing, radius, and focus states.
- Refactored buttons and cards to consume semantic/component tokens.
- Dark mode now overrides semantic tokens instead of duplicating component rules.

## Files changed
- `src/styles/tokens/colors.css`: added primitive and semantic color roles.
- `src/components/Button/Button.module.css`: replaced raw values with component tokens.
- `src/styles/tokens/README.md`: documented token naming and usage.

## Validation
- `npm run lint`: passed.
- `npm run build`: passed.
- Manual review: buttons/cards checked in light and dark themes.

## Remaining design debt
- Inputs still use raw border colors.
- Several marketing pages use one-off spacing values.
- No automated contrast test exists yet.
```
