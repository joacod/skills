# Proxy

## Category

Structural

## Intent

Provide a stand-in for another object to control access, add policy, or defer work.

## Problem It Solves

Use Proxy when the underlying object should remain behind access rules, lazy loading, remote boundaries, caching, or instrumentation.

## Signals

- access must be controlled or observed
- initialization is expensive and can be deferred
- local callers should treat remote or guarded resources as normal collaborators

## Anti-Signals

- behavior is just optional decoration
- there is no real access-control or lifecycle concern
- a direct wrapper would be clearer

## Structure

- subject interface
- real subject
- proxy with control logic

## Refactoring Clues

- repeated permission, caching, or lazy-load checks around the same dependency
- remote calls leaking transport concerns into business logic

## Incremental Adoption

- keep the subject interface stable
- put one control concern into the proxy
- migrate callers without changing their expectations

## Tradeoffs

### Pros

- centralizes access policy
- hides expensive or remote boundaries
- keeps callers unaware of control mechanics

### Cons

- behavior can become surprising if hidden too well
- adds another layer to debug
- often confused with Decorator or Adapter

## Nearby Patterns

- Decorator
- Adapter
- Facade

## AI-Agent Analogy

Front a tool with rate limits, permission checks, lazy initialization, or audit logging while preserving the same call interface.

## Language Notes

Can be a wrapper object, middleware layer, or lazy-loading handle depending on runtime style.
