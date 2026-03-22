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

## Decision Notes

- Choose Decorator when the main goal is to layer optional behavior around the same core capability.
- Prefer Proxy when the wrapper exists to control access, hide remoting, defer initialization, or enforce policy while preserving the same service boundary.
- If the language already has an idiomatic middleware or higher-order-function mechanism, use that instead of forcing a class-heavy decorator structure.

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

## Example

Before: search handlers manually add logging, retry, and metrics logic around the same client call in several places.

After: each concern wraps the client as a composable layer, so the core search behavior stays focused and optional concerns can be stacked as needed.

## Language Notes

Common as middleware, higher-order functions, wrapper objects, or trait composition depending on the language.
