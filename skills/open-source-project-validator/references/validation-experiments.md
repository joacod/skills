# Validation Experiments

## Validation principle

Design the smallest public or user-facing test that can produce stronger evidence than more research. Test the most decision-critical unknown, not the easiest metric to collect. Avoid building a production-ready framework when documentation, a walking skeleton, one integration, or a manually supported trial can test the same claim.

A test must specify:

- Primary success objective and dangerous assumption.
- Exact user or strategic-audience profile.
- A 10-20 person relevant sample; assume the user handles recruitment.
- Smallest artifact and concrete workflow.
- Meaningful behavior requested.
- Evidence to collect.
- Time and maintenance budget.
- `pass`, `iterate`, and `kill` thresholds set before launch.

## Match the test to the gate

### User problem and utility

Run the test with relevant users from the target workflow. Observe them attempt a real task with a narrow prototype, example repository, CLI, library, or manually supported implementation. Measure completion and comparison with the current method.

### Open-source fit

Test the claimed mechanism. Ask users to inspect, self-host, extend, debug, audit, or integrate the project. Do not assume an open license matters if no one needs source-level control.

### Distinctiveness

Ask qualified users to choose between the project and the best current alternative for a real case. Capture the switching reason, rejected tradeoffs, and whether the wedge changes behavior.

### Artifact and skill signal

Have members of the intended strategic audience inspect the repository and explain what capabilities it proves, what remains unverifiable, and whether the architecture and tradeoffs can be defended. Prefer concrete opportunities or detailed technical assessment over compliments.

### Adoption friction and time to value

Observe relevant users installing or evaluating the smallest artifact and completing the core workflow. Measure time to first value, failed setup, migration burden, integration work, trust objections, and independent completion rather than impressions or raw clicks.

### Maintenance sustainability

Operate a narrow release for a fixed period. Record setup questions, issue types, response time, compatibility work, security concerns, and recurring hours. Extrapolate cautiously from observed work rather than launch-week enthusiasm.

### Strategic opportunity

Make the artifact legible to the intended audience through a strong README, runnable example, architecture explanation, and evidence of use. Track only opportunities that explicitly reference the project and match the success contract.

## Meaningful commitments

Use this rough hierarchy:

1. Repeat production use, organizational reliance, or independent integration.
2. Adoption by another project, external extension, or sustained substantive contribution.
3. Real workflow access, implementation time, security review, or permission for a specific case study.
4. Successful independent setup and completion of the target workflow.
5. Detailed issue, migration attempt, technical review, or referral to a relevant team.
6. Stated intent to try.
7. Star, like, follow, click, or compliment.

For showcase objectives, a concrete interview, collaboration, referral, or detailed assessment from the target audience can outrank broad adoption. State the objective so the evidence is interpreted correctly.

## Default focused test

Within 14-30 days:

1. Choose one user segment, workflow, ecosystem, and success objective.
2. Run the test with 10-20 relevant users or teams; participant recruitment is outside this framework.
3. Produce only the smallest credible artifact: often a README, runnable example, narrow implementation, and documented tradeoffs.
4. Help the first users try it on a real case without hiding setup friction.
5. Ask for the next meaningful behavior: repeat use, integration, issue, contribution, referral, or case-study permission.
6. Record time to first value, failures, current alternative, switching reason, repeat behavior, support burden, and audience response.
7. Update only the gates the test addressed.

Adapt thresholds to the project and objective. A reasonable early utility test might pass when several qualified users independently complete the workflow and at least two repeat, integrate, or request continued use; iterate when users expose the same problem but fail for a repairable setup, scope, or trust reason; and kill or pivot when relevant users consistently prefer an adequate alternative or no one completes the core workflow after well-targeted attempts.

## Invalid tests

Do not use these alone as validation:

- A star target or launch-day ranking.
- General social engagement.
- Friends praising the idea.
- Downloads without verified execution.
- A polished README shown only to non-users.
- Synthetic personas or simulated code review.
- A testimonial requested before successful use.
- One maintainer or influencer mentioning the project without adoption.

Promotion activity is not validation; only decision-relevant user behavior affects the verdict.
