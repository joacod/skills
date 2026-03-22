# Bridge

## Category

Structural

## Intent

Separate an abstraction from its implementation so both can vary independently.

## Problem It Solves

Use Bridge when two dimensions of change are becoming entangled, such as shape and renderer, command and transport, or policy and mechanism.

## Signals

- class explosion from combining variations
- one hierarchy varies for reasons unrelated to another
- changing implementation details forces abstraction changes

## Anti-Signals

- there is only one dimension of variation
- composition alone already solves the problem clearly
- the abstraction boundary is speculative

## Structure

- abstraction
- implementor interface
- concrete implementors

## Refactoring Clues

- subclasses named by combining two separate concerns
- duplicated logic across pairs of classes

## Incremental Adoption

- identify the two independent axes of change
- extract one axis behind an implementation boundary
- compose the abstraction with that boundary instead of subclassing combinations

## Tradeoffs

### Pros

- avoids combinatorial subclass growth
- lets concerns evolve independently
- improves substitution and testing

### Cons

- adds architectural upfront cost
- can feel abstract in small systems
- easy to confuse with simple composition

## Nearby Patterns

- Adapter
- Strategy
- Abstract Factory

## AI-Agent Analogy

Keep agent policy separate from execution backends so reasoning style and runtime environment can evolve independently.

## Language Notes

Usually expressed as composition with interfaces, traits, or protocols rather than inheritance-heavy designs.
