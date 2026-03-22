# Observer

## Category

Behavioral

## Intent

Define a one-to-many dependency so subscribers react when a subject changes.

## Problem It Solves

Use Observer when changes in one part of the system should trigger loosely coupled reactions in others.

## Signals

- several consumers react to the same event
- direct calls from publisher to all listeners create coupling
- reactions should be extensible over time

## Anti-Signals

- there is only one stable consumer
- event ordering guarantees are critical and complex
- direct orchestration is clearer than notification

## Structure

- subject or publisher
- observers or subscribers
- subscription and notification mechanism

## Refactoring Clues

- one class directly calling several dependent services after each change
- ad hoc hook lists or callback arrays scattered around the code

## Incremental Adoption

- identify the real event boundary
- publish one meaningful event
- move one consumer behind subscription before generalizing

## Tradeoffs

### Pros

- decouples publishers from subscribers
- makes reactions extensible
- supports event-driven design naturally

### Cons

- event flow can be hard to trace
- ordering and failure handling need care
- can degenerate into hidden control flow

## Nearby Patterns

- Mediator
- Chain of Responsibility
- State

## AI-Agent Analogy

Notify memory, logging, and monitoring components when a task state changes without hardwiring each dependency.

## Language Notes

Events, signals, pub-sub, or reactive streams often serve as the idiomatic form.
