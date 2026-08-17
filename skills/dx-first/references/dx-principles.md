# DX principles

`dx-first` translates developer-experience research into repository-level
interventions. It is not a survey instrument, an employee-satisfaction score,
or a catalog of fashionable tools.

## What to optimize

Developer experience is how developers think about, feel about, and value their
work. A repository cannot observe every part of that experience, but it can
change many of the conditions that shape it. Look for unnecessary effort between
**clone → understand → setup → run → change → validate → debug → ship**.

Use three practical outcomes as the foundation:

### Reduce cognitive load

Make the next useful action discoverable, keep conventions consistent, state
implicit prerequisites, and reveal complexity progressively. Prefer one
well-supported happy path over a menu of equivalent paths. Bound autonomy with
clear constraints so developers know both what is safe to change and where an
escape hatch exists.

Cognitive load includes more than the number of commands. Count concepts to
remember, files to synchronize, unexplained ordering, context switches, hidden
state, and choices that the repository could safely decide for the common case.

### Shorten feedback loops

A fast signal is valuable only when it is trustworthy and scoped to the change.
Expose the smallest useful check for a small edit, keep broader confidence checks
available, and make failures actionable. Small batches, reliable test automation,
local validation, and CI that calls the same underlying tasks reduce the distance
between an edit and a confident decision.

Do not optimize for activity such as command count, lines changed, number of
checks, or time spent in tools. Optimize the developer's ability to learn what
the change means and what to do next.

### Protect flow

Flow is fragile when a developer waits on an unnecessarily broad check, leaves
the repository to find an answer, chooses between competing wrappers, or loses
state after a failure. Favor predictable startup, focused feedback, useful logs,
clear recovery, and small coherent changes. A good default should let a developer
make progress immediately without preventing advanced workflows.

## Paved paths, defaults, and escape hatches

The preferred way to do a frequent task should also be the easiest way to do it.
At repository scale this means an obvious path for starting development, running
one relevant test, running the suite, formatting, linting, type checking,
building, generating artifacts, and validating a change when those tasks apply.

Choose sensible defaults for the common case and disclose advanced options only
when needed. Keep a legitimate override possible for unusual environments,
performance-sensitive work, or expert workflows. Do not turn every option into
an onboarding decision.

A paved path is a supported behavioral contract, not necessarily a new wrapper.
If an existing native command is already the shortest reliable path, document or
rename it before adding another abstraction.

## Tooling must pay rent

Every dependency, wrapper, task runner, container, hook, generator, service,
and configuration layer adds concepts and maintenance. Before adding one, ask:

1. What concrete friction does it remove?
2. How often does that friction occur and who is affected?
3. Can the existing stack solve it more simply?
4. What new concept, failure mode, or owner does it introduce?
5. Does the net experience improve after maintenance cost is included?

Prefer removing duplicate scripts, stale setup, unsupported alternatives,
manual synchronization, and surprising defaults. A smaller command surface is
often a larger DX improvement than a more sophisticated one.

## Evidence over activity

Measure lived repository journeys where possible: steps, observed durations,
required services, configuration prompts, targeted-check duration, reproducible
failure output, and local/CI command differences. Otherwise report observable
friction without inventing time estimates.

Use confidence-aware evidence:

- **TESTED** — the path or behavior was directly executed or observed.
- **VERIFIED** — configuration, source, or documentation statically confirms it.
- **INFERRED** — a reasonable conclusion from incomplete evidence; label it and
  avoid presenting it as behavior that was tested.

A file's existence is not proof that its instructions work. A green CI badge is
not proof that a developer can reproduce the check locally. A fast command is
not useful feedback if it is flaky or opaque. Numeric scores are optional and
usually less informative than a ranked friction inventory.

## Reproducibility without cargo cult

Use explicit dependencies, runtime and package-manager declarations, lockfiles,
clear configuration, safe examples, and deterministic setup when they solve a
real problem. For services, explicit build/run boundaries, attached backing
services, and reasonable development/production parity can prevent machine-
specific surprises. Apply those ideas in context: a library, CLI, embedded
project, static tool, or data workflow may need a different contract.

