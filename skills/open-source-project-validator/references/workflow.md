# Investigation Workflow

## 1. Choose the mode and depth

### Evaluate

Use for one explicit project. Run all seven decision gates and return one verdict against the primary success objective.

### Compare

Use for two to five supplied projects. Normalize each against the same success contract, screen all projects, deepen only the leading one or two, and recommend one allocation of effort.

### Explore

Use when the user supplies capabilities, an ecosystem, a problem, or a desired reputation signal but no clear project. Generate at most four materially different candidates, screen them, and deepen the best one or two. Permit the conclusion that none deserves pursuit.

### Update

Use after new usage, issues, contributions, integrations, mentions, case studies, opportunities, maintenance experience, or ecosystem changes. Preserve unaffected conclusions and show changed gates as `previous -> current`.

Use triage depth for a preliminary screen, standard depth for the normal decision card, and deep research only when requested or when licensing, security, ecosystem structure, governance, or maintenance risk could reverse the verdict.

## 2. Define the success contract

Choose one primary objective. Treat other objectives as secondary benefits rather than allowing them to blur the decision.

| Objective | What success means |
| --- | --- |
| Adoption | Relevant users install, complete a real workflow, return, or integrate the project |
| Showcase | The artifact credibly demonstrates capabilities to a defined technical audience |
| Community | Users contribute knowledge, issues, extensions, code, or stewardship |
| Strategic opportunity | The project produces attributable relationships, interviews, contracts, partnerships, or influence |
| Learning | The creator gains a named capability within a bounded time and scope |
| Commercial option | Adoption exposes a plausible support, service, hosted, enterprise, or licensing path to evaluate separately |

Record:

- Primary objective and strategic audience.
- Observable evidence that would count.
- Time horizon.
- Maximum build and recurring maintenance budget.
- Continue, expand, and stop conditions.

If the user supplies a target such as 500 stars, preserve it but identify what it proxies. Stars can measure attention; they do not by themselves establish adoption, code quality, reliance, or opportunity value.

## 3. Normalize and frame the project

Extract the target user, trigger or workflow, current alternative, utility, reason for open source, ecosystem, creator capabilities, skills to demonstrate, strategic audience, evidence, dependencies, and constraints.

Create one sentence:

> For **[specific users]** handling **[trigger or workflow]**, the project replaces or improves **[current alternative]** by delivering **[concrete utility]**; open source matters because **[specific mechanism]**, and success means **[observable behavior]** from **[target audience]** within **[time and maintenance budget]**.

If the utility, open-source mechanism, or success evidence remains vague, narrow the project before expanding features.

## 4. Investigate by decision value

Prioritize:

1. Does a specific user receive standalone value?
2. Why does open source improve the outcome, user control, or collaboration model?
3. What direct, open-source, commercial, internal, or DIY alternatives already exist?
4. Can a relevant user understand, install, and reach the first useful outcome without disproportionate friction?
5. Does the artifact expose the capabilities the creator wants recognized?
6. Can the creator sustain compatibility, support, security, and governance demands?
7. What concrete opportunity could follow if adoption occurs, without assuming it will?

Stop researching when evidence supports the gates, a fatal flaw is established, or the remaining uncertainty requires real usage.

## 5. Design stronger positions

Create alternatives only to repair `WEAK` or `UNKNOWN` gates. Change no more than two of:

- Target user or strategic audience
- Trigger or workflow
- Scope or abstraction level
- Integration or ecosystem
- Setup or adoption model
- Open-core boundary
- Support or governance promise
- Primary success objective

Useful repairs include narrowing to one painful integration, shipping a reference implementation instead of a framework, reducing setup or migration burden, reducing compatibility promises, or changing a showcase project into a real utility for a small user group.

Reject cosmetic repairs such as adding AI, polishing branding, accumulating examples without testing use, or changing license without a user or stewardship reason.

## 6. Judge and update

Assign every gate a signal and concise rationale, identify fatal flaws, choose the best position, select a verdict and confidence, and design a test for the highest-impact unknown.

On updates, distinguish attention from use, first use from repeat use, usage from reliance, issue volume from healthy contribution, and opportunities caused by the project from opportunities merely reported alongside it.

When the primary success contract is already satisfied, do not manufacture a growth goal. Compare the cost of preserving the asset with parking it, and evaluate adoption, community, or commercial expansion only as a separate objective the user actually wants.
