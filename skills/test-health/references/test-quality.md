# Test quality

Sample enough real tests to understand the repository's testing habits. Judge
whether the tests make changes safer, not whether they look sophisticated.

## Behavior and implementation

Prefer tests that state what a caller or user can observe: a returned result,
state transition, persisted outcome, emitted event, response, error, rendered
interaction, or CLI effect. A useful test can often survive a substantial
internal refactor.

Warning signs include private-method tests, assertions on internal call counts
or ordering, reaching around a public interface to inspect storage, and test
names that describe implementation mechanics rather than behavior. A test can
legitimately assert a collaborator interaction when that interaction is itself
the contract at an external boundary; do not apply the rule mechanically.

Avoid tautological assertions that recompute the production algorithm. Expected
values should come from an independent example, domain rule, fixture, contract,
or known outcome.

## Mocks and test doubles

Use doubles deliberately at system seams such as external services, time,
randomness, filesystem access, or a database when a real test database is not
appropriate. Prefer real in-process collaborators for behavior that belongs to
the application.

Excessive mocking can make a test pass while the integration is broken. It can
also freeze internal structure and make refactoring expensive. If a test needs
to mock most of the application, reconsider the test level or introduce one
small seam at the actual external dependency. Fakes and in-memory adapters can
be useful when they preserve the relevant contract; they are not automatically
better than a test database or a real boundary.

## Assertions and readability

A good test has a clear scenario, a name that describes the behavior, focused
setup, and assertions on meaningful outcomes. Keep the expected result visible
and independent. Multiple assertions are appropriate when they describe one
coherent outcome; split unrelated behaviors.

Prefer ordinary test code that a maintainer can read over elaborate fixture
abstractions. Shared helpers should remove genuine repetition without hiding
important setup. Avoid a test DSL whose indirection makes the scenario harder
to understand than the production code.

## Isolation and reliability

Check for:

- shared mutable state or order-dependent setup;
- fixed ports, global environment variables, or leaked files;
- arbitrary sleeps and fragile timing assumptions;
- current time, random IDs, locale, timezone, or platform dependence;
- live network calls or services that are not controlled by the test;
- broad fixtures that make unrelated changes affect the test; and
- retries that hide real failures instead of removing their cause.

A flaky critical test is negative value: it trains developers to ignore the
signal. Identify and stabilize the highest-value failure before adding more
coverage. Record observed intermittent behavior rather than labeling a test
flaky from suspicion alone.

## Test-level fit

Choose the cheapest level that still observes the risk with useful fidelity:

- **Unit-like:** fast and focused for pure rules and transformations;
- **integration/contract:** appropriate for application wiring, persistence,
  serialization, permissions, queues, and external contracts;
- **system/browser:** appropriate for a small number of critical user journeys
  whose risk is in the rendered or deployed interaction.

Do not enforce a universal ratio. Too much browser coverage can be slow and
fragile; too much isolated testing can miss wiring and boundary failures. The
right level is the one that gives trustworthy evidence for the specific risk.

## Snapshots

Use snapshots only when the whole captured output is a meaningful, reviewed
contract and a snapshot diff is easy to interpret. Prefer explicit assertions
for important behavior. Do not add snapshots merely because they are quick or
because they increase a coverage report.

## Speed and maintenance

Consider local runtime, setup cost, failure diagnosis, and how often the test
runs. A slower test can be the right choice for a high-fidelity boundary, but
its cost should be visible and justified. A fast test that does not exercise the
real risk is not a good bargain.

Review whether test data and setup communicate domain intent, whether failures
point to the broken behavior, and whether the test is likely to survive normal
refactoring. Favor a small number of strong tests over a large number of change
detectors.
