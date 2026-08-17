# Prioritization

Choose the next testing improvement as a risk decision, not a backlog of
uncovered files. Generate a few candidates internally, compare them
qualitatively, and recommend one bounded improvement slice. The slice should
be large enough to close a meaningful risk and small enough to validate and
review as one iteration.

## Compare candidates

For each candidate, ask:

- What important failure could this catch or prevent?
- How much confidence would it add at the seam where changes occur?
- What is the smallest implementation effort?
- What ongoing maintenance and runtime cost will it add?
- Does it require an architectural seam or new tool?
- Will it improve or harm developer feedback speed and trust?
- Can completion be verified with a repeatable command?

Do not turn these questions into numeric ROI or maturity scores. Explain the
tradeoff in plain language.

## Scope the iteration

The unit of planning is a bounded behavior slice, not a single test and not an
entire gap category. Start with one primary risk, one main seam or test level,
and a clear completion command. Include the directly enabling pieces—such as a
fixture, runner setup, minimal seam, focused command, or CI visibility—and the
related scenarios needed to make the signal trustworthy.

A useful default is to cover the important success outcome plus the most
consequential failure or boundary outcome when both belong to the same risk.
This is guidance, not a test-count target: use fewer checks when one fully
captures the risk, and add more only when they close the same behavior slice.
Stop before a second independent risk, broad cleanup, framework migration, or
coverage campaign.

Examples of appropriately sized slices:

- **No runner:** establish the natural runner and command, then protect one
  important boundary with a small representative set of scenarios—not a full
  testing pyramid.
- **Missing application boundary:** add the smallest seam and the key success
  plus rejection/side-effect cases for that boundary—not every endpoint.
- **Flaky valuable group:** remove the nondeterminism in the affected setup and
  checks, adding a focused guard when it prevents regression—not a whole-suite
  reliability rewrite.
- **CI gap:** wire the existing focused command into CI with visible failure
  reporting and preserve the local path—not a new task framework.

## Typical bounded-slice matrix

| Repository evidence | Usually worth considering first | Avoid in the same iteration |
| --- | --- | --- |
| No runner and no meaningful tests | Natural ecosystem runner + one meaningful behavioral slice | A complete unit/integration/E2E stack |
| Runner exists, zero tests | A small representative slice at an important existing seam | Tests for every module |
| Only trivial utility tests | One core business or user-facing slice with its key outcomes | More low-risk utility tests |
| Valuable tests exist but CI skips them | Run the existing focused path in CI with visible failure reporting | Adding a parallel framework |
| Flaky critical tests | Stabilize the affected high-value group and its nondeterministic setup | Expanding suite size first |
| Slow feedback blocks normal use | Improve targeted selection, isolation, or expensive setup for one valuable path | Deleting meaningful coverage without evidence |
| Many mocked unit tests miss boundaries | One behavior-oriented integration or contract slice | Mocking more internal collaborators |
| Mostly expensive E2E tests | Move one valuable behavior to a cheaper reliable seam when fidelity permits | Replacing all E2E coverage |
| High-churn important path is weakly protected | One focused regression/characterization slice with related outcomes | Coverage-driven additions elsewhere |
| Existing behavior is unclear | Characterize the most consequential behavior slice | Rewriting behavior and tests together |
| Important behavior is impossible to observe | Smallest useful seam, then enough checks to prove it | Broad dependency-injection or architecture migration |
| Risk coverage and reliability are strong | No work for now | Testing activity for its own sake |

The repository's evidence overrides this table.

## Choosing the mode

- **Test-first:** new behavior has a clear observable contract and a useful
  existing seam. Write the smallest useful set of failing scenarios for that
  slice, implement the minimum, then keep the loop small.
- **Characterization-first:** existing behavior is poorly understood or legacy
  code has no reliable contract. Capture the important current outcomes in one
  behavior slice before changing it.
- **Regression-first:** an understood bug or existing behavior needs durable
  protection. Reproduce the failure or expected outcome at the public seam and
  cover the closely related outcome when it is part of the same risk.
- **Architecture-first:** the only available test would assert internals or
  require excessive mocks/setup. Change only the dependency or interface that
  blocks meaningful observation, then add the smallest complete behavioral
  slice at that seam.
- **Reliability/stability:** a valuable test group cannot be trusted due to
  flakiness, order dependence, shared state, timing, or uncontrolled external
  effects. Restore deterministic feedback for that group before adding cases.
- **CI/infrastructure:** tests are useful locally but are not run, visible, or
  reproducible in the normal change workflow. Repair that path, including the
  focused command and failure visibility when needed, instead of duplicating
  tests or adding another framework.
- **No work:** the current suite protects the important risks with trustworthy
  feedback and no additional slice has a compelling cost/benefit case.

Do not enforce TDD retroactively on existing repositories. Do not use a test
that passes only because it repeats production logic, and do not claim an
architecture-first pass is justified merely because isolated unit tests would
be convenient.

## High-value versus low-value examples

Higher-value improvements include:

- one integration slice protecting a checkout, authorization, persistence, or
  destructive-operation boundary with its key success and failure outcomes;
- one characterization slice around a legacy transformation whose behavior is
  relied on but undocumented, including the consequential boundary case;
- repairing a critical flaky test group and its nondeterministic setup so
  developers trust a command that already protects important behavior;
- wiring an existing valuable focused suite into the CI path that reviews
  changes and making its failures visible.

Lower-value improvements include:

- adding tests to every simple accessor or file solely because a report marks it
  uncovered;
- introducing a new runner because it is newer or fashionable;
- adding broad snapshots that only detect markup churn without asserting an
  important user-visible outcome;
- building a large test-double hierarchy to avoid one small, useful seam.

## Completion criteria

Define “done” before implementation. Good criteria usually include:

- the selected behavior slice is exercised through the named seam, including
  its key success, failure, or boundary outcomes when they are part of the
  same risk;
- the new or repaired checks fail for the intended breakage when that proof is
  practical;
- the slice passes reliably through the repository's existing command;
- relevant CI executes it when CI is in scope;
- no unnecessary framework or architecture migration was introduced; and
- the final diff contains only the selected slice and its directly enabling
  work.

Do not enforce TDD retroactively on existing repositories. Do not use a test
that passes only because it repeats production logic, and do not claim an
architecture-first slice is justified merely because isolated unit tests would
be convenient. A small cluster of related scenarios is still one iteration;
independent risks should be deferred.
