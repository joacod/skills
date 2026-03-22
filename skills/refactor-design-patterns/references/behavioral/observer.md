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

## Decision Notes

- Choose Observer when one subject emits events and multiple consumers should react independently.
- Prefer Mediator when the core problem is multi-step coordination among peers and one place should own the interaction rules.
- Be careful when delivery guarantees, strict ordering, or failure handling are central requirements; plain notifications may not be enough on their own.

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

## Example

Before: after an invoice is paid, the billing service directly calls receipt, analytics, and notification services in sequence.

After: the billing service publishes a payment event and each subscriber reacts without being hardwired into the publisher.

## Language Notes

Events, signals, pub-sub, or reactive streams often serve as the idiomatic form.
