# Chain of Responsibility

## Category

Behavioral

## Intent

Pass a request through a sequence of handlers until one handles it or the chain completes.

## Problem It Solves

Use this pattern when request handling should be decoupled into ordered checks or handlers rather than one large conditional block.

## Signals

- request processing has a natural pipeline
- each step may handle, modify, or reject the request
- new rules should be insertable without editing a central conditional

## Anti-Signals

- the order is trivial and fixed in one place
- every request always needs every step
- a simple loop of functions already captures the design clearly

## Structure

- handler interface
- concrete handlers
- next handler link or chain container

## Refactoring Clues

- long validation or routing chains expressed as nested conditionals
- repeated pre-check logic before real work begins

## Incremental Adoption

- extract each decision block into a handler
- preserve current ordering
- stop once the chain is easier to change than the old conditional

## Tradeoffs

### Pros

- simplifies insertion and reordering of rules
- isolates handling logic
- supports early exit naturally

### Cons

- control flow becomes less obvious
- debugging can require tracing the full chain
- can be overkill for short fixed pipelines

## Nearby Patterns

- Strategy
- Command
- Mediator

## AI-Agent Analogy

Run a task through planner, policy, executor, and validator steps until one resolves or rejects it.

## Language Notes

Often a list of handlers or middleware functions is simpler than explicit linked objects.
