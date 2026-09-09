---
name: project-specs
description: >
  Turn a finished brainstorm into a durable pre-implementation specification in
  the current repository: project brief, research catalog, architecture with
  confidence labels, version roadmap, V0 tasks, and an agent handoff. Use when
  the user wants to spec a project or experiment before coding, prepare pre-v0
  docs, create an implementation roadmap from a brainstorm, document a project
  so another agent can implement it incrementally, finish brainstorming and
  write the docs, or make the project plan and V0 tasks. Also use when
  exploration has clearly ended and the next step is organizing everything
  needed before implementation. Do not use for ordinary planning questions,
  small coding tasks, starting implementation, writing the main README, or
  general Markdown cleanup. Write or update docs/project-slug/ and stop before
  building.
---

# Project Specs

Capture a finished exploration as a durable implementation package inside the
repository. The package should be strong enough to review before building,
re-enter weeks later, and hand near-term tasks to a capable but less intelligent
coding model.

This skill is the step immediately before V0:

**brainstorm → project specification → version roadmap → executable tasks → V0**

It does not implement the project.

## Choose the mode

- **Create** when no project specification package exists yet.
- **Update** when a matching package already exists. Read it first and follow
  the update behavior in [spec-structure.md](references/spec-structure.md).
  Implementation reality wins over outdated planning assumptions.

If the request is only a small coding task, an ordinary design question, a main
README rewrite, or general Markdown cleanup, do not use this skill.

## Operate in this order

Follow this pipeline; do not begin by filling a template:

**gather → inspect → classify → research → specify → decompose → review → summarize → stop**

1. **Gather.** Use whatever is available: the current conversation, user notes
   or handoffs, existing code and experiments, mentioned URLs, and previous spec
   files. Do not require every input. Do not ask for missing optional material
   unless two interpretations would produce materially different packages.
2. **Inspect.** Map the repository enough to reuse real infrastructure: stack,
   packages, conventions, existing experiments, constraints, and nearby code.
   Prefer concrete paths over generic architecture. Do not read the entire
   codebase blindly.
3. **Classify.** Separate what is decided, provisional, speculative, or in
   contradiction with earlier brainstorm turns. Identify assumptions that need
   experiments, technical risks, existing systems to reuse, things that should
   not be built yet, and premature abstractions.
4. **Research.** Preserve every important external reference. If browsing is
   available and understanding a linked repository, article, demo, paper, model,
   or tool would materially improve the spec, inspect it instead of judging it
   from its title. Catalog what to borrow and what not to copy blindly.
5. **Specify.** Read [spec-structure.md](references/spec-structure.md). Create or
   update the project directory. Prefer an established repository documentation
   convention when one already exists; otherwise use `docs/<project-slug>/`.
6. **Decompose.** Read [task-design.md](references/task-design.md). Turn the
   destination into versions with observable outcomes. Thoroughly task-split
   only near-term versions, especially V0. Keep far-future versions directional.
7. **Review.** Read [quality-checklist.md](references/quality-checklist.md) and
   fix inconsistencies before finishing.
8. **Summarize, then stop.** Return the compact handoff below. Do not start V0,
   scaffold production architecture, or "just implement the first task."

## Hard rules

- This is a planning skill. Tiny API or pseudocode sketches are allowed when
  they clarify a design; production code, refactors, frameworks, and V0
  implementation are not.
- Do not silently resolve major product questions. Label uncertainty. Prefer an
  experiment in an early version over an invented decision.
- Never promote a brainstorm idea to an accepted architectural decision just to
  make the spec look complete.
- Prefer adapting what already exists in the repository over proposing a greenfield
  stack.
- Record tempting generalizations as premature abstractions until multiple
  concrete implementations justify them. Prefer
  `concrete example → second example → emerging pattern → abstraction`.
- Each project or experiment gets its own directory. Do not dump every idea into
  one global specification.
- Omit a spec file only when it genuinely does not apply, and say why in
  `README.md`'s documentation map.

## Final response

After writing or updating the package, do not begin building. Reply with:

1. **Interpretation** of the project
2. **Documentation path**
3. **Version progression**
4. **Chosen V0 and why**
5. **Major architectural decisions**
6. **Biggest unresolved questions**
7. **Disagreements or concerns** about the brainstorm
8. **Recommended first implementation task**

Then stop.
