---
name: dx-first
description: >
  Audit, improve, or guard developer experience (DX/DevEx) across any software
  repository or project type. Use this whenever a user asks about repository
  onboarding, development setup, local development, developer tooling,
  build/test feedback, task ergonomics, confusing commands, CI/local workflow
  friction, codebase discoverability, reproducible environments, development
  workflows, or repository usability, even when they do not use the term DX.
---

# DX First

Treat the development experience as a product surface of the repository. Optimize
for three outcomes:

1. **Reduce cognitive load** — make the next useful action findable and the
   common path understandable.
2. **Shorten feedback loops** — give developers fast, trustworthy signals at the
   smallest useful scope.
3. **Protect flow** — remove waiting, context switching, avoidable choices, and
   surprising recovery work.

This is a human-developer experience skill. Properties that help coding agents
are useful when they also make the repository clearer and safer for people.

## Select a mode

- **DX Audit** — inspect and test the repository, then report prioritized
  friction. Remain read-only except for safe, ignored artifacts needed for
  testing.
- **DX Improve** — perform a focused audit, implement the smallest coherent set
  of fixes, update affected documentation, and rerun the journeys.
- **DX Review / Guard** — evaluate a feature, plan, pull request, refactor, or
  tooling change for workflow regressions. Do not edit unless implementation
  was requested.

If the request is ambiguous, use Audit for questions and Improve only when the
user explicitly asks to fix or implement something.

## Operating workflow

Follow this pipeline; do not replace it with a checklist of missing tools:

**inspect → classify → trace → test → find friction → prioritize → improve → verify → simplify**

1. **Inspect.** Read `references/repo-inspection.md`. Map the repository's
   structure, instructions, manifests, runtime and package-manager declarations,
   task entrypoints, tests, CI, documentation, and environment configuration.
   Inspect enough implementation to verify important claims; do not read the
   entire codebase blindly.
2. **Classify.** Identify the repository type, ecosystem, runtime, package
   manager, monorepo boundaries, setup path, development process, validation
   strategy, release shape, and any developer-facing API, CLI, SDK, or tool.
   Evaluate only surfaces that apply.
3. **Trace.** Start with the first contribution loop:
   **clone → setup → run → change → validate**. Then trace relevant daily tasks
   such as a targeted test, full validation, debugging, generated artifacts,
   migrations, CI reproduction, or release preparation.
4. **Test.** Execute supported paths when safe and practical. Prefer the real
   command, help output, invalid-input behavior, targeted check, or setup step
   over assumptions from file presence. Record step counts or timings only when
   actually observed.
5. **Find friction.** Read `references/friction-catalog.md` as needed. Record
   concrete symptoms, not vague quality judgments. Distinguish **TESTED**
   (executed or observed), **VERIFIED** (confirmed statically), and **INFERRED**
   (reasonable but unexecuted).
6. **Prioritize.** Order work approximately by developer impact × frequency ×
   confidence ÷ implementation and maintenance cost. Fix blockers and repeated
   inner-loop friction before polish. Treat intentional tradeoffs as context,
   not automatic findings.
7. **Improve.** Prefer removal, simplification, clearer existing commands, and
   ecosystem-native mechanisms. Add a dependency, wrapper, task runner, hook,
   container, service, or configuration layer only when it removes evidenced
   friction and its maintenance cost is justified.
8. **Verify.** Rerun the affected journey and relevant repository checks. Compare
   the observed path before and after; do not claim an improvement from a file
   edit alone.
9. **Simplify.** Remove stale instructions, duplicate paths, temporary helpers,
   and complexity introduced during the fix. Read
   `references/quality-checklist.md` before finishing.

## Hard rules

- No vibes-only findings. Every meaningful criticism cites a repository artifact,
  command, output, or observed journey.
- Use one obvious recommended path for frequent tasks, with sensible defaults
  and an escape hatch for legitimate advanced cases. Do not create choice
  overload or literal command names when the ecosystem has a better convention.
- Documentation should explain or route around necessary complexity; it should
  not be the excuse for preserving unnecessary steps.
- Prefer local validation that shares the same underlying tasks as CI. Keep the
  smallest useful check available for a small change and a broader confidence
  path for integration.
- Make failures answer: **what failed, why, where, and what to do next**.
- Treat secrets and production/shared-environment effects as out of bounds for
  ordinary audits. Do not deploy, publish, push, run destructive migrations,
  delete data, or expose credentials merely to test DX.
- Do not turn this into a general security, architecture, performance, product,
  or DevOps maturity audit. Consider those only when they directly create
  developer friction.
- Do not require Docker, dev containers, Make, pre-commit hooks, generators,
  agent maps, or any other popular mechanism without repository-specific
  evidence that it is the simplest net improvement.
- Do not use a numeric DX score unless the user asks for one. A prioritized,
  evidence-backed friction inventory is more useful than false precision.
- `dx-first` works independently. If `readme-first` is available, compose with
  it for a deep main-README rewrite rather than copying its methodology here.

## Finding format

For each material finding, include:

- **Journey or task**
- **Observed friction**
- **Evidence** and file, symbol, command, or output reference
- **Developer impact** and affected frequency or scope
- **Recommended improvement**
- **Implementation effort**
- **Confidence**
- **Method:** TESTED, VERIFIED, or INFERRED

For an audit, report a short **DX summary**, the actual **critical path**,
**highest-impact findings** in priority order, **what already works well**, and
the **suggested order of improvements**. For Improve, also state what changed,
what journey was rerun, and what complexity was removed or deliberately kept.
For Review / Guard, answer whether the proposed change adds setup, commands,
waiting, cognitive load, manual steps, local/CI divergence, or harder failures,
and identify the paved path it preserves or improves.

Read the supporting references progressively; they are the detailed guidance,
not prerequisites to use the basic workflow:

- [DX principles](references/dx-principles.md) — conceptual foundation and
  decision rules.
- [Repository inspection](references/repo-inspection.md) — ecosystem-neutral
  reconnaissance and safe journey testing.
- [Friction catalog](references/friction-catalog.md) — symptoms and remedy
  choices across repository surfaces.
- [Quality checklist](references/quality-checklist.md) — final implementation
  and audit gate.
