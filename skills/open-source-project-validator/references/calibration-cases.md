# Calibration Cases

Use these fixtures only to test or recalibrate the skill. They test reasoning behavior, not whether the model reproduces one exact verdict. They are not market facts and must never be cited in a live evaluation.

## Case 1: Open-source webhook infrastructure

### Input

A TypeScript library helps teams receive, verify, replay, and debug webhooks locally and in production. The creator wants a recognizable project that demonstrates infrastructure engineering and could later lead to consulting, employment, or a hosted product. There is no current willingness-to-pay evidence.

### Expected reasoning behavior

- Evaluate open-source utility separately from immediate revenue potential.
- Research current webhook tools, libraries, hosted products, framework integrations, and local-development workflows.
- Test one narrow integration and real webhook workflow before recommending a broad framework.
- Treat documentation, examples, types, tests, local setup, reliability, and explainable architecture as credibility surfaces.
- Test with relevant teams using real installation and repeat use rather than asking only for feedback or stars; assume the user handles recruitment.
- Keep consulting, employment, and hosting as optionality until attributable evidence appears.

### Acceptable verdict range

`TEST` or `PIVOT` is calibrated with only the supplied input. `PURSUE` requires stronger evidence of a meaningful gap, usable artifact, and bounded maintenance. Lack of immediate revenue potential must not force `DROP` under the open-source objective.

## Case 2: Polished clone seeking stars

### Input

A creator plans to rebuild a popular task manager with a modern stack and polished README. Success is defined as 1,000 stars and something attractive to show employers. No target user need or technical distinction is identified.

### Expected reasoning behavior

- Treat the star target as attention, not adoption or proof of skill.
- Ask what capability the artifact demonstrates to which employers.
- Identify the lack of standalone utility and distinctiveness.
- Prefer a narrower technically meaningful project or explicit learning objective over polishing a clone.

### Acceptable verdict range

`PIVOT` or `DROP` is calibrated. `TEST` is defensible only for a sharply bounded showcase hypothesis with a relevant audience and low opportunity cost.

## Case 3: Useful project with unsustainable support

### Input

A solo maintainer has a self-hosted deployment tool used by several teams, but every platform version creates breakage, users expect urgent support, and security reports require ongoing response. The creator has two hours per week and primarily wants career credibility.

### Expected reasoning behavior

- Recognize real adoption while rating maintenance sustainability separately.
- Measure support, compatibility, and security burden rather than recommending more growth.
- Consider narrowing supported platforms, transferring stewardship, documenting maintenance status, or parking new features.
- Evaluate whether existing usage and stewardship already provide sufficient career evidence.

### Acceptable verdict range

`PIVOT`, `PARK`, or a tightly constrained `PURSUE` can be calibrated. More stars or users are not automatically desirable.

## Case 4: Strong portfolio artifact with little adoption

### Input

A developer created a database internals visualization tool used mainly in technical demos. Few people need it in production, but experienced database engineers praise its correctness and it has directly produced two relevant interviews.

### Expected reasoning behavior

- Distinguish weak production adoption from successful showcase and opportunity outcomes.
- Attribute interviews only when evidence connects them to the project.
- Avoid forcing a hosted product or broad community strategy.
- Judge whether modest maintenance preserves the artifact's value.

### Acceptable verdict range

`PURSUE` or `PARK` can be calibrated depending on maintenance cost and whether the success contract has already been met.

## Calibration failure signals

Recalibrate if the skill:

- Treats stars, downloads, forks, or launch engagement as sufficient validation.
- Rejects every project without immediate monetization.
- Calls developer experience or open source an automatic moat.
- Recommends polishing a full repository before testing user utility.
- Ignores support, compatibility, security, governance, or abandonment burden.
- Invents production users, contributors, testimonials, opportunities, or future revenue.
- Produces launch or promotion advice instead of an evidence-producing test.
