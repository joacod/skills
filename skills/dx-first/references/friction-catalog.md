# Friction catalog

Use this catalog to name observable patterns and choose remedies. A signal is
not automatically a finding: confirm its impact, frequency, affected scope,
confidence, and whether it is an intentional tradeoff. Prefer the simplest fix
that removes the friction.

## Discoverability

**Symptoms:** setup or task commands are buried, scripts have opaque names,
multiple documents disagree, CI contains the only usable command, package
boundaries are unclear, or help output omits the next action.

**Prefer:** one front door, one recommended path per frequent task, names that
match ecosystem conventions, links from shallow guidance to deeper reference,
and concise help that exposes defaults and examples. Remove competing paths
before adding an index or wrapper.

## Bootstrap and onboarding

**Symptoms:** a new contributor must guess runtime versions, install undeclared
system tools, copy unexplained configuration, start services manually, or learn
an ordering that setup does not enforce.

**Prefer:** explicit prerequisites, pinned or clearly supported runtimes,
deterministic dependency installation, safe configuration examples, a visible
success signal, and setup that fails early with a next action. Automate repeated
mechanical steps only when the automation is easier to understand and maintain
than the steps it replaces.

## Reproducibility and environment drift

**Symptoms:** works-on-my-machine failures, missing lockfiles or runtime
metadata, local and CI use different dependency resolution, or developers need
machine-specific state with no documented reset.

**Prefer:** explicit dependencies and versions, one supported package manager,
reusable existing environment definitions, clear config contracts, and a
low-cost reset or recreation path. Choose version pinning, ecosystem tooling,
a container, or another mechanism from the observed failure; do not prescribe a
container because one is absent.

## First contribution loop

**Symptoms:** clone-to-change requires archaeology, the first run has no clear
success signal, a small change needs unrelated setup, or validation cannot be
found until review.

**Prefer:** a traced happy path with the smallest useful edit and check. Put
instructions at the point of need, make the expected result visible, and expose
the next safe validation command. Record actual step counts or timings only when
observed.

## Inner loop and iteration speed

**Symptoms:** every edit triggers a broad slow suite, watch/rebuild behavior is
missing where the ecosystem supports it, targeted checks are hidden, generated
artifacts require manual synchronization, or local feedback is flaky.

**Prefer:** focused checks for focused changes, reliable watch or incremental
behavior when it materially helps, clear escalation from targeted to broader
validation, and automation that removes repeated manual work without creating a
new abstraction maze. Investigate flakiness before adding parallelism or more
retries that hide failures.

## Command surface and task ergonomics

**Symptoms:** several wrappers invoke the same operation, names vary between
README, scripts, and CI, defaults are surprising, destructive commands have no
warning, or advanced flags are required for common work.

**Prefer:** the shortest maintainable native path or one thin canonical task
surface, sensible defaults, explicit destructive boundaries, and progressive
disclosure for advanced options. Delete stale aliases and document legitimate
escape hatches rather than exposing every knob during onboarding.

## Tests and validation confidence

**Symptoms:** no targeted test path, the full suite is the only documented
check, tests are unreliable or depend on hidden services, CI checks are not
reproducible, or developers cannot tell what a passing command proves.

**Prefer:** a small behavior-focused check at an observable seam, a trustworthy
broader confidence path, test data and service setup that are discoverable, and
commands whose scope is clear. Improve reliability and diagnostic output before
adding more test categories. Do not demand every quality tool or a blanket
coverage target.

## Local and CI parity

**Symptoms:** CI runs a different task implementation, uses a different runtime
or install mode, validates generated files that local commands do not, or
requires developers to wait for CI to discover a basic failure.

**Prefer:** CI invoking the same canonical local tasks, shared configuration,
explicit exceptions for genuinely hosted checks, and a documented local
reproduction command. Keep hidden CI-only behavior rare and explain why it is
not local.

## Error messages and feedback quality

**Symptoms:** startup fails with a generic stack trace, a missing variable is
reported far from its use, CLI errors omit valid syntax, test output loses the
first cause, or a CI failure says only that a job failed.

