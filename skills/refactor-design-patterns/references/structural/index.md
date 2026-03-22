# Structural Patterns

Use structural patterns when the main challenge is composition, wrapping, interoperability, access control, or exposing a simpler interface.

## Quick routing

- Need to connect incompatible interfaces -> Adapter
- Need to separate abstraction from implementation -> Bridge
- Need tree structures with uniform treatment -> Composite
- Need to add responsibilities without changing the original type -> Decorator
- Need a simpler entry point to a complex subsystem -> Facade
- Need to reduce memory usage by sharing intrinsic state -> Flyweight
- Need a stand-in that controls access -> Proxy

## Common caution

Do not wrap simple code just to satisfy a pattern name. If the boundary is already clean, leave it alone.
