---
name: safe-pnpm-updater
description: >
  Safely investigate, install, and update dependencies in pnpm-managed JavaScript
  and TypeScript projects through Socket Firewall and release-age checks.
  Use for dependency upgrades, security remediation, dependency installation,
  or pnpm lockfile reviews. Audit-only requests remain read-only. Execution
  requires the configured interactive zsh firewall alias and a positive pnpm
  minimumReleaseAge; npm, Yarn, and Bun projects are unsupported.
---

# Safe pnpm updater

Select the newest stable versions within the requested scope that satisfy
release-age, security, and compatibility checks. Discover the project's stack
and verification commands instead of assuming a framework or application.
Defer candidates that cannot be validated and report the concrete blocker.
Passing tests and a clean audit are evidence, not proof of complete safety.

## Scope and authorization

- Read repository instructions and inspect the working tree before edits.
  Preserve unrelated changes; ask before taking ownership of pre-existing
  dependency-file changes. Capture the starting contents of files this run may
  change so recovery can preserve those changes.
- Determine the package manager from `packageManager`, lockfiles, workspace
  configuration, and CI. Stop on conflicting evidence. For npm, Yarn, or Bun,
  report unsupported execution; do not migrate the project to pnpm.
- An update request covers its requested local dependency changes, subject to
  repository authorization rules. Audit/review requests cover investigation
  only. Installing existing dependencies does not authorize upgrading them.
- Explain candidate groups before editing. Ask about major versions when scope
  is unclear. For an unrestricted "update all" request, consider every direct
  dependency, including majors, but obtain any required confirmation for a
  non-trivial migration. Do not turn an update into a redesign.
- Do not branch, commit, push, create a PR, deploy, publish, send messages, or
  modify remote environments without authorization for those actions. Inspect
  validation scripts for uploads, paid calls, production access, and destructive
  behavior before running them.

## 1. Verify the security boundary

Resolve bundled scripts relative to this skill's installed directory, not a
hardcoded repository path. From the project or workspace root:

```bash
bash "<skill-directory>/scripts/check-prerequisites.sh" "$PWD"
```

The preflight requires the exact interactive zsh alias `sfw --verbose pnpm`,
an executable `sfw`, Socket Firewall runtime confirmation, and a positive
effective `minimumReleaseAge` in minutes. It performs version and configuration
checks, without registry lookups or installation.

If it fails, stop before candidate research, registry queries, dependency edits,
or installation. Report the exact `SAFE_DEPENDENCY_UPDATE_BLOCKED` reason and
state that the update was not attempted. Do not repair global configuration.
If a diagnosed sandbox restriction prevents Socket's localhost listener, request
narrowly scoped permission to rerun the same protected command; continue only
after the preflight passes.

Use the wrapper for every subsequent pnpm command, including project scripts,
registry queries, installs, and audits:

```bash
bash "<skill-directory>/scripts/run-pnpm.sh" <pnpm-arguments...>
```

It rechecks the preflight and expands the alias in interactive zsh. Run at the
same root throughout; use pnpm workspace filters for package-specific work.
Alternatively, set `DEPENDENCY_UPDATE_PROJECT_DIR` to that absolute root.

Never use an unwrapped pnpm binary, npm, npx, Yarn, Bun, or Corepack as a fallback.
Inspect helpers for unwrapped package-manager subprocesses; use their underlying
command through the wrapper or report the check unavailable. Never lower release
age, add a release-age exclusion, use `--trust-lockfile`, disable Socket, or alter
aliases, registries, or global configuration to make an update succeed. Existing
age exclusions do not authorize exempting new candidates.

For JSON output, remove only the identified Socket confirmation line. Preserve
other warnings and reject malformed data instead of silently discarding it.

## 2. Establish the baseline and candidate policy

Read manifests, `pnpm-lock.yaml`, workspace configuration, `.npmrc`, patches,
overrides, lifecycle-script approvals, and CI. Verify that the routed pnpm
version matches the project's toolchain pin and Node satisfies relevant engines
and CI requirements. Treat a toolchain change as a separate reviewed candidate.
Do not print secrets or environment-file contents.

Discover workspace manifests from the current workspace configuration, excluding
installed dependencies and generated output. Account for all direct production,
development, and optional dependencies in scope. Treat peer declarations as
consumer compatibility contracts, not packages to blindly pin. Distinguish
registry packages from workspace links and Git/file/URL sources; do not replace
non-registry sources or invent publication timestamps. Defer their updates until
an appropriate provenance and verification policy is established.

Capture existing install/peer warnings, audit findings, and relevant validation
failures before updates when feasible. Keep reports outside tracked source files.
Investigate registry packages through the wrapper, for example:

```bash
bash "<skill-directory>/scripts/run-pnpm.sh" outdated --format json
bash "<skill-directory>/scripts/run-pnpm.sh" view <package> time --json
bash "<skill-directory>/scripts/run-pnpm.sh" view <package>@<version> engines peerDependencies deprecated --json
bash "<skill-directory>/scripts/run-pnpm.sh" audit --json
```

Use workspace-aware queries when needed. An outdated/audit command may return
useful findings with a non-zero exit; distinguish those from network or registry
failure. An unavailable audit is not a clean audit.

Select stable, non-deprecated compatible releases using trustworthy publication
timestamps. Require both conditions:

```text
publishedAt <= current UTC time - effective minimumReleaseAge
publishedAt <= supplied as-of cutoff, when requested
```

