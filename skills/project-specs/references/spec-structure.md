# Spec structure

Load this when creating or updating any file in the project specification
package.

- [Location](#location)
- [Package files](#package-files)
- [Confidence labels](#confidence-labels)
- [README.md](#readmemd)
- [STATUS.md](#statusmd)
- [01-context-and-research.md](#01-context-and-researchmd)
- [02-product-and-experience.md](#02-product-and-experiencemd)
- [03-architecture.md](#03-architecturemd)
- [04-version-roadmap.md and 05-implementation-tasks.md](#04-version-roadmapmd-and-05-implementation-tasksmd)
- [06-decisions-and-open-questions.md](#06-decisions-and-open-questionsmd)
- [07-agent-handoff.md](#07-agent-handoffmd)
- [Updating an existing package](#updating-an-existing-package)

## Location

Default path: `docs/<project-slug>/`

Choose `<project-slug>` as a short filesystem-safe name for this project or
experiment (`story-studio`, `soft-matter`, `webaudio-engine`). Derive it from
the project's identity, not the chat title.

If the repository already has a strong documentation convention for project
specs, ADRs, or experiment writeups, follow that convention instead of
inventing a parallel tree. Still keep each project or experiment in its own
directory.

If a matching package already exists, update it. Search for an existing
directory before creating a new one. Ask only when two existing packages could
reasonably be the same project.

## Package files

Create or update:

| File | Role |
| --- | --- |
| `README.md` | Durable project brief and entry point |
| `STATUS.md` | Short mutable checkpoint for the next session |
| `01-context-and-research.md` | Origin, repo context, external references |
| `02-product-and-experience.md` | Intended experience, independent of implementation |
| `03-architecture.md` | Components and boundaries with confidence labels |
| `04-version-roadmap.md` | Sequence of meaningful implementations |
| `05-implementation-tasks.md` | Near-term executable tasks |
| `06-decisions-and-open-questions.md` | ADRs and unknowns, kept separate |
| `07-agent-handoff.md` | Compact entry for future coding agents |

Omit a file only when it genuinely does not apply. Do not collapse every
project into one giant document.

## Confidence labels

Use these labels in architecture, decisions, and other claims where useful:

- **DECIDED** — supported by the brainstorm and compatible with the repo
- **PROVISIONAL** — current working choice, cheap to change
- **HYPOTHESIS** — plausible, unproven
- **NEEDS EXPERIMENT** — should be learned by building or measuring, not by
  more discussion
- **FUTURE POSSIBILITY** — directional; do not task-split yet

## README.md

Durable brief. A later agent should be able to read this and `STATUS.md` and
know what the project is.

### What we are building

Plain-language explanation.

### Why

Motivation and the opportunity or problem.

### Desired end state

What the mature system should enable and feel like. Capabilities and
experience, not implementation.

### Core principles

Only principles the project actually supports. Do not paste a generic list.
Possible examples, include only if true here: experiment before abstracting,
excellent developer experience, visual quality, deterministic behavior,
composability, reuse existing infrastructure, local-first, provider
independence.

### Non-goals

Tempting adjacent work the project is not trying to solve.

### Documentation map

One line per file in this directory, including any omitted file and why.

## STATUS.md

Keep this short and easy to rewrite after every implementation session.

### Current state

What actually exists now.

### Current version

Examples: `V0 — Not started`, `V0.2 — In progress`.

### Current task

Task ID and short description, or `none`.

### Completed

Important finished versions or tasks.

### Next

The next recommended task.

### Latest learnings

Discoveries from implementation or experiments. Empty on a first Create pass
unless the repo already taught something.

### Changes to original assumptions

What reality disproved or clarified. Empty until something changed.

### Blockers / open questions

Only currently relevant items. Link to `Q00x` IDs when they exist.

### Last updated

Use the current date when possible.

## 01-context-and-research.md

Preserve useful intellectual history without dumping the conversation.

### Origin

How the idea developed, including useful reasoning and changes of direction.

### Existing repository context

Relevant stack, packages, infrastructure, components, conventions, previous
experiments, reusable systems, and constraints. Use concrete repository paths.

### External reference catalog

For every important reference (GitHub repos, demos, articles, posts, papers,
models, libraries, tools, APIs, videos, examples):

- name
- URL
- what it is
- why it matters
- specific ideas worth borrowing
- what should not be copied blindly

### Related approaches

Comparable systems and lessons.

### Research questions

Things not yet known, and how they could be learned.

## 02-product-and-experience.md

Describe the intended product, creative, or developer experience independently
from implementation.

### Primary workflows

What someone should actually be able to do.

### Desired developer experience

Small hypothetical sketches of the ideal mature API or workflow. These are
design sketches, not commitments.

### Progressive complexity

Simplest, intermediate, and advanced usage when that distinction matters.

### Important qualities

Only qualities that matter here: iteration speed, responsiveness,
discoverability, visual quality, determinism, composability, debuggability,
portability, or others actually discussed.

### Success criteria

Observable signs the idea is succeeding.

## 03-architecture.md

### Existing architecture to reuse

Prefer adapting what already exists.

### Proposed major components

For each: responsibility, inputs, outputs, dependencies, and what it should
not own. Label confidence.

### Data/control flow

Use Mermaid when a diagram materially clarifies the architecture.

### Important boundaries

Interfaces that should remain clean.

### Extension points

Likely places later capabilities could attach. Mark distant ones as
FUTURE POSSIBILITY.

### Premature abstractions to avoid

Attractive generalizations that should wait until multiple concrete
implementations justify them.

### Technical risks

Hard areas, uncertainties, and possible mitigations.

## 04-version-roadmap.md and 05-implementation-tasks.md

Follow [task-design.md](task-design.md).

## 06-decisions-and-open-questions.md

Keep decisions and unknowns clearly separated.

### Decisions

Lightweight ADR entries:

```markdown
### D001 — Name

**Status:** accepted / provisional

**Decision**

...

**Reason**

...

**Alternatives considered**

...

**Revisit when**

...
```

Do not mint an accepted decision from an uncertain brainstorm idea.

### Open questions

IDs such as `Q001`. For each: the question, why it matters, when it needs
answering, the best method for answering it, and whether it blocks V0.
Prefer experiments over debate when that would settle the question.

## 07-agent-handoff.md

Keep this compact. Future coding agents should enter here quickly.

### Project

Very short description.

### Current state

Point to `STATUS.md`.

### Source of truth

Which files to read depending on the task.

### Rules for implementation agents

1. Read `README.md`, `STATUS.md`, the relevant roadmap version, and the
   assigned task before coding.
2. Implement only the current task or version unless a dependency genuinely
   requires otherwise.
3. Prefer the simplest solution that satisfies current acceptance criteria.
4. Reuse repository conventions and infrastructure.
5. Do not introduce generalized abstractions based on one example.
6. Run the required validation.
7. Update documentation when implementation reveals an incorrect assumption.
8. Record important new architectural decisions.
9. Preserve useful planning history rather than rewriting it so old
   predictions look correct.
10. Leave the repository working after each task.
11. Update `STATUS.md` after meaningful progress.

### How to continue

How to identify the next incomplete task.

### Completion report

Future coding agents should report:

- Task completed
- What changed
- Files changed
- Validation performed
- Deviations from spec
- New findings
- Documentation updates
- Recommended next task

## Updating an existing package

1. Read the existing documentation first.
2. Inspect the current implementation.
3. Reconcile documentation with reality.
4. Preserve useful completed history.
5. Update `STATUS.md`.
6. Revise future roadmap assumptions when necessary.
7. Do not recast completed versions as if the new plan had always existed.
