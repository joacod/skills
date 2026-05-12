# Research basis

These recommendations are based on current web platform capabilities, design-token standards, Tailwind architecture, and public design-system practice. Use this file as background only; implementation should still match the target repository.

## Skill structure

Skills work best with a compact `SKILL.md` entry point and optional reference files that are loaded only when relevant. This skill therefore keeps the main workflow in `SKILL.md` and moves framework-specific details into separate references.

Sources:

- https://skills.sh/anthropics/skills/skill-creator

## Design token standards

The Design Tokens Community Group format exists to exchange token data between tools. Its model treats a token as a human-readable name/value pair with optional properties such as type and description. It also supports groups, references, and translation workflows.

Practical recommendation:

- Use CSS custom properties directly for most web-only projects.
- Use DTCG JSON plus a build tool when tokens need cross-tool or cross-platform outputs.
- Do not make a JSON pipeline mandatory for simple sites.

Sources:

- https://www.designtokens.org/tr/2025.10/format/
- https://www.styledictionary.org/

## CSS custom properties and cascade layers

CSS custom properties make repeated values easier to change and can carry semantic meaning. Cascade layers provide explicit cascade order and help avoid specificity battles across reset, tokens, base, components, and utilities.

Practical recommendation:

- Use `@layer` for global CSS architecture.
- Put tokens before base/components/utilities.
- Use CSS variables for runtime theming and dark mode.
- Avoid relying on Sass variables alone for themeable values.

Sources:

- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Cascade_layers
- https://developer.mozilla.org/docs/Web/CSS/%40layer

## Tailwind

Tailwind v4 defines design tokens through CSS theme variables with `@theme`. Those variables drive which utility classes exist and are also emitted as CSS variables. Tailwind also supports `@custom-variant`, useful for data-attribute or class-based dark mode. Tailwind v3 projects still commonly map CSS variables through `tailwind.config.js`.

Practical recommendation:

- In Tailwind v4, use `@theme` for utility-generating primitives.
- Keep semantic runtime tokens in `:root` and theme selectors.
- Use `@theme inline` to expose semantic tokens as stable utility names when useful.
- In Tailwind v3, map CSS custom properties through config extension.

Sources:

- https://tailwindcss.com/docs/theme
- https://tailwindcss.com/docs/functions-and-directives
- https://tailwindcss.com/docs/dark-mode
- https://tailwindcss.com/blog/tailwindcss-v4

## Theming and modern color

Modern CSS supports color-scheme integration for browser-provided UI, `prefers-color-scheme` for system preferences, and OKLCH for perceptual color authoring in current browsers.

Practical recommendation:

- Use `color-scheme` with theme toggles.
- Use OKLCH for new palettes when browser targets allow it.
- Prefer semantic foreground/background pairs and test contrast.

Sources:

- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/%40media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch

## Accessibility

WCAG contrast guidance remains a core acceptance criterion for text readability. Normal text generally needs at least 4.5:1 contrast and large text at least 3:1, with exceptions such as disabled/incidental text and logotypes.

Practical recommendation:

- Document semantic foreground/background pairs.
- Check contrast before approving new color roles.
- Do not rely on color alone for status meaning.

Sources:

- https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum

## Public design-system practice

Large design systems use tokens as an abstraction over raw values and increasingly structure color tokens around semantic roles, state, and theme behavior.

Practical recommendation:

- Use semantic names that describe role and state, not just hue.
- Include interaction states such as hover, active, selected, disabled, and focus.
- Keep specialty/component tokens constrained to their intended use.

Sources:

- https://atlassian.design/components/tokens
- https://polaris-react.shopify.com/design/colors/color-tokens
- https://polaris-react.shopify.com/design/layout/layout-tokens
- https://polaris-react.shopify.com/design/typography/typography-tokens
