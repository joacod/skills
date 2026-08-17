---
name: readme-first
description: >
  Create, improve, simplify, rewrite, or review a software repository's main
  user-facing README.md. Use this whenever a user asks for a README from an
  existing codebase, faster onboarding, clearer README structure or developer
  experience, a 60-second quick start, or a fix for stale or inaccurate README
  instructions. Focus on the repository front door, not arbitrary Markdown,
  architecture or API documentation, contributor guides, branding, or landing
  pages.
---

# README First

Treat the repository's main README as its front door. Optimize for a new visitor
understanding what the project is, why it matters, and how to reach a first
useful result in about 60 seconds. Prefer evidence, reader value, and a short
happy path over a complete-looking template.

## Choose the mode

- **Create** when the repository has no useful main README.
- **Improve** when a README exists but needs correction, simplification,
  reorganization, or stronger onboarding.
- **Review** when the user wants an audit or recommendations without edits.

In every mode, target the repository's main user-facing README (normally the
root `README.md`). Do not silently turn the task into general Markdown,
architecture, API, contributor, branding, or project-marketing work.

## Operate in this order

Follow this pipeline; do not begin with a universal template:

**inspect → classify → establish facts → prioritize → write → verify → trim**

1. **Inspect.** Read [repo-inspection.md](references/repo-inspection.md) before
   creating or substantially changing the README. Inspect only repository
   evidence needed to describe the user experience: manifests and lockfiles,
   scripts and task runners, entrypoints and exports, CLI definitions, examples,
   tests that reveal usage, CI, assets, supporting docs, license, contribution
   guidance, and the current README.
2. **Classify.** Identify the project type, primary audience, user-facing
   capability, normal happy path, supported runtime/package manager, and the
   documentation that should remain deeper than the README.
3. **Establish facts.** Prefer executable behavior and configuration over stale
   prose. Record unresolved facts instead of guessing. Never invent commands,
   package names, prerequisites, environment variables, ports, features, URLs,
   screenshots, badges, or compatibility claims.
4. **Prioritize.** Read [readme-structure.md](references/readme-structure.md).
   Plan for the reader journey: 3 seconds for identity and value, 30 seconds
   for relevance and capabilities, 60 seconds for installation and normal use,
   then links to deeper documentation. Select sections because they answer an
   important reader question, not because a template includes them.
5. **Write.** Put the concrete value proposition and the shortest realistic
   Quick Start early. Use one representative example, concise benefit-oriented
   features, restrained badges, and existing visuals only when they help. Keep
   project identity and a useful established voice when improving an existing
   README.
6. **Verify.** Cross-check every command, import, package name, path, config
   key, link, and claim against repository evidence. When safe and practical,
   execute the primary happy path locally. Do not claim a command was tested
   when only static inspection was possible. Review mode must not modify files.
7. **Trim.** Read [quality-checklist.md](references/quality-checklist.md), fix
   every material finding, and re-read the result as a stranger. Remove
   duplication, ceremony, mechanism-heavy prose, exhaustive reference material,
   and anything that does not help a new or prospective user decide or start.

## Mode-specific behavior

### Create

Inspect first, classify the project, identify the audience and happy path, then
select only the sections that fit. Generate a usable README from established
facts, verify its commands and links, and finish with the quality checklist.

### Improve

Treat the existing README as evidence, not authority. Preserve accurate
terminology, useful examples, relevant visuals, project-specific explanations,
and a clear voice. Compare it with repository truth, repair stale instructions,
move deep material to existing canonical documents when appropriate, strengthen
Quick Start, and remove content only when it hurts comprehension or onboarding.
Do not rewrite merely because another wording is possible.

### Review

Do not edit the repository. Evaluate immediate comprehension, audience fit,
value proposition, hierarchy, Quick Start, factual accuracy, copy-pasteability,
scanability, examples, progressive disclosure, tone, and unnecessary depth.
Prioritize findings by user impact and cite concrete evidence, such as a script
that is documented but absent from the manifest. Do not expose a numeric score
unless the user asks for one.

## Boundaries

- The main README is an onboarding and adoption surface, not the canonical
  home for internal architecture, exhaustive APIs or CLI flags, complete
  configuration or environment-variable references, deployment internals,
  repository walkthroughs, long troubleshooting guides, changelogs, roadmaps,
  or full contributor workflows.
- Link to real canonical documents instead of fabricating links or duplicating
  deep material. Do not create supporting documents just to satisfy a template.
- Keep Quick Start to one obvious supported path. Prefer a working result over a
  menu of equivalent package managers or speculative alternatives.
- Features describe what users can accomplish; implementation details and
  architecture belong in a short explanation or deeper documentation only when
  they are necessary to use or evaluate the project.
- Badges, visuals, tables, a table of contents, and `<details>` are optional.
  Use each only when it improves comprehension; never use collapsed content as
  a substitute for a proper supporting document.
- Keep the license accurate and minimal. Link to existing contribution and
  support guidance rather than copying it into the README.
