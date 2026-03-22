# Prototype

## Category

Creational

## Intent

Create new objects by copying an existing prototype instead of rebuilding them from scratch.

## Problem It Solves

Use Prototype when setup is expensive, defaults are rich, or callers need templated variations of a configured object.

## Signals

- many objects start from the same configured baseline
- setup is verbose or expensive
- cloning a template is clearer than reconstructing it

## Anti-Signals

- objects are simple to construct directly
- copying is unsafe or confusing
- shared mutable state would create bugs

## Structure

- prototype interface or clone behavior
- concrete prototypes
- client that copies and customizes

## Refactoring Clues

- repeated setup code with small differences
- fixtures or configs copied by hand across tests or workflows

## Incremental Adoption

- identify a stable configured baseline
- add explicit copy or clone behavior
- customize the copy at the edges

## Tradeoffs

### Pros

- reduces repeated setup
- makes template-based variants easy
- can improve performance for expensive initialization

### Cons

- deep vs shallow copy rules can be tricky
- hidden shared state can surprise callers
- harder to reason about than explicit construction

## Nearby Patterns

- Builder
- Factory Method
- Memento

## AI-Agent Analogy

Clone a configured workflow template and tweak the toolset, budget, or prompts for a specific task.

## Language Notes

Use explicit copy APIs where possible; language-native cloning can be too implicit if object graphs are complex.
