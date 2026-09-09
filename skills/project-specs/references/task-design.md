# Task design

Load this when writing `04-version-roadmap.md` or `05-implementation-tasks.md`.

The destination is a sequence of meaningful implementations, not a miniature of
the final system in every early version. Optimize early versions for
**learning value + tangible output**. The package still has to name the last
form and the versions that get there.

## Version roadmap

Do not force a numbering scheme. Choose versions that make sense for the
project. A common shape is `V0`, `V0.1`, `V0.2`, `V1`, `V2`, desired state.

Write the **entire** progression: first useful version through the desired last
form. The last version is the destination from `README.md` and
`02-product-and-experience.md`, not an optional epilogue.

Each version must produce something observable, usable, or informative. V0 is
not "a tiny version of every final feature." It is the smallest implementation
that tests an important assumption and leaves something a person can run, see,
or inspect.

### Confidence by distance

- **Current near-term version (V0 on create):** high confidence, detailed,
  fully task-split.
- **Immediately following versions:** medium-high detail. Enough that a later
  update pass can decompose them without the original brainstorm.
- **Far future versions, including the desired last form:** directional, but
  specific about capability and experience. Do not replace them with "TBD" or
  omit them.

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

Translate only the **current near-term** roadmap version into concrete tasks.
On create that is V0. On update, after V0 (or the just-finished version) is
done, that is the next incomplete version.

The immediately following version may stay at medium-high roadmap detail until
it becomes current. Far-future versions, including the desired last form,
normally stay at roadmap level until then.

Use IDs such as `V0-T01`, then `V0.1-T01` or `V1-T01` when that version becomes
current.

Write each current-version task so an agent who never saw the brainstorm can
complete it from the task plus the spec files it cites. Include the context,
paths, constraints, and verification that would otherwise live only in chat.

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

Every current-version task should contribute directly to that version. V0 must
not secretly require later-version infrastructure.

## Update behavior

When reconciling an existing spec with implementation, including after a
version or experiment lands:

- Mark completed tasks and versions as completed.
- Keep their original intent visible; add what actually shipped.
- Move invalidated future work rather than pretending it was never planned.
- Re-read each completed version's expected learnings and possible roadmap
  impact; change later versions when the result warrants it.
- Keep the desired last form unless the new evidence changes it; if it
  changes, say so in the brief, product doc, and last roadmap version.
- Split, merge, or rewrite incomplete tasks for the **new** current version
  with the same thoroughness V0 originally received.
- Leave still-distant versions at roadmap level.
- Record assumption changes in `STATUS.md` and in the relevant decision or
  question entries.
