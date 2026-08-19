# Markdown Practices and Compatibility

Use this reference when editing Markdown syntax or deciding whether an
extension is appropriate. The target renderer is the source of truth: Markdown
implementations differ, and a feature that looks correct in one preview may be
literal text or inaccessible in another.

## Establish the dialect first

Before changing syntax, inspect the repository's docs site, package scripts,
front matter, MDX components, CI checks, renderer configuration, and hosting
platform. Record the supported baseline and any extensions, such as:

- CommonMark or another portable Markdown dialect;
- GitHub Flavored Markdown (GFM), including tables, task lists, and
  strikethrough;
- front matter consumed by a static-site generator;
- MDX or custom components;
- admonitions, alerts, Mermaid, math, footnotes, or raw HTML.

Do not replace an existing extension with portable Markdown when the extension
is part of the document's interface. Conversely, do not add renderer-specific
syntax to a document that is copied to multiple consumers without evidence that
all consumers support it.

## Portable baseline

- Put a space after heading markers (`## Heading`) and keep blank lines around
  block elements when the renderer benefits from them.
- Use a clear heading outline. A standalone document generally needs one
  meaningful top-level heading; do not skip levels merely for visual size.
- Separate paragraphs with blank lines. Use headings, lists, or blockquotes for
  structure instead of indentation or repeated punctuation.
- Prefer `*` or `_` for emphasis only when it clarifies meaning. Do not use bold
  as a substitute for headings or make every important-looking phrase bold.
- Use fenced code blocks for multi-line code and identify the language when the
  renderer supports syntax highlighting. Use inline code for names, flags,
  paths, and short literals.
- Prefer descriptive link text (`read the deployment guide`) over bare URLs or
  vague text such as “click here.” Keep links close to the claim they support.
- Use images only when they communicate something useful. Verify relative asset
  paths and write alternative text that conveys the image's purpose, not its
  filename.
- Use tables for compact, genuinely tabular comparisons with a header row. Use
  lists or sections for prose, procedures, or content that must work on narrow
  screens.
- Keep list markers, indentation, and nesting consistent within a document.
  Ordered-list numbering should communicate sequence when sequence matters.
- Avoid trailing spaces for visual spacing. If a hard line break is required,
  use the renderer-supported form deliberately and verify the result.

These compatibility-oriented practices are distilled from the references below;
read the actual source when a renderer edge case matters.

## Features with a compatibility cost

Use these only when they earn their complexity and are supported by the target:

- **GFM tables, task lists, and strikethrough:** useful in GitHub workflows;
  avoid assuming they render in every Markdown consumer.
- **Alerts and admonitions:** useful for warnings or notes, but use the exact
  syntax of the docs platform and keep the same information available to
  readers who receive raw Markdown.
- **Footnotes and reference-style links:** useful for repeated citations or
  long URLs; keep definitions discoverable and do not hide essential actions.
- **Raw HTML:** appropriate when the renderer or an existing document contract
  requires it. Avoid using HTML only to force visual styling that Markdown can
  express clearly.
- **MDX, Mermaid, math, and custom components:** preserve established syntax;
  verify imports, build support, accessibility, and fallback behavior before
  introducing or rewriting it.
- **Escaping:** escape punctuation only when it would otherwise be parsed as
  Markdown. Over-escaping makes source harder to read and can break links or
  code examples.

## Accessibility and rendered usability

- Use headings for structure, not just large text.
- Make links understandable when read out of context; avoid repeating the same
  vague label for different destinations.
- Give informative images useful alt text. Mark decorative images as
  decorative only when the renderer and accessibility convention support it.
- Do not make emoji, color, symbols, or text styling the only way to understand
  status or meaning.
- Keep tables narrow and simple; repeat enough context in headers so a cell is
  meaningful when read independently.
- Pair diagrams with a concise textual explanation and preserve the source for
  maintainers when the diagram is not self-explanatory.
- Check contrast, keyboard behavior, and heading/link semantics in the rendered
  documentation when those properties are controlled by the docs site rather
  than by Markdown alone.

## References

- [Markdown Guide: Basic Syntax](https://www.markdownguide.org/basic-syntax/) —
  portable syntax and compatibility-oriented examples.
- [Markdown Guide: Extended Syntax](https://www.markdownguide.org/extended-syntax/)
  — tables, fenced code, footnotes, task lists, and other common extensions.
- [Markdown Here Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
  — compact examples of common GitHub-style constructs.
- [Daring Fireball: Markdown Syntax](https://daringfireball.net/projects/markdown/syntax)
  — the original Markdown design and syntax reference.
