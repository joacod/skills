---
name: refactor-design-patterns
description: Review existing code or architecture and decide whether a specific design pattern would improve it without overengineering. Use this whenever the user is asking whether a pattern is justified, comparing nearby patterns like Strategy vs State or Adapter vs Facade vs Proxy, or refactoring code with recurring branching, growing state logic, hard-to-extend construction, or inconsistent wrappers. Do not use this for broad system design unless the core question is pattern fit, refactoring shape, or whether a simpler non-pattern refactor is better.
---

# Refactor Design Patterns

Use this skill to make design-pattern suggestions practical, incremental, and grounded in the code that already exists.

Start with `references/refactoring-workflow.md`.

Use `references/catalog.md` to route by problem type:
- `references/creational/index.md` for creation and configuration problems
- `references/structural/index.md` for composition, wrapping, interoperability, or simplification problems
- `references/behavioral/index.md` for control flow, runtime behavior, communication, or orchestration problems

Use `references/agent-mappings.md` only when an AI-agent analogy would clarify the recommendation.

## Working style

Anchor every recommendation in the current codebase and the user's actual pain points.

Prefer the smallest useful refactor.
The goal is not to force a pattern into the design; the goal is to decide whether a pattern makes the code easier to change, easier to test, or easier to understand.

When reviewing a feature:
1. Identify the concrete design pressure.
2. Decide whether the problem is mainly creational, structural, or behavioral.
3. Recommend 1 to 3 candidate patterns at most.
4. Explain why the best option fits this code better than nearby alternatives.
5. Call out anti-signals and the simplest valid option if a pattern would be overkill.
6. Suggest an incremental refactor path instead of a rewrite.
7. Tailor the implementation advice to the repository language and conventions when they are known.

## What to look for

Look for recurring signs such as:
- large conditional trees that choose behavior
- tightly coupled modules with unclear boundaries
- difficult object or service construction
- wrapper code repeated across integrations
- state transitions encoded as flags and branching
- scattered side effects and notification logic
- features that are correct but painful to extend

## Output guidance

Prefer a practical structure like this:
- Design problem
- Best pattern choice
- Why it fits here
- Why nearby patterns do not fit as well
- Refactor sketch or steps
- Risks, tradeoffs, and anti-signals

If the user asks for code changes, keep the implementation incremental and idiomatic for the language in the repo.

## Guardrails

Do not recommend a pattern only because the terminology sounds familiar.

Do not abstract early when:
- there is only one stable behavior
- the variation is speculative
- the new layer would hide simple code behind ceremony
- the existing problem can be solved with a small extraction or rename

If no pattern is warranted, say so clearly and recommend the simpler refactor.
