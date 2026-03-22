# Builder

## Category

Creational

## Intent

Construct a complex object step by step so the assembly process is clear and optional pieces stay manageable.

## Problem It Solves

Use Builder when constructors or setup functions have too many parameters, optional parts, or ordering rules.

## Signals

- constructors are long or hard to read
- partial configuration leads to invalid objects
- assembly happens in stages

## Anti-Signals

- the object is small and stable
- a plain config object is already readable
- there are no meaningful assembly steps

## Structure

- builder
- product
- optional director or orchestration flow

## Refactoring Clues

- telescoping constructors
- repeated setup sequences copied across callers

## Incremental Adoption

- extract repeated setup into named steps
- introduce a builder around the unstable construction path
- keep direct construction for simple cases if that remains clearer

## Decision Notes

- Choose Builder when the object or workflow is assembled in stages and invalid or incomplete setup is a real risk.
- Prefer Factory Method when the main question is which variant to create, not how to assemble it.
- If keyword arguments, config objects, or functional options already make setup readable, keep the lighter option.

## Tradeoffs

### Pros

- makes complex setup explicit
- handles optional parts well
- improves readability for staged construction

### Cons

- adds extra type or API surface
- can be unnecessary for simple data structures
- directors are often overused

## Nearby Patterns

- Factory Method
- Abstract Factory
- Prototype

## Example

Before: export-job creation sprawls across call sites with optional filters, destination settings, formatting rules, and notification hooks.

After: one builder makes the staged setup explicit and keeps invalid partial configurations harder to construct.

## Language Notes

Classic fluent builders fit Java, C#, and TypeScript; Python, Ruby, and Go often prefer option structs, keyword args, or functional options if they stay simpler.
