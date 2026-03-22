# Iterator

## Category

Behavioral

## Intent

Traverse a collection without exposing its internal representation.

## Problem It Solves

Use Iterator when callers need stable traversal behavior while the underlying data structure should remain encapsulated.

## Signals

- collection internals leak into callers
- multiple traversal strategies are needed
- traversal logic is duplicated across features

## Anti-Signals

- native language iteration already solves the problem
- the structure is simple and internal details are harmless
- no custom traversal behavior is needed

## Structure

- aggregate
- iterator
- traversal state

## Refactoring Clues

- callers manually index into internal arrays or nodes
- traversal order logic repeated in multiple places

## Incremental Adoption

- expose a stable iteration API
- move traversal state out of callers
- add special iterators only if different traversals matter

## Tradeoffs

### Pros

- hides representation details
- centralizes traversal logic
- supports alternate traversal strategies

### Cons

- often redundant with language features
- custom iterators can add boilerplate
- can obscure simple collections

## Nearby Patterns

- Composite
- Visitor
- Command

## AI-Agent Analogy

Walk through task steps, memory entries, or tool results through one stable traversal API.

## Language Notes

Prefer native iterables, generators, or enumerators when available instead of building heavyweight custom iterators.
