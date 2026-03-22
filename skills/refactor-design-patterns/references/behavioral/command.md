# Command

## Category

Behavioral

## Intent

Encapsulate a request as an object so it can be queued, logged, retried, or undone.

## Problem It Solves

Use Command when actions themselves need identity and lifecycle beyond an immediate function call.

## Signals

- actions must be queued, scheduled, or retried
- you need undo, audit, or history
- invokers should trigger actions without knowing implementation details

## Anti-Signals

- a plain function call is enough
- action objects add ceremony without lifecycle value
- there is no need to store or transport actions

## Structure

- command interface
- concrete commands
- receiver
- invoker

## Refactoring Clues

- UI or API layers coupled directly to business operation implementations
- homegrown job payloads with ad hoc action metadata

## Incremental Adoption

- identify one action that benefits from storage or deferred execution
- wrap it as a command
- introduce invokers or queues only where the action lifecycle matters

## Tradeoffs

### Pros

- decouples senders from receivers
- enables queuing, retries, undo, and logging
- gives actions a first-class lifecycle

### Cons

- adds object count and boilerplate
- can be too heavy for direct calls
- command hierarchies can sprawl

## Nearby Patterns

- Chain of Responsibility
- Strategy
- Memento

## AI-Agent Analogy

Store agent actions like tool executions or plan steps as structured commands for replay or retry.

## Language Notes

Often maps well to job payload structs, callable objects, or serializable action records.
