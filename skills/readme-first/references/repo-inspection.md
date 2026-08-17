# Repository Inspection

Inspect enough of the repository to document the user experience accurately;
do not read the implementation exhaustively. The main README should reflect
what a visitor can actually install, run, and use.

## Inspect in a focused order

Start at the repository root and current `README.md`. Confirm which README the
hosting platform and repository convention treat as the main user-facing entry
point; normally use the root file and do not substitute a profile, locale, or
arbitrary documentation README. Then inspect the smallest set of relevant
sources:

1. **Project identity and package metadata** — `package.json`, `pyproject.toml`,
   `Cargo.toml`, `go.mod`, `pom.xml`, `*.csproj`, gemspecs, or equivalent
   manifests; lockfiles; repository metadata; and the license file.
2. **Supported actions** — package-manager scripts, `Makefile`, `Justfile`, task
   runner configuration, Dockerfiles and Compose files, release/build config,
   CLI definitions, application entrypoints, public exports, and runnable
   examples.
3. **User setup** — `.env.example` or equivalent, required services, runtime
   versions, installation instructions, seed/demo data, ports, and local
   development configuration.
4. **Evidence of intended usage** — examples, tests that exercise the public
   interface, fixtures, docs, tutorials, CI workflows, and screenshots or
   recordings already in the repository.
5. **Project support** — `CONTRIBUTING.md`, `SECURITY.md`, support links, issue
   templates, release notes, and other canonical documents that the README may
   link to.

Use targeted search (`git grep`, focused `find`, or equivalent) to answer a
question. Do not inspect irrelevant internal modules simply to fill a section.
Treat generated files, vendored dependencies, build output, secrets, and
private configuration as non-sources unless they directly establish a public
fact.

## Classify before writing

Identify:

- project type: library/package, CLI, application, service/API, framework,
  developer tool, GitHub Action, plugin, template/starter, Agent Skill, or
  monorepo;
- primary user and the problem or workflow that brings them here;
- main user-facing capability and the first useful result;
- supported runtime, package manager, operating system, and prerequisites;
- normal happy path from a clean checkout or package install;
- important user-visible capabilities, with implementation details kept
  separate;
- relevant examples, visuals, supporting docs, license, and contribution path.

For a monorepo, identify the product or package the main README represents and
link to package-specific documentation rather than blending every workspace
into one generic introduction.

## Establish repository truth

When sources disagree, prefer evidence in roughly this order:

1. executable configuration and actual source behavior;
2. manifests, task runners, build configuration, and CLI definitions;
3. examples and tests;
4. CI workflows;
5. current supporting documentation;
6. the current README;
7. inference.

Use the README to discover terminology and intent, but never preserve a claim
only because it is already written there. Check that:

- every documented command exists in a script, task runner, CLI, or supported
  tool invocation;
- package names, imports, exports, flags, paths, configuration keys, runtime
  versions, ports, and filenames exist;
- links and images point to real repository files or verified external targets;
- listed features are observable and current;
- badges describe a real, useful signal and point to a meaningful URL;
- license and contribution statements match files actually present.

If a fact cannot be established confidently, omit it. If it is important to
explain a limitation, label it as unresolved and state what evidence is still
needed. Do not turn a guess into a prerequisite or compatibility promise.

## Find and validate the happy path

Choose one recommended path, not a catalog of equivalent choices:

1. determine the project's normal install or startup mechanism from its manifest,
   scripts, task runner, or documented entrypoint;
2. find the smallest representative invocation or code example in current
   examples, tests, exports, or CLI definitions;
3. cross-check prerequisites and required configuration;
4. run the primary local path when it is safe, practical, and self-contained;
5. record the expected result or next action only when repository evidence
   supports it.

Static verification is acceptable when execution needs unavailable services,
credentials, paid APIs, deployment, publishing, production access, migrations,
or destructive operations. In that case, say that the path was statically
verified; never imply it was executed. Do not run commands that send messages,
publish artifacts, alter shared environments, deploy, migrate, or expose
secrets merely to validate README prose.

## Handle conflicts and missing evidence

When evidence conflicts:

- prefer the higher-ranked source;
- inspect the conflicting path or command directly;
- update the README to the confirmed behavior;
- preserve a limitation only if it is confirmed and useful to a new user.

When evidence is missing:

- do not invent a command, URL, screenshot, demo, badge, feature, dependency,
  environment variable, or version;
- use a narrow statement that can be supported, or leave the section out;
- ask the user only when the missing decision changes the README's scope or
  safe happy path.

Keep a short internal fact list while writing: confirmed facts, safe inferences,
and unresolved questions. Only confirmed facts and clearly labeled limitations
belong in the final README.
