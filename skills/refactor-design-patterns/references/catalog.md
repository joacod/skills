# Refactor Design Patterns Catalog

## Purpose

Use this catalog to route from a concrete design problem to a small set of candidate patterns.
Start from the pressure in the code, not from pattern names.

## Categories

### Creational

Use when the main problem is how objects, services, components, clients, or configured workflows are created.

Patterns:
- Factory Method
- Abstract Factory
- Builder
- Prototype
- Singleton

### Structural

Use when the main problem is composition, wrapping, compatibility, access control, or simplifying a subsystem.

Patterns:
- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

### Behavioral

Use when the main problem is runtime behavior, communication, control flow, state, orchestration, or request handling.

Patterns:
- Chain of Responsibility
- Command
- Iterator
- Mediator
- Memento
- Observer
- State
- Strategy
- Template Method
- Visitor

## Quick selection guidance

- If the pain is object or service creation, start with Creational.
- If the pain is wrappers, boundaries, or composition, start with Structural.
- If the pain is decision-making, routing, state, or collaboration, start with Behavioral.

## Common sense rule

Before recommending any pattern, check whether the code only needs:
- a small extraction
- a rename
- one more helper function
- one better boundary between modules

If the simple move solves the issue, prefer it.
