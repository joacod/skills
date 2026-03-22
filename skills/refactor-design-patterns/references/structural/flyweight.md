# Flyweight

## Category

Structural

## Intent

Share intrinsic state across many similar objects to reduce memory use.

## Problem It Solves

Use Flyweight when a huge number of near-identical objects make memory or allocation costs meaningful and shared immutable state can be separated from per-instance state.

## Signals

- very large object counts
- most object data is repeated
- performance or memory pressure is measurable

## Anti-Signals

- memory pressure is not actually a problem
- the shared state is not stable or immutable
- readability would suffer more than performance improves

## Structure

- flyweight shared state
- extrinsic per-instance state
- factory or cache of shared flyweights

## Refactoring Clues

- repeated large objects that differ only by a small key
- allocations dominating profiling results

## Incremental Adoption

- measure first
- separate intrinsic from extrinsic state
- introduce shared instances behind a factory or cache

## Tradeoffs

### Pros

- reduces memory usage
- can lower allocation overhead
- makes repeated shared state explicit

### Cons

- adds complexity to state management
- can hurt readability
- often premature without profiling data

## Nearby Patterns

- Singleton
- Factory Method
- Prototype

## AI-Agent Analogy

Share immutable prompt templates or tool metadata across many executions while keeping per-run state separate.

## Language Notes

Most useful in performance-sensitive systems; many codebases never need it.
