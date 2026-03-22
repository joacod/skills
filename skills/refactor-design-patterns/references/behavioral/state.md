# State

## Category

Behavioral

## Intent

Represent states as objects or modules so behavior changes with internal state without large conditionals.

## Problem It Solves

Use State when the same object behaves differently across lifecycle stages and flags or switches are making transitions hard to manage.

## Signals

- behavior depends on lifecycle state
- state transitions are explicit and important
- conditionals over status values keep growing

## Anti-Signals

- there are only one or two trivial states
- behavior differences are small
- a simple enum and switch remains clearer

## Structure

- context
- state interface
- concrete states

## Refactoring Clues

- one class with many branches based on `status`, `mode`, or flags
- invalid transitions are easy to introduce

## Incremental Adoption

- identify the true states and transitions
- move one state's behavior behind a dedicated object or module
- evolve remaining branches only if complexity warrants it

## Decision Notes

- Choose State when lifecycle stages and valid transitions are central to the design problem.
- Prefer Strategy when the variants are interchangeable choices rather than phases the same object moves through.
- If there are only a couple of small states and the transition rules are obvious, an enum and switch may stay clearer.

## Tradeoffs

### Pros

- localizes state-specific behavior
- makes transitions explicit
- reduces giant conditional blocks

### Cons

- adds more moving parts
- may be excessive for small state models
- can overlap with Strategy in confusing ways

## Nearby Patterns

- Strategy
- Template Method
- Memento

## Example

Before: an order object branches on `status` across approve, cancel, and fulfill methods, and invalid transitions are easy to miss.

After: each lifecycle state owns its allowed behavior and transition rules, so invalid moves become harder to express.

## Language Notes

Can be full objects, enum-associated behavior, state tables, or modules depending on how rich the state logic is.
