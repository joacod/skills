# Prioritization

Choose the next testing improvement as a risk decision, not a backlog of
uncovered files. Generate a few candidates internally, compare them
qualitatively, and recommend exactly one coherent pass.

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

## Typical first-pass matrix

| Repository evidence | Usually worth considering first | Avoid in the same pass |
| --- | --- | --- |
| No runner and no meaningful tests | Natural ecosystem runner + one meaningful behavioral test | A complete unit/integration/E2E stack |
| Runner exists, zero tests | One tracer test at an important existing seam | Tests for every module |
| Only trivial utility tests | One core business or user-facing behavior | More low-risk utility tests |
| Valuable tests exist but CI skips them | Run the existing suite in CI with visible failure reporting | Adding a parallel framework |
| Flaky critical tests | Stabilize the highest-value failure and remove its nondeterminism | Expanding suite size first |
| Slow feedback blocks normal use | Improve targeted selection, isolation, or expensive setup | Deleting meaningful coverage without evidence |
| Many mocked unit tests miss boundaries | One behavior-oriented integration or contract test | Mocking more internal collaborators |
| Mostly expensive E2E tests | Move one valuable behavior to a cheaper reliable seam when fidelity permits | Replacing all E2E coverage |
| High-churn important path is weakly protected | One focused regression/characterization test | Coverage-driven additions elsewhere |
| Existing behavior is unclear | Characterize the most consequential behavior | Rewriting behavior and tests together |
| Important behavior is impossible to observe | Smallest useful seam, then one test | Broad dependency-injection or architecture migration |
| Risk coverage and reliability are strong | No work for now | Testing activity for its own sake |

The repository's evidence overrides this table.

## Choosing the mode

- **Test-first:** new behavior has a clear observable contract and a useful
  existing seam. Write one focused failing scenario, implement the minimum,
  then keep the loop small.
- **Characterization-first:** existing behavior is poorly understood or legacy
  code has no reliable contract. Capture important current behavior before
  changing it.
- **Regression-first:** an understood bug or existing behavior needs a durable
  check. Reproduce the failure or expected outcome at the public seam.
- **Architecture-first:** the only available test would assert internals or
  require excessive mocks/setup. Change only the dependency or interface that
  blocks meaningful observation, then add the smallest behavioral test.
- **Reliability/stability:** a valuable test exists but cannot be trusted due to
  flakiness, order dependence, shared state, timing, or uncontrolled external
  effects. Restore deterministic feedback before adding cases.
- **CI/infrastructure:** tests are useful locally but are not run, visible, or
  reproducible in the normal change workflow. Repair that path instead of
  duplicating tests.
- **No work:** the current suite protects the important risks with trustworthy
  feedback and no additional pass has a compelling cost/benefit case.

Do not enforce TDD retroactively on existing repositories. Do not use a test
that passes only because it repeats production logic, and do not claim an
architecture-first pass is justified merely because isolated unit tests would
be convenient.

## High-value versus low-value examples

Higher-value improvements include:

- one integration test protecting a checkout, authorization, persistence, or
  destructive-operation boundary that currently has no meaningful protection;
- one characterization test around a legacy transformation whose behavior is
  relied on but undocumented;
- repairing a critical flaky test so developers trust a command that already
  protects important behavior;
- wiring an existing valuable suite into the CI path that reviews changes.

Lower-value improvements include:

- adding tests to every simple accessor or file solely because a report marks it
  uncovered;
- introducing a new runner because it is newer or fashionable;
- adding broad snapshots that only detect markup churn without asserting an
  important user-visible outcome;
- building a large test-double hierarchy to avoid one small, useful seam.

## Completion criteria

Define “done” before implementation. Good criteria usually include:

- the selected behavior is exercised through the named seam;
- the new or repaired check fails for the intended breakage when that proof is
  practical;
- it passes reliably through the repository's existing command;
- relevant CI executes it when CI is in scope;
- no unnecessary framework or architecture migration was introduced; and
- the final diff contains only the selected pass.
