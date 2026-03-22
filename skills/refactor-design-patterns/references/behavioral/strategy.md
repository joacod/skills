# Strategy

## Category

Behavioral

## Intent

Define a family of algorithms or behaviors, encapsulate each one, and make them interchangeable.

## Problem It Solves

Use Strategy when the same task can be solved in several meaningful ways and the caller should switch between them without branching through every case.

## Signals

- the same task has multiple behaviors or algorithms
- `if` or `switch` logic chooses between implementations
- behavior should be replaceable at runtime or by configuration

## Anti-Signals

- there is only one stable behavior
- the variants are tiny and unlikely to grow
- passing a function is already enough

## Structure

- context
- strategy interface
- concrete strategies

## Refactoring Clues

- a single method containing many alternative code paths
- repeated mode checks across several callers

## Incremental Adoption

- isolate the varying algorithm
- extract one alternate behavior behind a common seam
- move remaining variants only if the seam clearly improves the design

## Decision Notes

- Choose Strategy when the caller, configuration, or context selects among interchangeable behaviors.
- Prefer State instead when behavior changes mainly because the object moves through lifecycle stages and the transitions are part of the problem.
- In languages with strong function support, a function map or small callable objects may express the same idea with less ceremony.

## Tradeoffs

### Pros

- removes behavior-selection branching
- supports runtime substitution
- keeps algorithms focused and testable

### Cons

- adds indirection and extra types
- can be overkill for two tiny variants
- context and strategy boundaries may be awkward at first

## Nearby Patterns

- State
- Template Method
- Command

## Example

Before: one checkout service switches between pricing rules for standard, premium, and partner accounts.

After: each pricing rule lives behind the same calculation seam, and the caller selects the rule without growing the service's branching logic.

## Language Notes

Often a natural fit for functions, interfaces, protocols, or trait objects depending on the language.
