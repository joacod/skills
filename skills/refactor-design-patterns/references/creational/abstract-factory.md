# Abstract Factory

## Category

Creational

## Intent

Provide an interface for creating related families of objects without coupling callers to concrete implementations.

## Problem It Solves

Use Abstract Factory when the code needs coordinated product families, such as UI components, drivers, clients, or environment-specific services that should vary together.

## Signals

- related objects must remain compatible
- environment or platform selection affects several products at once
- callers are mixing product family decisions with business logic

## Anti-Signals

- only one thing varies
- the products are unrelated
- a simple config map would be enough

## Structure

- abstract factory
- concrete factories
- related product interfaces

## Refactoring Clues

- repeated environment checks that create several matching collaborators
- tests that manually wire large compatible object sets

## Incremental Adoption

- group the related construction calls
- define the family boundary
- introduce one factory for a real variant
- add more families only if the compatibility rule matters

## Tradeoffs

### Pros

- keeps product families consistent
- removes environment-specific wiring from callers
- improves test setup for alternate families

### Cons

- adds many interfaces and types
- overkill when only one product varies
- can freeze the model around rigid families

## Nearby Patterns

- Factory Method
- Builder
- Bridge

## AI-Agent Analogy

Switch an agent between local, cloud, or sandbox tool stacks where each environment needs a matching set of clients and policies.

## Language Notes

Most explicit in statically typed OO languages; in dynamic languages it may look like a module or object that returns related factories or configured functions.
