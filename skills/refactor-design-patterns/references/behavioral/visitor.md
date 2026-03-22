# Visitor

## Category

Behavioral

## Intent

Add new operations to a stable object structure without changing the element classes each time.

## Problem It Solves

Use Visitor when the structure is stable, the operations keep changing, and scattering those operations across element classes would be painful.

## Signals

- many operations run over the same object structure
- the structure changes rarely but behaviors change often
- operations need type-specific logic without giant type checks in one place

## Anti-Signals

- the object structure changes frequently
- only one or two operations exist
- the language offers simpler pattern matching or exhaustive dispatch

## Structure

- visitor interface
- concrete visitors
- visited element types

## Refactoring Clues

- repeated type switches over a stable AST, document tree, or command tree
- new operations forcing edits across many core classes

## Incremental Adoption

- confirm the structure is actually stable
- move one cross-cutting operation into a visitor
- stop if pattern matching or methods on the elements remain clearer

## Tradeoffs

### Pros

- centralizes operations over stable structures
- keeps element classes focused
- helps avoid repeated type-switch logic

### Cons

- adding new element types becomes expensive
- double dispatch can be hard to explain
- often too formal for modern language features

## Nearby Patterns

- Iterator
- Composite
- Strategy

## AI-Agent Analogy

Run different analyses over a stable plan tree or action graph without changing each node type for every new operation.

## Language Notes

Modern enums, tagged unions, or pattern matching may be simpler than classic Visitor in many languages.
