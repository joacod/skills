# Task design

Load this when writing `04-version-roadmap.md` or `05-implementation-tasks.md`.

The destination is a sequence of meaningful implementations, not a miniature of
the final system in every early version. Optimize early versions for
**learning value + tangible output**.

## Version roadmap

Do not force a numbering scheme. Choose versions that make sense for the
project. A common shape is `V0`, `V0.1`, `V0.2`, `V1`, `V2`, desired state.

Each version must produce something observable, usable, or informative. V0 is
not "a tiny version of every final feature." It is the smallest implementation
that tests an important assumption and leaves something a person can run, see,
or inspect.

### Confidence by distance

- **V0:** high confidence, detailed.
- **Immediately following versions:** medium-high detail.
- **Far future versions:** directional.

Do not write dozens of implementation tasks for speculative later versions.
Early implementation is allowed to change later architecture. The roadmap is a
living hypothesis, not a contract.

### Per-version sections

For every version include:

#### Goal

One clear outcome.

#### Why this version exists

Which uncertainty it resolves.

#### User-visible result

What can actually be run, seen, tested, or used afterward.

#### Scope

Included work.

#### Explicitly out of scope

Adjacent work that should wait.

#### Technical approach

Enough guidance without locking every implementation detail.

#### Dependencies

What it relies on.

#### Deliverables

Concrete outputs.

#### Acceptance criteria

Objective definition of done.

#### Validation / experiments

What needs to be tested, rendered, benchmarked, inspected, compared, or
measured.

#### Expected learnings

What this version should teach.

#### Possible roadmap impact

Which later assumptions or versions might change based on the result.

## Implementation tasks

Translate only near-term roadmap versions into concrete tasks. V0 should be
thoroughly decomposed. The next version can be reasonably detailed. Far-future
versions normally stay at roadmap level.

Use IDs such as `V0-T01`.

### Per-task sections

#### Objective

One focused outcome.

#### Context

Why the task exists.

#### Likely files / areas

Use actual repository paths when known.

#### Implementation instructions

Enough direction that a capable but lower-reasoning coding model does not need
to reconstruct the whole project. Local and reversible engineering decisions
can remain with that agent.

#### Constraints

What it must preserve or avoid.

#### Acceptance criteria

Verifiable completion conditions.

#### Verification

Name the actual checks: unit or integration tests, typecheck, lint, build,
screenshots, render output, benchmark, visual inspection, deterministic
comparison, console validation, interaction testing. Use only checks that
apply.

#### Dependencies

Prior task IDs where relevant.

#### Notes for implementation agent

Anything subtle a smaller model may otherwise miss.

## Sizing

Optimize tasks for focused coding-agent sessions.

Avoid vague work such as "implement the rendering architecture."

Prefer specific steps:

- add a minimal data representation
- implement one concrete renderer
- expose one API
- add one fixture
- implement deterministic replay
- add one example
- validate output

Tasks should minimize architectural inference without prescribing every line of
code.

Every V0 task should contribute directly to V0. V0 must not secretly require
V1 infrastructure.

## Update behavior

When reconciling an existing spec with implementation:

- Mark completed tasks and versions as completed.
- Keep their original intent visible; add what actually shipped.
- Move invalidated future work rather than pretending it was never planned.
- Split, merge, or rewrite only incomplete near-term tasks.
- Record assumption changes in `STATUS.md` and in the relevant decision or
  question entries.