**Prefer:** identify the failed operation, likely cause, location or input,
and next action. Preserve diagnostic detail behind a concise summary, include
safe examples or links when stable, and make invalid-input behavior part of
journey testing. Never include secret values in errors or reports.

## Configuration and local services

**Symptoms:** required and optional settings are mixed, examples contain unsafe
or stale values, configuration is read implicitly, or developers must infer
which database, queue, emulator, or credential is needed.

**Prefer:** an explicit contract, safe example values, startup validation,
clear distinction between required and optional settings, local substitutes
when they are already part of the ecosystem, and a reset/seed workflow. Do not
add a service or configuration layer just to imitate production if it increases
local burden without improving a demonstrated path.

## Debuggability and recovery

**Symptoms:** logs lack context, stack traces point to generated code only,
source maps or diagnostics are unavailable, a failure cannot be reproduced at a
smaller scope, or the only recovery is deleting unexplained state.

**Prefer:** actionable diagnostics, stable debug modes, focused reproduction,
visible reset/retry behavior, useful fixtures, and documented recovery. Match
observability to project complexity; a simple project does not need a platform
just to print a helpful error.

## Documentation structure and accuracy

**Symptoms:** the README documents an unsupported command, tutorials mix with
reference, how-to steps omit prerequisites, examples drift, or troubleshooting
is separated from the failure that motivates it.

**Prefer:** keep the front door short, put task guidance near the task, separate
tutorials, how-to guides, reference, and explanation when that distinction
reduces search cost, and verify commands and links. Prefer removing an
unnecessary step to documenting it more carefully. Use `readme-first` for a
comprehensive main-README rewrite when available; `dx-first` still fixes small
README issues that block a wider workflow.

## Cognitive load and context switching

**Symptoms:** developers must remember hidden ordering, synchronize duplicated
configuration, choose between equivalent tools, leave the repository for common
answers, or carry exceptions that automation could safely handle.

**Prefer:** conventional structure, explicit constraints, one default path,
progressive disclosure, local examples, and removal of redundant concepts. Keep
escape hatches visible but out of the critical path. Do not confuse more
abstraction with less cognitive load.

## Monorepos and multi-scope repositories

**Symptoms:** root commands are ambiguous, a package change runs unrelated
work, dependencies cross boundaries unexpectedly, or developers cannot tell
which package owns a command or check.

**Prefer:** a discoverable scope model, root orchestration only where useful,
package-level targeted commands, clear working-directory or filter behavior,
shared validation that delegates to package-native tasks, and documentation of
cross-package prerequisites. Do not duplicate scripts in every package merely
to make names look uniform.

## Change, release, and migration workflows

**Symptoms:** versioning or migrations require tribal knowledge, breaking changes
lack guidance, release commands have no preview or dry-run where appropriate,
or rollback/recovery is unclear.

**Prefer:** the repository's existing release conventions, small reviewable
batches, explicit migration and deprecation steps, safe previews where the
ecosystem supports them, and a recovery path. Expand into release engineering
only when shipping the change is part of the developer journey.

## Human and agent legibility

**Symptoms:** constraints live only in chat or CI, repository navigation is
unclear, validation cannot be invoked from a clean checkout, or agents are
expected to guess commands and scope.

**Prefer:** version-controlled entrypoints, accurate docs, deterministic checks,
clear boundaries, and documented unusual decisions. Add `AGENTS.md`, maps, or
other agent-specific files only when the repository uses agents or evidence
shows that human-readable guidance alone is insufficient. Do not optimize for
agents at the expense of people.

## Tooling accumulation

**Symptoms:** each friction report produces another wrapper, hook, task runner,
container, service, or configuration file; several tools solve the same problem;
maintenance ownership is unclear.

**Prefer:** first remove stale paths, simplify the existing stack, or expose an
existing native command. If addition is justified, state the friction removed,
frequency, owner, maintenance cost, alternatives considered, and how the new
mechanism will be verified. A tool that cannot pay rent should not land.