Development containers are one possible reproducibility mechanism, not a default.
First determine whether pinning versions, declaring system prerequisites,
reusing existing ecosystem configuration, or a container is the simplest durable
answer.

## Actionable feedback and recovery

Useful feedback identifies:

1. what failed;
2. why it failed;
3. where to inspect; and
4. what action is likely to fix or retry it.

Apply this to startup errors, missing configuration, test failures, lint output,
CLI help, generated artifacts, and CI failures. Preserve useful context and make
reset, retry, or targeted reproduction discoverable. Do not hide detail behind a
friendly message; provide progressive disclosure from a concise next action to
diagnostic output.

## Human and agent legibility

Canonical commands, explicit constraints, navigable structure, accurate docs,
deterministic validation, and documented unusual decisions help both humans and
coding agents. Agent-specific maps or instructions are appropriate only when the
repository clearly uses them or they solve a demonstrated navigation problem.
Human comprehension remains the acceptance bar.

## Continuous improvement

Adapt the research framework's ask–plan–act loop to a repository:

1. **Ask:** make friction visible through an actual journey, developer report,
   support question, or reproducible failure.
2. **Plan:** select a high-impact, frequent, confident improvement; identify its
   owner, validation, and maintenance cost.
3. **Act:** make a small change, rerun the journey, and repeat only if the
   evidence shows the next change still pays for itself.

The repository is not a blank slate. Preserve useful conventions and intentional
tradeoffs. Improve incrementally rather than replacing a working ecosystem for
fashion.

## Research basis and deliberate boundaries

This synthesis draws on the following sources, but the skill is self-contained
and does not need to fetch them during execution:

- [An Actionable Framework for Understanding and Improving Developer Experience](https://arxiv.org/abs/2205.06352) — grounds DX in cognition, affect, and conation; emphasizes context, frequency, actionable factors, barriers, ownership, and continuous small improvements.
- [DevEx in Action](https://www.microsoft.com/en-us/research/publication/devex-in-action-a-study-of-its-tangible-impacts/) — reinforces developer-centered experience over output proxies, feedback-loop quality, cognitive load, flow, and measuring lived experience rather than activity alone.
- [gstack devex-review](https://github.com/garrytan/gstack/blob/main/devex-review/SKILL.md) — contributes live journey testing, getting-started and error testing, and evidence labels.
- [gstack plan-devex-review](https://github.com/garrytan/gstack/blob/main/plan-devex-review/SKILL.md) — contributes first-five-minutes thinking, progressive disclosure, sensible defaults, escape hatches, and context-switch reduction.
- [OpenAI agentic-legibility](https://github.com/openai/build-hours/blob/main/24-api-codex/skills/agentic-legibility/SKILL.md) — contributes bootstrap self-sufficiency, discoverable entrypoints, validation harnesses, structured docs, and repository-visible evidence.
- [shadcn improve](https://github.com/shadcn/improve/blob/main/skills/improve/SKILL.md) — contributes reconnaissance before judgment, exact evidence, prioritization, confidence, verification baselines, and intentional-tradeoff checks.
- [DORA capabilities](https://dora.dev/capabilities/) — informs continuous integration and delivery, test automation, documentation quality, small batches, local confidence, and reliable delivery without turning this into a maturity audit.
- [Backstage](https://backstage.io/) — supplies the golden-path principle: make the supported way the easiest way, without requiring Backstage or a platform.
- [Development Containers](https://containers.dev/) — treats declarative environments as an option for a demonstrated reproducibility problem, not a ritual prerequisite.
- [The Twelve-Factor App](https://12factor.net/) — supplies context-dependent guidance on explicit dependencies and config, attached services, build/run boundaries, and dev/prod parity.
- [Diátaxis](https://diataxis.fr/) — helps distinguish tutorials, how-to guides, reference, and explanation when documentation organization is causing friction.

Intentionally not adopted as requirements: numeric scorecards or time-to-hello-
world benchmarks, competitive-product benchmarking, community/ecosystem audits,
interactive persona ceremonies, employee surveys, agent-only infrastructure,
mandatory containers or task runners, and broad security/performance/
architecture audits. Use any of these only when the user explicitly asks and the
repository evidence makes them relevant.
