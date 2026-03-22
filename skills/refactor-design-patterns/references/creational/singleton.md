# Singleton

## Category

Creational

## Intent

Ensure one shared instance and provide a controlled access point to it.

## Problem It Solves

Use Singleton sparingly when the system genuinely needs one shared coordinator, cache, registry, or resource manager.

## Signals

- there must be exactly one active instance
- global coordination is real, not just convenient
- lifecycle control matters

## Anti-Signals

- singleton is being used as hidden global state
- dependency injection would be clearer
- tests need isolated instances

## Structure

- singleton instance holder
- access point
- guarded initialization

## Refactoring Clues

- ad hoc module-level globals
- duplicate managers competing for the same shared resource

## Incremental Adoption

- first ask whether explicit dependency passing is clearer
- if one instance is required, centralize lifecycle and access
- keep the dependency visible to callers where practical

## Tradeoffs

### Pros

- enforces a single shared instance
- centralizes lifecycle rules
- can simplify access to one real shared resource

### Cons

- easily becomes disguised global state
- hurts testability
- often overused when wiring is the real problem

## Nearby Patterns

- Factory Method
- Facade
- Flyweight

## AI-Agent Analogy

A single run coordinator or registry used by all tool calls, only when having multiple instances would be wrong.

## Language Notes

Prefer module-level singletons or dependency containers only when justified; many languages offer simpler explicit wiring that is easier to test.
