# Decorator

## Category

Structural

## Intent

Add responsibilities to an object dynamically by wrapping it instead of changing the original implementation.

## Problem It Solves

Use Decorator when behavior needs optional layering such as logging, metrics, caching, retries, formatting, or validation.

## Signals

- optional cross-cutting behavior stacks up around one interface
- subclassing combinations are multiplying
- callers should compose features without changing core logic

## Anti-Signals

- the added behavior is not truly optional
- only one wrapper layer will ever exist
- a simpler helper or middleware mechanism already fits better

## Structure

- component interface
- concrete component
- decorators wrapping the same interface

## Refactoring Clues

- many subclasses created only to add one concern
- repeated pre/post behavior around the same calls

## Incremental Adoption

- stabilize the core interface
- extract one cross-cutting behavior into a wrapper
- add more wrappers only when composition remains readable

## Tradeoffs

### Pros

- composes optional responsibilities cleanly
- avoids subclass explosion
- keeps the core component focused

### Cons

- wrapper chains can be hard to trace
- debugging order-sensitive behavior gets harder
- identity and configuration can become noisy

## Nearby Patterns

- Proxy
- Facade
- Composite

## AI-Agent Analogy

Wrap a tool executor with logging, caching, permission checks, or retry behavior without changing the core executor.

## Language Notes

Common as middleware, higher-order functions, wrapper objects, or trait composition depending on the language.
