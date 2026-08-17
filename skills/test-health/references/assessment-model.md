# Assessment model

Testing health is a qualitative judgment about how safely a repository can be
changed. Do not collapse it into a score. A repository may have many tests and
still have little protection if the tests are brittle, untrusted, or aimed at
low-risk code.

## Maturity states

Choose the first state that accurately describes the evidence:

### No safety net

There are no meaningful runnable automated tests protecting important
behavior. This includes unused testing dependencies, missing commands, or test
infrastructure that cannot currently run.

### Foothold

A runner and at least some meaningful automated tests exist, but protection is
narrow or difficult to use. The repository has a starting point, not broad
confidence.

### Partial safety net

Useful tests protect meaningful parts of the application, but important risks,
change paths, or system boundaries remain weakly protected.

### Reliable safety net

Important behavior is covered through sensible seams, the relevant checks run
predictably, and developers can reasonably trust the feedback. Some gaps may
remain without undermining normal changes.

### Strong enough

No obvious high-value testing improvement currently justifies its cost. More
tests may still be useful later, but expansion would mainly serve testing
activity rather than change safety.

## Seven dimensions

Assess each dimension with concrete evidence, but keep the report focused on
the biggest current risk.

1. **Executability** — Can developers find and run the relevant commands? Are
   dependencies and configuration present? Do useful subsets exist? Does CI run
   them? Do they pass now?
2. **Risk coverage** — Are important business rules, user journeys, public
   interfaces, persistence, authorization, payments, destructive operations,
   integrations, transformations, and error paths protected?
3. **Test quality** — Do sampled tests observe behavior through a stable seam,
   assert meaningful outcomes, and survive reasonable refactoring? Do they
   avoid duplicating production logic and excessive implementation coupling?
4. **Reliability** — Are tests isolated and deterministic? Look for arbitrary
   sleeps, order dependence, shared state, uncontrolled networks, time/random
   assumptions, broad fixtures, and intermittent failures.
5. **Test-level fit** — Is each behavior tested at a level that balances speed,
   fidelity, maintenance, and debugging usefulness? Do not impose a universal
   unit/integration/E2E ratio.
6. **Architectural testability** — Can important behavior be observed through an
   existing function, application service, route, CLI, rendered UI, repository
   abstraction, or other stable seam? If not, what is the smallest seam that
   would make it observable?
7. **Change protection** — When history exists, do high-churn or historically
   buggy areas have useful tests? A rarely changed utility is not automatically
   more urgent than a frequently changed, weakly protected path.

## Evidence and confidence

Prefer evidence in this order:

1. Fresh output from the relevant test or reproduction command.
2. Existing targeted tests and their assertions.
3. CI commands and results or configuration.
4. Manifests, runner configuration, source behavior, and history.
5. File presence alone.

Use confidence to describe how complete the assessment is:

- **High** — important commands were run, representative tests were sampled,
  CI and history were inspected where available, and the recommendation is
  directly supported by observed behavior.
- **Medium** — most configuration and code evidence is available, but one
  material source such as execution, history, or CI was unavailable.
- **Low** — the assessment relies mostly on static file evidence, partial
  access, or ambiguous configuration.

A missing capability lowers confidence; it does not justify a made-up result.
For example: “Tests could not be executed in this environment; executability is
inferred from the manifest and CI configuration. Confidence: Medium.”

## Characterization and seams

Use a characterization test when the behavior already exists but its contract is
unclear. Capture a meaningful current outcome through the public seam before
changing it. Do not treat every observed quirk as a desired permanent contract;
identify which behavior is valuable to preserve and document uncertainty.

Use a regression test for understood existing behavior or a known bug. For new
behavior, test-first development can expose the intended contract early, but it
is one technique, not the objective of this skill.

A seam is the place where behavior can be observed or changed without reaching
through the implementation: an exported function, domain/application service,
HTTP route, CLI command, repository interface, rendered UI behavior, or system
boundary. Prefer the narrowest seam that still represents what matters. If a
test needs private methods, internal call counts, or a large graph of mocks,
question the seam before adding more test doubles.

If the architecture genuinely prevents meaningful observation, recommend one
minimal adjustment—such as passing one external dependency into an existing
function or extracting one stable application operation. Do not turn the
assessment into a broad architecture migration.

## Stopping rule

Stop when the selected slice has:

- one clear primary risk or behavior;
- one appropriate main seam and test level;
- the supporting setup and related scenarios needed to make its signal
  trustworthy;
- a bounded implementation scope that does not cross into an independent
  risk;
- a reliable verification command;
- concrete completion criteria; and
- enough evidence to explain why it is more valuable than the alternatives.

Do not stop merely because the first test passes if a closely related outcome
is needed to close the same risk. Conversely, do not continue to enumerate gaps
after the slice is trustworthy and marginal value becomes low. “Good enough for
now” is a valid outcome.
