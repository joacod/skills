# Markdown Quality Checklist

Apply only the checks that fit the document role and renderer. Fix material
problems before cosmetic preferences, and record a check as unavailable when
its evidence cannot be obtained.

## Context and scope

- [ ] The document's primary audience, purpose, renderer, and dialect are
      known or explicitly marked as unresolved.
- [ ] The file is human-authored, generated, vendored, archived, or
      machine-consumed, and the edit authority is clear.
- [ ] Front matter, include markers, HTML comments, directives, and generated
      regions were preserved or intentionally updated with evidence.
- [ ] The change set is limited to the user's scope and avoids unrelated
      reflow or formatting churn.

## Meaning and accuracy

- [ ] Claims, commands, paths, API names, versions, examples, and expected
      output agree with repository evidence.
- [ ] Links, anchors, images, and referenced assets point to intended targets.
- [ ] Repeated facts have a canonical source, or the duplication is deliberate
      and synchronized by an established mechanism.
- [ ] Historical documents preserve their original decision, chronology, and
      status rather than being rewritten as current guidance.
- [ ] No content was invented to fill a missing section, link, screenshot,
      prerequisite, or compatibility claim.

## Structure and readability

- [ ] The heading outline is meaningful for the renderer and does not skip
      levels without a documented reason.
- [ ] A standalone document has a clear title; sections appear in reader-useful
      order and answer concrete questions.
- [ ] Paragraphs are focused, lists represent parallel items or steps, and list
      nesting is shallow and consistent.
- [ ] Tables are used only for real comparisons or compact structured data,
      have useful headers, and do not serve as layout containers.
- [ ] Code, paths, flags, identifiers, and short literals use inline code; long
      examples use fenced blocks with an appropriate language tag.
- [ ] Emphasis, blockquotes, alerts, HTML, and other features clarify content
      rather than add decoration or hide the main path.

## Navigation and accessibility

- [ ] Link text is descriptive out of context and does not rely on bare URLs or
      repeated “here” labels without a good reason.
- [ ] Local links and anchors were checked with the target renderer's rules.
- [ ] Images have useful alternative text, stable paths, and surrounding
      context; diagrams have a text explanation when needed.
- [ ] Essential meaning does not depend on emoji, color, symbols, or styling.
- [ ] Tables and headings remain understandable to readers using assistive
      technology or narrow screens.
- [ ] Renderer-specific syntax has a supported fallback or an intentional
      compatibility boundary.

## Role-specific finish

- [ ] README: the value and first useful path are clear, or the file was
      intentionally left to `readme-first`.
- [ ] Guide/tutorial: prerequisites, ordered steps, and an observable result
      are present and verified.
- [ ] Reference: terminology, signatures, defaults, constraints, and examples
      are current and easy to look up.
- [ ] ADR/design: status, context, decision, alternatives, and consequences are
      historically faithful.
- [ ] Changelog/release notes: version, chronology, categories, and links are
      consistent with repository release evidence.
- [ ] Template/instruction: placeholders, markers, directives, precedence, and
      safety boundaries remain intact.
- [ ] Generated/machine-facing: the owning generator or consumer was checked,
      and the document will be regenerated or validated through its contract.

## Verification and diff

- [ ] Existing Markdown lint, formatter, docs build, link checker, preview, or
      tests were run when relevant and available.
- [ ] Static inspection or a focused rendered preview covers checks that have no
      automated equivalent.
- [ ] Results distinguish passed, executed-but-informational, unavailable, and
      skipped checks.
- [ ] The final diff contains no lost front matter, broken fences, changed
      semantics, accidental mass reflow, or unrelated files.
