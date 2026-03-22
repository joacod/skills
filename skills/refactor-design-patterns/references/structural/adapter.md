# Adapter

## Category

Structural

## Intent

Convert one interface into another so existing code can work with an incompatible dependency.

## Problem It Solves

Use Adapter when a useful library, service, or legacy module almost fits your design but exposes the wrong shape.

## Signals

- integrations require repetitive translation code
- legacy or third-party APIs do not match your domain interface
- callers know too much about external quirks

## Anti-Signals

- you only need a small helper function
- the mismatch is tiny and isolated
- a broader simplification is needed instead of translation

## Structure

- target interface
- adapter
- adaptee

## Refactoring Clues

- repeated data reshaping around API boundaries
- conditionals that branch on provider-specific behavior at call sites

## Incremental Adoption

- define the interface the application wants
- adapt one external dependency to it
- migrate callers away from provider-specific code

## Decision Notes

- Choose Adapter when the main problem is interface mismatch or repeated translation.
- Prefer Facade when the subsystem shape is already compatible enough but too noisy or hard to use.
- Prefer Proxy when the interface should stay the same and the main concern is access control, caching, remoting, or lazy loading.

## Tradeoffs

### Pros

- isolates external quirks
- protects the domain from integration details
- makes swapping providers easier

### Cons

- adds one more layer to understand
- can hide poor boundaries if overused
- may duplicate concepts from the adaptee

## Nearby Patterns

- Facade
- Proxy
- Bridge

## Example

Before: each caller reshapes vendor-specific payloads and response fields before using them.

After: one adapter translates the vendor API into the application's preferred payment or shipping interface.

## Language Notes

Often a lightweight wrapper object or module; in dynamic languages this may just be a thin normalization function plus a stable interface.
