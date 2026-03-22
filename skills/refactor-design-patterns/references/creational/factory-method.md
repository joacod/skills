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

## Decision Notes

- Choose Factory Method when the main problem is deciding which concrete variant to create.
- Prefer Builder when the hard part is assembling one complex object step by step with optional parts or ordering rules.
- In dynamic languages, a small factory function may capture the same idea without needing a full textbook class hierarchy.

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

## Example

Before: several callers switch on report type and directly instantiate `PdfExporter`, `CsvExporter`, or `HtmlExporter`.

After: one creation boundary chooses the exporter variant so callers depend on the export contract rather than concrete classes.

## Language Notes

Often a class hierarchy in Java or C#, a factory function in JavaScript or Python, or a constructor helper in Go or Rust.
