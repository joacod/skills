# Factory Method

## Category

Creational

## Intent

Delegate object creation to a method so callers depend on a stable creation contract instead of concrete classes.

## Problem It Solves

Use Factory Method when creation varies by subtype or context and constructors are leaking those decisions into callers.

## Signals

- callers choose concrete classes directly
- construction branches are repeated in multiple places
- subclasses or variants need to decide what to create

## Anti-Signals

- there is only one concrete implementation
- creation logic is trivial and local
- a simple helper function would solve the duplication

## Structure

- creator
- factory method
- concrete products

## Refactoring Clues

- repeated `if` or `switch` blocks that pick a concrete type
- direct constructor calls scattered across the codebase

## Incremental Adoption

- extract creation into one function or method
- hide concrete type decisions behind that boundary
- move additional callers to the factory only if the seam proves useful

## Tradeoffs

### Pros

- centralizes creation rules
- reduces caller coupling to concrete types
- makes variants easier to add

### Cons

- adds indirection
- can become ceremonial in small codebases
- may overlap with plain functions in dynamic languages

## Nearby Patterns

- Abstract Factory
- Builder
- Prototype

## AI-Agent Analogy

Choose a tool wrapper or executor type based on task kind without forcing every caller to know the concrete implementation.

## Language Notes

Often a class hierarchy in Java or C#, a factory function in JavaScript or Python, or a constructor helper in Go or Rust.
