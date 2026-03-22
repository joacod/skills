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

## AI-Agent Analogy

Wrap several tool APIs so the agent sees one consistent interface for search, storage, or execution.

## Language Notes

Often a lightweight wrapper object or module; in dynamic languages this may just be a thin normalization function plus a stable interface.
