# Decision Framework

## Seven decision gates

### 1. User problem and utility

Ask whether a specific user has a real trigger or workflow and whether the project delivers meaningful standalone value over the current alternative.

### 2. Open-source fit

Ask whether source availability materially improves trust, inspectability, extensibility, interoperability, self-hosting, learning, local control, or ecosystem participation. Publishing source is not proof of value.

### 3. Distinctiveness and ecosystem gap

Ask why a user would adopt or contribute instead of using established open-source projects, commercial products, platform features, internal code, generic tools, or doing nothing. Prefer a narrow workflow, integration, technical approach, or stewardship promise over a feature list.

### 4. Artifact and skill signal

Ask whether the repository visibly demonstrates capabilities valued by the intended strategic audience. Consider code quality, tests, types, documentation, examples, local development, release discipline, architecture tradeoffs, security, and evidence of thoughtful maintenance. Match the signal to the desired role or opportunity.

### 5. Adoption friction and time to value

Ask whether a relevant user can understand the project, install or evaluate it, complete the core workflow, and obtain value without disproportionate setup, migration, integration, trust, or organizational change. Judge the product's adoption burden, not how the creator will promote it.

### 6. Maintenance sustainability

Ask whether compatibility, support, triage, releases, documentation, security, governance, moderation, and on-call expectations fit the creator's recurring budget. Evaluate the maintainer experience after initial excitement fades.

### 7. Strategic leverage and optionality

Ask whether credible use can plausibly produce the primary objective: reputation, relationships, career opportunities, community influence, consulting, support, a hosted service, enterprise features, sponsorship, or another future path. Keep potential commercial models provisional until separately validated.

## Signal anchors

| Signal | Meaning |
| --- | --- |
| `STRONG` | Direct, current evidence supports the gate and major risks are bounded |
| `MIXED` | Credible support exists, but material limits or contradictions remain |
| `WEAK` | Evidence points against the gate or a major obstacle is visible |
| `UNKNOWN` | Evidence is insufficient; do not infer a positive or negative result |

Do not assign `STRONG` from a plausible story, polished repository, or large star count alone.

## Fatal flaws

Examples include:

- No identifiable user, workflow, or standalone utility.
- Open source provides no relevant benefit and creates disproportionate support or exposure risk.
- Mature alternatives solve the problem with no credible wedge or learning objective.
- The artifact cannot demonstrate the capabilities the creator wants recognized.
- Adoption requires broad popularity before any user receives value.
- Necessary data, APIs, permissions, trademarks, or licenses cannot plausibly be used.
- Security, compatibility, moderation, or support obligations exceed the maintenance budget.
- The success definition depends on vanity metrics with no path to stronger behavior.
- Validation requires building most of the production system first.

Do not average a fatal flaw into a medium result.

## Verdict rules

### `PURSUE`

Use when critical gates are `STRONG` or bounded `MIXED`, no fatal flaw exists, and evidence supports building or releasing the smallest useful public version. It does not mean building the full roadmap.

### `TEST`

Use when the project is credible but one or two high-impact assumptions can be tested cheaply with a prototype, documentation-first artifact, direct user trial, or narrow integration.

### `PIVOT`

Use when the underlying problem, capability, or ecosystem is useful but the current user, scope, integration, setup model, maintenance promise, or success objective is weak. Name the repaired position.

### `PARK`

Use when the project may become attractive but current timing, creator constraints, ecosystem maturity, or test cost makes pursuit irrational. State the reconsideration trigger.

### `DROP`

Use when a fatal flaw is established, the project is below the creator's opportunity cost, or repeated meaningful tests fail. State the decisive reason directly.

## Confidence

Use high confidence for direct behavior with current, converging evidence; medium for credible but incomplete evidence; and low for mostly inference, weak proxies, or unresolved contradictions. Confidence describes evidentiary support, not enthusiasm.
