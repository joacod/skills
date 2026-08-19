# Markdown Document Roles

Markdown quality is role-dependent. Use this map to decide what “better” means
before applying shared formatting conventions.

| Role | Primary reader question | Useful structure | Protect |
| --- | --- | --- | --- |
| README / landing page | What is this, why does it matter, and how do I start? | identity, value, quick start, one representative use, deeper links | onboarding path, project voice, verified commands |
| Guide / tutorial | How do I accomplish this task? | goal, prerequisites, ordered steps, expected result, next steps | sequence, prerequisites, copy-pasteable examples |
| API / reference | What does this symbol, option, or endpoint do? | lookup headings, signatures, parameters, examples, constraints | names, types, defaults, version semantics |
| How-to / runbook | What should I do in this operational situation? | trigger, prerequisites, steps, checks, rollback or escalation | safety boundaries and explicit conditions |
| ADR / design record | What decision was made and why? | status, context, decision, alternatives, consequences | historical truth and decision scope |
| Changelog / release notes | What changed in this release? | version/date, categorized entries, links, migration notes | chronology, release identity, factual attribution |
| Contributor / development guide | How do I work on this repository? | prerequisites, setup, workflow, focused checks, contribution rules | repository-native commands and policy wording |
| Issue / pull-request template | What information must a contributor provide? | placeholders, checklists, comments, required fields | template markers, HTML comments, automation cues |
| Policy / governance document | What rule or expectation applies? | scope, normative guidance, exceptions, ownership, review date | precise language, obligations, exceptions |
| Agent-facing instructions | What behavior should an automated contributor follow? | scope, priorities, commands, boundaries, escalation | front matter, directives, safety constraints, precedence |
| Generated or machine-consumed Markdown | What stable format does a tool parse or publish? | tool-defined schema or markers | exact syntax, markers, ordering, regeneration workflow |

## Classification clues

Use repository evidence rather than filenames alone:

- A root `README.md` is usually the public front door, but a package or docs
  site may have a different entry point.
- `docs/`, `guides/`, and tutorial paths usually indicate reader journeys, but
  front matter and site configuration can change the renderer and navigation.
- `adr/`, `decisions/`, or dated design files often preserve history; do not
  rewrite them into current guidance without an explicit request.
- `CHANGELOG.md`, `release-notes/`, and generated release pages may be consumed
  by release tooling or links; preserve their chronology and markers.
- `.github/`, `.devcontainer/`, `templates/`, and files named in CI or scripts
  can be machine-facing even when they render as Markdown.
- `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and policy files may be
  instructions rather than ordinary prose; formatting changes must not weaken
  precedence, commands, or safety boundaries.
- A generated header, HTML comment, front-matter key, or `<!-- START/END -->`
  marker is an interface until its producer and consumer are understood.

## Shared checks versus role-specific checks

Shared checks are usually safe across roles:

- links point to real intended targets;
- headings form a usable outline for the renderer;
- code fences and tables parse as intended;
- images have usable paths and alternative text;
- examples and claims are not silently invented;
- the diff does not contain unrelated churn.

Role-specific checks should remain distinct:

- a README needs a clear first-use path;
- a tutorial needs a reliable sequence and expected result;
- a reference needs lookup accuracy and stable terminology;
- an ADR needs historical integrity;
- a template needs placeholders and automation markers;
- an instruction file needs semantic precedence and safe boundaries;
- generated Markdown needs regeneration evidence rather than hand formatting.

When a repository has multiple families, record the boundary and use the
narrowest convention that satisfies each consumer. Consistency is useful when
it lowers reader effort; it is harmful when it erases a document's job.
