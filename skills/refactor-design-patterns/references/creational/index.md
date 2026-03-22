# Creational Patterns

Use creational patterns when the main challenge is how objects, services, clients, modules, or configured workflows are created.

## Quick routing

- Need subclasses or variants to decide what gets created -> Factory Method
- Need families of related products that must stay compatible -> Abstract Factory
- Need step-by-step assembly with optional parts -> Builder
- Need cloning or templated copies -> Prototype
- Need one shared instance with controlled access -> Singleton

## Common caution

Do not introduce a creational pattern if a plain constructor, function, or config object is already clear enough.
