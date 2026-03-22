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

## AI-Agent Analogy

Choose between fast, deep, low-cost, or tool-heavy execution modes without changing the caller.

## Language Notes

Often a natural fit for functions, interfaces, protocols, or trait objects depending on the language.