Interpret `as-of YYYY-MM-DD` as the end of that UTC date unless the user supplies
another timezone. Do not invent a historical cutoff or lower configured age.
If an additional minimum age is requested, enforce the stricter age. Reject
missing timestamps; use prereleases only when explicitly requested, with the
same age checks. An outdated result or a latest tag does not establish compliance.

Record current specs, selected versions, timestamps, compatibility evidence,
and deferrals. Preserve dependency sections and the project's range/pinning
style rather than imposing exact versions on every project.

## 3. Review compatibility and existing exceptions

Locate each candidate's use in source, configuration, scripts, and tests.
Review official release notes and migration guides as needed, alongside peers,
engines, exports, and changed behavior. Patch/minor labels do not replace review.
Packages without imports may still power the build or development tools.

Derive update groups from actual relationships: framework/runtime pairs, tightly
coupled plugin families, renderers and adapters, or test runners and environments.
Keep versions aligned only when the upstream ecosystem requires it. For each
group, identify an affected feature and a concrete verification path. Include
native binaries, install scripts, assets/styles, and persisted formats when
relevant. Avoid adding framework-specific rules to unrelated projects.

Reconcile existing exceptions deliberately:

- **Patches:** check their purpose and whether upstream fixes it. Retain or
  recreate a needed minimal patch for the selected release through wrapped pnpm
  commands. Remove one only with evidence and any required authorization;
  verify its mapping and lockfile. Never silently drop or reuse a mismatched patch.
- **Overrides:** trace their resolved paths with wrapped `pnpm why`. Prefer an
  upstream parent update. Change an override only with evidence that the graph
  remains compatible; do not treat old advisory workarounds as permanent fixes.
- **Peer exceptions:** revisit them when the affected packages change. Do not
  widen ranges or add exceptions merely to silence warnings.
- **Lifecycle approvals:** preserve the project's policy. Review newly requested
  scripts and obtain required authorization; do not approve all builds or hide
  necessary script failures.
- **Age exclusions:** preserve unrelated entries. Remove obsolete version-specific
  entries only within scope; do not replace them with exemptions for new candidates.

Research before asking the user to classify unfamiliar packages. If a remaining
gap requires a migration decision, credentials, paid requests, remote writes,
or manual feature validation, name the package, candidate, affected behavior,
and decision needed. Continue independent groups while waiting. An unanswered
question is not approval; defer that candidate with its reason.

## 4. Apply updates in recoverable groups

Apply explicit reviewed versions in small compatibility groups and reconcile
manifests and lockfiles through the wrapper. Avoid blanket `update --latest`,
automatic `audit --fix`, new dependencies, and unrelated lockfile churn.
For install-only requests, use the repository's documented install command;
prefer frozen-lockfile installation when reproducing an existing locked graph.

Review the manifest/lockfile diff, patches, peer warnings, and lifecycle output
after each group. Run affected checks while failures are easy to attribute.
If release age or timestamps are rejected, decline bypasses and choose an older
compliant candidate or defer it.

If installation or validation fails, diagnose before continuing. Restore only
this run's changes to the failed group from the captured baseline, respecting
repository approval requirements for overwrites/removals. Reconcile restored
lockfile and install state through the wrapper. Never reset the whole worktree.
If recovery cannot be verified, report failure and the remaining local state.

For advisories, trace the vulnerable resolved path and fixed range. Prefer a
compatible direct/parent update. Use a narrow override only with verified API
compatibility. Never hide findings through audit exclusions or severity changes.
If no mature compatible fix exists, report the advisory and blocking dependency.

## 5. Verify and report

Verify that the final manifest and lockfile resolve the reviewed versions and
their timestamps meet policy. Inspect unexpected transitive churn. Use a wrapped
`install --frozen-lockfile` to check consistency when appropriate, then run the
current applicable CI gates and focused feature checks through the wrapper.
Discover lint, typecheck, tests, and build commands from this repository rather
than assuming script names. Do not deploy or use production credentials to make
a build pass.

Inspect the final full-graph audit, including development and low-severity
findings; use a production audit where supported to distinguish runtime exposure.
Passing a severity threshold is not zero advisories. Recheck peers, deprecations,
and actual resolved paths. New unexplained warnings remain unresolved evidence.

Provide concrete manual checks for behavior automated tests cannot prove, such
as sign-in, audio playback, native integrations, or GPU rendering. Label checks
as passed, failed, skipped, unavailable, or user-verified; do not describe mocks
as live acceptance. Account for every in-scope direct dependency as updated,
already current under policy, or deferred with a reason.

Report `UPDATED`, `PARTIAL`, `NO_CHANGES`, `BLOCKED`, or `FAILED`, including:

- Firewall alias/runtime evidence, routed pnpm version, effective release age,
  and any as-of cutoff.
- Old/new specs and selected publication times; deferred packages and blockers.
- Files changed, migrations, patch/override decisions, and files intentionally
  untouched.
- Exact verification commands/results, baseline failures versus regressions,
  remaining advisory paths/severities, and install/peer warnings.
- Concrete manual checks, required decisions, or follow-ups.

Use `PARTIAL` when requested candidates remain deferred or required checks are
unavailable. Use `FAILED` for unresolved introduced regressions. Claim zero
known advisories only when the final full-graph audit reports zero. For preflight
failure, include the exact blocker and state that no candidate investigation or
installation occurred.
