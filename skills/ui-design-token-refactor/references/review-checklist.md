# Review checklist

Use this checklist before handing off CSS or Tailwind design-token work.

## Token architecture

- [ ] Token source of truth is clear: CSS-first, Tailwind theme, or generated from JSON.
- [ ] Primitive tokens are raw scales with no product meaning.
- [ ] Semantic tokens express product/UI intent.
- [ ] Component tokens are scoped to the component or component family.
- [ ] Component styles do not use raw hex/rgb/hsl/oklch values except for intentional one-offs.
- [ ] Component styles do not use primitive color tokens where a semantic token would be better.
- [ ] Token names are kebab-case and follow the repo convention.
- [ ] Deprecated or compatibility tokens are clearly marked.

## CSS architecture

- [ ] Global CSS uses a predictable layer order.
- [ ] Token declarations load before base, components, and utilities.
- [ ] Base styles are low-specificity and do not over-control components.
- [ ] Third-party overrides are isolated and documented.
- [ ] `!important` is absent or justified.
- [ ] Selectors are not unnecessarily deep or ID-based.

## Tailwind architecture

- [ ] Tailwind v4 projects use `@theme` for utility-generating tokens.
- [ ] Tailwind v4 projects use `:root` or theme selectors for runtime semantic values.
- [ ] Tailwind v3 projects map CSS variables in `tailwind.config.js` or `tailwind.config.ts`.
- [ ] Semantic utilities exist for common product roles such as `bg-surface`, `text-fg`, `text-muted`, and `border-subtle`.
- [ ] Repeated `dark:*` class pairs are replaced by semantic tokens where appropriate.
- [ ] Arbitrary utilities are reduced or justified.
- [ ] Tailwind default namespace resets are not used unless the migration impact is understood.

## Themes

- [ ] Light and dark modes override semantic tokens, not entire component rules.
- [ ] There is one theme control mechanism, such as `[data-theme="dark"]` or `.dark`.
- [ ] `color-scheme` is set for themes so native UI matches the page.
- [ ] System theme fallback is intentional if used.
- [ ] Theme changes do not cause unreadable text, invisible borders, or missing focus rings.

## Accessibility

- [ ] Normal text foreground/background pairs meet WCAG AA contrast, usually 4.5:1.
- [ ] Large text foreground/background pairs meet at least 3:1.
- [ ] Non-text UI indicators such as focus rings and meaningful borders are visible.
- [ ] Focus states are present and keyboard-visible.
- [ ] Disabled states are visually distinct and do not rely only on color when meaning matters.
- [ ] Error/success/warning states include text or icons when needed, not color alone.
- [ ] Reduced motion preferences are respected for large or non-essential motion.

## Component quality

- [ ] Primary, secondary, ghost, danger, and disabled variants are handled consistently if they exist.
- [ ] Hover, active, focus, selected, loading, and disabled states are preserved.
- [ ] Responsive behavior is preserved.
- [ ] Component tokens reduce duplication instead of adding unnecessary indirection.
- [ ] Visual hierarchy remains clear after token replacement.

## Maintainability

- [ ] The token README or handoff note explains how to add and use tokens.
- [ ] New values are added to existing scales when possible.
- [ ] The refactor does not introduce an unnecessary build dependency.
- [ ] Generated files, if any, are marked as generated.
- [ ] Remaining token debt is documented with concrete next steps.

## Validation evidence

Record commands and results:

```markdown
## Validation
- `npm run lint`: passed/failed/not available
- `npm run typecheck`: passed/failed/not available
- `npm run build`: passed/failed/not available
- `npm test`: passed/failed/not available
- Storybook/visual check: passed/failed/not available
- Contrast review: passed/failed/not available
```

If validation cannot be run, explain why and list manual checks performed.
