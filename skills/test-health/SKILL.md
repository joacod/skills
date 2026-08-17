---
name: test-health
description: >
  Audit a repository's automated testing health and recommend the smallest
  high-value next improvement. Use when assessing an existing test suite,
  introducing tests into an untested or legacy project, deciding what to test
  next, evaluating testing strategy or coverage, choosing between unit,
  integration, and end-to-end tests, investigating brittle or flaky tests, or
  determining whether a small architecture change is needed for testability.
  Detect and prefer the repository's existing stack and conventions. Improve
  testing incrementally rather than pursuing arbitrary coverage targets.
---

# Test health

Analyze the repository's current ability to detect important regressions, then
choose one improvement that makes future changes safer. Optimize for confidence
and risk reduction—not test count, line coverage, or testing activity.

This skill is a repository assessment and incremental-improvement playbook. It
is not a mandate to use TDD everywhere, add tests for every file, migrate the
testing stack, or make the repository fully tested in one run.

## Principles

Apply these principles directly:

- Treat coverage and test count as evidence, never as objectives. Do not set
  arbitrary percentages or pursue 100% coverage by default.
- Prefer one coherent improvement pass. Stop when its evidence is sufficient;
  do not attempt to improve every testing weakness at once.
- Prioritize important, risky, frequently changed, or historically buggy
  behavior over uncovered but unimportant lines.
- Test externally observable behavior through a stable interface or seam. Do
  not add tests merely to exercise implementation details.
- Prefer the repository's existing runner, framework, fixtures, and naming
  conventions when they are adequate. Introduce tooling only for a concrete,
  evidenced need.
- Treat flaky, slow, or hard-to-run tests as a trust problem. Stabilizing a
  valuable check can be more useful than adding another check.
- Use characterization tests when existing behavior is poorly understood. Use
  regression tests for understood existing behavior. For genuinely new
  behavior, prefer a small red → green → refactor loop at one observable seam
  when it helps; strict retroactive TDD is not required.
- If architecture prevents meaningful testing, create only the smallest useful
  seam. Do not broadly refactor toward a preferred architecture or mock every
  dependency just to test one class.
- Be willing to conclude **Good enough for now** when additional testing has
  low marginal value.

## Workflow

Follow this sequence. Gather evidence before choosing a recommendation.

1. **Understand the repository.** Read repository instructions, the README,
   manifests, build/workspace configuration, architecture notes, and relevant
   documentation. Detect languages, frameworks, package managers, entrypoints,
   and monorepo boundaries. Do not assume a particular ecosystem.
2. **Inventory testing infrastructure.** Locate test directories and naming
   conventions, test configuration, fixtures/fakes/mocks/snapshots, coverage
   configuration or reports, and CI configuration. Determine which test
   commands are actually documented or encoded in manifests, task runners, and
   CI. A dependency named `test` is not proof that a runnable suite exists.
3. **Collect deterministic evidence.** When command execution is available,
   run the portable helper bundled with this skill:

   ```text
   python3 path/to/test-health/scripts/inspect_test_health.py --root . --pretty
   ```

   It reports evidence only; it does not decide maturity or recommend work.
   If it cannot run, perform the same inspection manually and lower confidence
   rather than inventing results.
4. **Run the smallest relevant existing checks.** Inspect commands before
   executing them. Run a focused test command when one exists, then a broader
   existing suite when scope and time justify it. Also run relevant lint,
   typecheck, build, or packaging checks when the repository normally uses
   them. Report each as passed, failed, skipped, or unavailable. Never claim a
   command ran from configuration alone.
5. **Inspect CI.** Establish whether tests run automatically, which command CI
   uses, whether only a narrow subset runs, and whether failures are visible.
6. **Sample real tests.** Read a representative few—not every test file—across
   the relevant levels and risk areas. Assess behavior assertions, seams,
   mocks, isolation, readability, speed, flakiness, and maintainability.
7. **Identify risk.** Find important behavior and change paths: domain rules,
   user journeys, public interfaces, persistence, permissions, destructive
   operations, external integrations, error handling, and high-churn areas.
   Use history when available; if it is unavailable, say so.
8. **Assess health qualitatively.** Use one of: **No safety net**,
   **Foothold**, **Partial safety net**, **Reliable safety net**, or
   **Strong enough**. Base the state on executability, risk coverage, test
   quality, reliability, test-level fit, architectural testability, and change
   protection—not on a numeric score.
9. **Choose exactly one pass.** Compare candidate improvements by risk reduced,
   confidence gained, implementation effort, maintenance cost, architectural
   prerequisites, and feedback speed. Select the smallest high-value pass:
   test-first, characterization-first, architecture-first with a minimal seam,
   reliability/stability, CI/infrastructure, or no work for now. Explain why it
   wins over obvious alternatives and define concrete completion criteria.
10. **Stop.** Keep later ideas to at most three brief follow-ups. Do not add
    tests solely to inflate metrics, introduce a second framework without a
    concrete reason, favor E2E merely because it is realistic, or favor unit
    tests merely because they are fast.

For detailed guidance, load only what is needed:

- [Maturity and evidence](references/assessment-model.md)
- [Prioritization and pass selection](references/prioritization.md)
- [Test quality and test-level fit](references/test-quality.md)
- [Ecosystem detection](references/ecosystem-detection.md)
- [Final report format](references/report-format.md)

## Decision rules

Use repository evidence to choose among these common cases:

- **A meaningful seam exists:** test through it; do not refactor for testability
  merely because another design would be easier to test.
- **Behavior is poorly understood:** characterize important current behavior
  before changing it. Do not silently replace undocumented behavior with an
  imagined ideal.
- **Setup requires excessive mocking or invasive manipulation:** identify the
  one dependency or boundary that blocks useful observation and expose the
  smallest seam there. Avoid broad dependency-injection, repository-pattern,
  or architecture migrations.
- **No testing infrastructure exists:** establish only a minimum foothold using
  the ecosystem's natural tool, one clear command, and one meaningful
  behavioral test. Stop after verifying it runs.
- **The suite is flaky, unreliable, or painfully slow:** restore trust in the
  highest-value feedback before increasing suite size.
- **Testing is already strong:** say **Good enough for now** unless a specific
  additional improvement clearly justifies its cost.

Do not equate a passing suite with meaningful protection, a large suite with
maturity, or high coverage with quality. Do not write tests for every source
file merely because it exists, target a coverage number, use snapshots as a
cheap coverage mechanism, or broadly refactor unprotected code just for
idealized testability.

## Implementation mode

If the user asks to implement the recommendation, first confirm the existing
conventions and implement only that one pass. Keep the change behavior-focused
and avoid unrelated cleanup.

After implementation:

1. Run the new or changed tests and verify their output freshly.
2. Run the relevant broader suite and normal lint, typecheck, build, or
   packaging checks when reasonably practical.
3. Confirm the intended behavior is protected at the selected seam. When
   useful, demonstrate that the test fails if the protected behavior is
   intentionally broken; do not claim this if it was not checked.
4. Reassess the affected risk and report the actual commands and results.
5. Recommend at most one next improvement, or say **Good enough for now**.

## Default report

Use the concise structure in [report-format.md](references/report-format.md):

```markdown
# Testing health

**State:** [state]
**Confidence:** [Low | Medium | High]

## What I found
## Biggest current risk
## Recommended pass
## Why this first
## Done when
## Later
```

Include facts, commands, and observed results. If execution was unavailable,
say what was inferred from configuration or CI and lower confidence. Never turn
an unavailable check into a pass.
