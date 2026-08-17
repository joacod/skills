# README Structure

Use information priority to shape the README, not a universal list of
headings. The structure should move a new visitor through:

**3 seconds → 30 seconds → 60 seconds → deeper documentation**

At each stage answer the next useful question: what is this, why would I use
it, what can it do, how do I start, what does normal use look like, and where
do I go next?

## Three attention tiers

### Tier 1 — immediate understanding

The first screen should normally contain:

1. project name;
2. one concrete value proposition;
3. a small set of meaningful badges, when repository evidence supports them;
4. a screenshot, GIF, terminal recording, or diagram only when it explains the
   value faster than prose and an authentic asset exists;
5. useful top-level links such as docs, demo, or issue tracker only when they
   help a visitor decide or start.

Do not bury the project identity below a long preamble, badge wall, generic
marketing paragraph, or table of contents. The value proposition should say
what the project does and for whom or why it matters. Replace phrases such as
"a powerful modern solution" with a concrete capability.

### Tier 2 — adoption

Select the sections that help a visitor decide and get a first result. A common
order is:

1. **Why / Overview / Problem** — only when the one-liner needs context;
2. **Features / Benefits** — user-visible outcomes, not internal components;
3. **Quick Start** — the shortest realistic supported path;
4. **Usage / Examples** — one representative happy-path example;
5. **Install or prerequisites** — separate these only when the project needs
   setup detail that would make Quick Start hard to scan.

The headings may change by project type. Do not add a section when it answers
no important reader question.

### Tier 3 — supporting navigation

Keep this area compact. Use short descriptions and links to existing canonical
resources for configuration, full API or CLI reference, architecture, advanced
examples, troubleshooting, development, contributing, security, releases, and
license details. A short license statement and a concise contribution link may
remain inline. Deep material belongs in `docs/` or another established home,
not copied into the main README.

Use GitHub's rendered outline instead of a manual table of contents by default.
Add a table of contents only when the final README is long or genuinely complex
and the navigation benefit outweighs the extra visual noise.

## Quick Start is a first-class deliverable

Quick Start should move a new user from zero to a useful result through one
obvious path:

- derive commands from the repository's real manifest, scripts, task runners,
  CLI definitions, examples, and supported runtime;
- use the normal or recommended package manager instead of listing every
  equivalent;
- include only prerequisites that block the path;
- make commands copy-pasteable and keep explanations near the decision they
  clarify;
- show the smallest useful code example or CLI invocation;
- state the expected result or next action when it prevents confusion.

For a library, install the actual package and show the smallest current import
and call. For a CLI, show the actual install and one normal input. For an
application or service, show the supported install/start path and how to reach
its first useful screen or endpoint. Never copy a generic npm, pip, Docker, or
CLI example without verifying it against the repository.

## Select sections by project type

Adapt the reader journey without forcing identical headings:

- **Library/package:** package installation, one import/API example, supported
  runtime, and links to full API/reference docs.
- **CLI/developer tool:** installation, one copy-paste command, representative
  input/output, supported platforms, and links to full flags/configuration.
- **Application/service:** local start path, prerequisites or required services,
  first useful workflow, relevant configuration minimum, and links to deployment
  or operations docs.
- **Framework/plugin/action:** the host ecosystem, integration/install step,
  smallest working example, compatibility constraints, and canonical guides.
- **Template/starter:** what it creates, how to use it to create the first
  project, and what is intentionally left to the generated project.
- **Agent Skill:** what the skill enables, how to invoke its distinct modes or
  outcomes, how to install it in the supported skill ecosystem, and what it
  does not cover. Do not turn the README into a copy of `SKILL.md`.
- **Monorepo:** the repository-level purpose and the shortest path to the main
  product; link to workspace-specific READMEs for package detail.

## Features, benefits, and mechanism

Features explain what users can accomplish. Write short, concrete,
benefit-oriented bullets and order the most decision-relevant capabilities
first. Use a compact table only when it improves a real comparison.

- Good: `Finds unused dependencies before they reach production.`
- Not a feature: `Uses an AST traversal pipeline with three compiler passes.`

A short "How It Works" explanation is appropriate only when the mechanism is
necessary to evaluate or use the project, or when it explains an important
constraint. Otherwise move architecture and implementation detail to a
canonical document and link to it.

## Badges and visuals

Badges are optional trust signals, not decoration. Select only those whose
meaning and target URL are established. A useful priority is:

1. release or package version;
2. CI/build status;
3. license;
4. coverage when meaningful;
5. downloads or adoption when useful;
6. runtime/platform compatibility.

Avoid vanity badges for stars, forks, arbitrary technologies, or social accounts
unless they carry unusual decision value for this project. Do not add a badge
because a template has a placeholder for it.

Use authentic repository screenshots, recordings, diagrams, or terminal output
when they communicate the value substantially faster than prose. Do not invent
or generate a product visual, demo, logo, screenshot, or performance chart to
fill an empty slot. Non-visual libraries and small utilities may need none.

## Examples and progressive disclosure

Prefer one excellent, current example over several variations. Verify imports,
flags, output, and setup against repository truth. Keep advanced examples in
existing `examples/`, `docs/`, API references, or dedicated guides and link to
them. Do not create placeholder documentation to justify a link.

Apply a simple placement test to every section: if removing it would make a
prospective user less likely to install, run, or try the project, keep it in
the README; otherwise prefer a concise teaser and a link to the canonical
resource. A deep topic should get a substantive one-to-three-sentence teaser,
not a vague "see docs" line.

Use `<details>` only for genuinely optional, short content when a separate
file would be disproportionate. Never hide the primary value proposition,
Quick Start, prerequisites, or normal usage, and never use collapsed content to
avoid organizing material that belongs in a proper reference document.

## Tone, length, and boundaries

Use direct language, short paragraphs, descriptive headings, active voice, and
project-specific terminology. Preserve a clear existing author voice when it
remains useful. Avoid hype, generic AI prose, repetitive summaries, excessive
emojis, badge walls, boilerplate acknowledgments, back-to-top links, and
unnecessary roadmaps.

Lean is the default. There is no universal line count: remove or relocate
material when doing so improves comprehension without losing a decision or
working path. The README should not become the canonical home for internal
architecture, exhaustive API or CLI references, complete configuration or
environment variables, deployment internals, directory walkthroughs, long
troubleshooting guides, changelogs, roadmaps, or full contributor workflows.

Keep support, contributing, security, and license information proportional:
link to existing canonical files and channels, state the license accurately,
and avoid legal or process essays in the main README.
