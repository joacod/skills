---
name: refactor-design-patterns
description: Review existing code or architecture and decide whether a specific design pattern would improve it without overengineering. Use this whenever the user is asking whether a pattern is justified, comparing nearby patterns like Strategy vs State or Adapter vs Facade vs Proxy, or refactoring code with recurring branching, growing state logic, hard-to-extend construction, or inconsistent wrappers. Do not use this for broad system design unless the core question is pattern fit, refactoring shape, or whether a simpler non-pattern refactor is better.
---

# Refactor Design Patterns

Use this skill to make design-pattern suggestions practical, incremental, and grounded in the code that already exists.

Start with `references/refactoring-workflow.md`.

If a pattern is warranted or the user requests a pattern comparison, use
`references/catalog.md` to route by problem type:

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
2. Decide whether a pattern is needed. Consider leaving the code as is or using
   a small extraction, rename, or local simplification first.
3. If a pattern adds value, classify the problem and compare at most three
   candidates. Explain why the selected option improves on the simpler approach.
4. Call out tradeoffs and anti-signals, and suggest an incremental path only
   when a change is warranted.
5. Tailor implementation advice to the repository language and conventions.

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
- Does this need a pattern?
- Recommended approach, including no change or a simpler refactor when appropriate
- Pattern comparison, only when useful
- Refactor sketch or steps, if a change is warranted
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
