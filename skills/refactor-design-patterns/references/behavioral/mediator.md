# Mediator

## Category

Behavioral

## Intent

Centralize collaboration logic so peers do not talk to each other directly in tangled ways.

## Problem It Solves

Use Mediator when many objects coordinate with one another and direct dependencies are turning the system into a mesh.

## Signals

- many-to-many communication is hard to follow
- changes in one collaborator ripple through others
- workflow coordination is spread across participants

## Anti-Signals

- there are only a few collaborators
- the mediator would become a giant god object
- simple event publication already solves the coupling

## Structure

- mediator
- colleague objects
- centralized coordination rules

## Refactoring Clues

- classes calling each other in cycles
- orchestration logic scattered across domain objects or UI components

## Incremental Adoption

- identify one noisy coordination flow
- centralize that interaction in a mediator
- keep domain logic local and move only collaboration rules

## Tradeoffs

### Pros

- reduces peer-to-peer coupling
- centralizes workflow rules
- makes collaboration changes easier

### Cons

- mediator can grow too large
- adds indirection
- risks moving too much domain logic into orchestration

## Nearby Patterns

- Observer
- Facade
- Chain of Responsibility

## AI-Agent Analogy

A coordinator manages planner, retriever, executor, and validator interactions so those parts stay decoupled.

## Language Notes

Often expressed as an orchestrator service, controller, or coordinator object rather than a formal classic mediator class.
