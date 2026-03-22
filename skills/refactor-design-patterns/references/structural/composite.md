# Composite

## Category

Structural

## Intent

Represent part-whole hierarchies so individual objects and groups can be treated uniformly.

## Problem It Solves

Use Composite when the domain naturally contains trees of items and callers should not care whether they are handling one node or a collection node.

## Signals

- recursive tree structures exist in the domain
- client code branches for leaf vs group handling
- operations should work on single items and nested groups alike

## Anti-Signals

- the structure is not actually hierarchical
- grouping behavior differs too much from leaf behavior
- a plain nested data structure would be simpler

## Structure

- component interface
- leaf
- composite node

## Refactoring Clues

- recursive traversal code duplicated across features
- special cases for item and collection processing

## Incremental Adoption

- define the minimal common operation set
- wrap existing leaves first
- introduce composite nodes only where grouping behavior is real

## Tradeoffs

### Pros

- simplifies tree handling
- reduces leaf-vs-group branching
- makes recursion a domain concept

### Cons

- common interface can become too broad
- some operations fit leaves and groups differently
- may hide invalid tree operations

## Nearby Patterns

- Decorator
- Iterator
- Visitor

## AI-Agent Analogy

Treat one agent step and a nested workflow of agent steps through a common execution interface.

## Language Notes

Works well with recursive interfaces, algebraic data types, or tagged unions depending on language style.
