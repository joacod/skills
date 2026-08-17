# Ecosystem detection

Use this guide to recognize existing conventions, not to prescribe a
migration. Repository-local configuration, scripts, CI, lockfiles, and sampled
tests take precedence over defaults in this document.

## General precedence

Inspect in this order:

1. repository instructions and documented commands;
2. package/build manifests and lockfiles;
3. test configuration and actual test file conventions;
4. CI commands and recent passing output;
5. framework defaults.

A dependency or config file is evidence of intent, not proof that a command
works. Prefer the command already used by the repository, including workspace
or environment qualifiers. If no command is executable in the current
harness, report that limitation.

## JavaScript and TypeScript

**Signals:** `package.json`, lockfiles for npm/yarn/pnpm/bun, `.js`, `.jsx`,
`.mjs`, `.cjs`, `.ts`, or `.tsx` files, and configs such as
`jest.config.*`, `vitest.config.*`, `mocha.*`, `playwright.config.*`, or
`cypress.config.*`.

**Common commands:** `npm test`, `npm run test:<name>`, `pnpm test`,
`yarn test`, `bun test`, or the exact script in `package.json`. Direct runner
commands may be useful only when the repository already uses them.

**Established frameworks:** Jest, Vitest, Mocha, AVA, Tap, Playwright, and
Cypress. Testing Library packages usually provide interaction helpers, not the
runner itself.

**Conventions:** `*.test.*`, `*.spec.*`, `__tests__/`, and directories named
`unit`, `integration`, or `e2e` are common. Reuse the existing module system,
transpilation, environment, fixtures, and setup files.

## React and frontend applications

**Signals:** React dependencies, `.jsx`/`.tsx`, frontend build configuration,
component test setup, browser-runner configuration, or a `src`/`app` UI tree.

**Common levels:** component or interaction tests through rendered behavior,
route or application integration tests, and a small number of browser tests
for critical journeys. Use the repository's existing DOM environment and
selectors.

**Frameworks:** Testing Library with the repository's runner, Vitest or Jest,
Playwright, Cypress, and occasionally framework-specific tools. Do not add a
browser stack merely because the project has a UI.

**Risks to sample:** form submission, navigation, loading/error states,
permissions, data fetching, accessibility-relevant interactions, and
serialization or API seams. Prefer user-visible outcomes over component
internals.

## Node.js

**Signals:** `package.json` with a server entrypoint, Node runtime fields,
server framework dependencies, CLI definitions, or backend source outside a
browser app.

**Common levels:** fast tests for domain rules, integration tests for routes,
persistence, queues, and serialization, and contract tests for external
interfaces. Use boundary doubles for live services when a real local service
is not the repository convention.

**Commands/frameworks:** follow the package scripts and existing Jest, Vitest,
Mocha, Tap, or native runner convention. Verify environment variables, ports,
and cleanup before executing tests.

## Python

**Signals:** `pyproject.toml`, `pytest.ini`, `tox.ini`, `noxfile.py`,
`setup.cfg`, `requirements*.txt`, `Pipfile`, `.py` files, and `tests/`.

**Common commands:** `pytest`, `python -m pytest`, `tox`, `nox`, or a documented
wrapper. The standard library's `unittest` may be used directly when tests and
commands show that convention.

**Frameworks/conventions:** pytest, unittest, hypothesis, and behave. Common
names are `test_*.py`, `*_test.py`, and classes or functions beginning with
`test`.

Check fixture scope, database cleanup, environment isolation, and plugin
configuration before judging reliability.

## Go

**Signals:** `go.mod`, `go.sum`, `go.work`, `.go` files, and `*_test.go`.

**Common command:** `go test ./...`; targeted packages or `-run` filters when
already documented. The standard `testing` package is the default. Testify,
GoMock, or other libraries should be treated as established only when imports,
modules, or configuration show them.

**Conventions:** tests sit beside packages in `*_test.go`; integration tests
may use build tags, separate packages, or explicit directories. Check cleanup,
parallel tests, shared fixtures, and external service setup.

## Java and Kotlin

**Signals:** `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle*`,
`src/test/java`, `src/test/kotlin`, `.java`, or `.kt` files.

**Common commands:** `mvn test`, `./gradlew test`, or a repository-specific
module/task command. Common frameworks are JUnit, TestNG, Kotest, and Spock.

**Conventions:** test sources mirror production packages. Inspect Maven or
Gradle test task configuration, profiles, tags, test containers, and parallel
execution before choosing a command.

## .NET

**Signals:** `.sln`, `.csproj`, `.fsproj`, `Directory.Build.*`, `.cs`, `.fs`,
and test projects with names such as `.Tests` or `.Test`.

**Common command:** `dotnet test`, optionally with the solution or project
path already used by CI. Common frameworks are xUnit, NUnit, and MSTest, often
alongside the .NET test SDK.

Use the repository's target framework, fixtures, collection settings, and
coverage or adapter configuration. Do not assume every project in a solution
is a test project.

## Rust

**Signals:** `Cargo.toml`, `Cargo.lock`, `.rs` files, and `tests/`.

**Common command:** `cargo test`, with package, feature, or workspace options
from the manifest or CI. Rust's built-in unit and integration test conventions
are the default; rstest, proptest, and tarpaulin/LLVM coverage tools count as
established only when configured or used.

Unit tests commonly live in modules beside source; black-box integration tests
live under `tests/`. Check feature flags, workspace packages, async runtimes,
and external resources.

## Other ecosystems

Apply the same evidence-first approach to Ruby/Minitest or RSpec,
PHPUnit/Pest, Swift XCTest, and other ecosystems: identify the manifest, the
runner command encoded in the repository, the test layout, and the CI path.
Do not infer a framework solely from a familiar file extension.
