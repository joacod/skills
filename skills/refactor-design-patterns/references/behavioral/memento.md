# Memento

## Category

Behavioral

## Intent

Capture and restore an object's prior state without exposing its internals broadly.

## Problem It Solves

Use Memento when undo, rollback, checkpoints, or recovery are real requirements and state snapshots need a disciplined home.

## Signals

- the system needs undo or rollback
- long workflows need checkpoints
- recovery after partial failure matters

## Anti-Signals

- state is trivial to recompute
- snapshots would be too large or too frequent
- persistence or event sourcing is the real concern instead

## Structure

- originator
- memento snapshot
- caretaker of stored snapshots

## Refactoring Clues

- ad hoc copies of mutable state before risky actions
- rollback logic scattered through the codebase

## Incremental Adoption

- identify one operation that truly needs restore capability
- define the minimal snapshot shape
- keep snapshot storage outside business logic where possible

## Tradeoffs

### Pros

- supports undo and recovery cleanly
- localizes snapshot logic
- reduces ad hoc rollback code

### Cons

- snapshot size and lifecycle can be expensive
- hard to manage with large mutable graphs
- can hide the need for better immutable design

## Nearby Patterns

- Command
- Prototype
- State

## AI-Agent Analogy

Checkpoint an agent plan or intermediate workspace state before taking risky steps.

## Language Notes

Immutable data and persistent structures can sometimes replace explicit mementos more cleanly.
