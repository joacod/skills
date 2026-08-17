# DX quality checklist

Use this gate after an implementation and as a compact audit completeness check.
Skip items that do not apply to the repository, and say why.

## First contribution loop

- [ ] The path from clone to a small validated change is explicit.
- [ ] Prerequisites, runtime, package manager, configuration, and local services are clear.
- [ ] The first successful run has an observable success signal.
- [ ] The smallest useful change has a focused validation command.
- [ ] No step is merely documented when it could safely be removed.

## Discoverability and command ergonomics

- [ ] Common tasks have one obvious supported path.
- [ ] Names, defaults, working directories, and scope are understandable.
- [ ] Targeted and broader checks are both available when relevant.
- [ ] Advanced options have escape hatches without burdening the common case.
- [ ] Duplicate, stale, or unsupported entrypoints are removed or clearly retired.

## Setup and reproducibility

- [ ] Dependencies and important runtime assumptions are explicit.
- [ ] Configuration separates required values from optional values and uses safe examples.
- [ ] Lockfiles or ecosystem-equivalent reproducibility mechanisms are respected.
- [ ] Local services, seed data, generated files, and reset/recovery paths are discoverable.
- [ ] Any environment mechanism added solves an observed problem and has an owner.

## Inner loop and feedback

- [ ] The relevant workflow was rerun after the change when safe.
- [ ] Focused feedback is not replaced by an unnecessarily broad universal check.
- [ ] Failures explain what happened, why, where, and what to try next.
- [ ] Logs and diagnostics retain useful context without burying the next action.
- [ ] Flaky or slow checks are reported honestly; retries do not hide failures.

## Validation and local/CI parity

- [ ] The repository's real lint, format, type, test, build, and generation gates were identified.
- [ ] Developers can reproduce important CI checks locally, or the exception is explicit.
- [ ] Local and CI tasks share underlying implementations where practical.
- [ ] Verification results are labeled passed, failed, skipped, unavailable, or not applicable.
- [ ] No timing, success claim, or behavior is reported without evidence.

## Cognitive load and documentation

- [ ] The change reduces concepts, choices, synchronization, or context switching.
- [ ] Documentation matches commands, paths, examples, and current behavior.
- [ ] Tutorials, how-to guidance, reference, and explanation are separated only when useful.
- [ ] Unusual conventions and constraints are discoverable.
- [ ] Agent-specific guidance is additive and does not make human use harder.

## Maintenance and scope

- [ ] Every new dependency, wrapper, hook, service, or configuration layer has a concrete rent-paying reason.
- [ ] The existing ecosystem and intentional tradeoffs were preserved.
- [ ] The change stays focused on developer friction rather than general code quality.
- [ ] Cleanup removed temporary artifacts and complexity introduced during the work.
- [ ] Remaining risks, assumptions, and deferred friction are stated with confidence and evidence method.
