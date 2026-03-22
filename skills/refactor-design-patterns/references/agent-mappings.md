# AI-Agent Mappings

Use this file only when an AI-agent analogy helps explain the pattern.
The analogy should support the recommendation, not replace software design reasoning.

## Routing and delegation

- Chain of Responsibility
- Command
- Mediator

Examples:
- planner -> executor -> validator chains
- task dispatch through registered handlers
- coordination through a central orchestrator

## Tool abstraction and integration

- Adapter
- Facade
- Proxy

Examples:
- wrapping different APIs behind one interface
- exposing a simpler tool surface
- adding permission, caching, or rate-limit controls

## Dynamic behavior selection

- Strategy
- State
- Template Method

Examples:
- fast mode vs deep mode
- behavior changing after a task phase changes
- fixed workflow with replaceable substeps

## Memory and recovery

- Memento

Examples:
- checkpointing plans
- restoring prior task state

## Event-driven systems

- Observer

## Composite systems

- Composite

## Object or configuration creation

- Factory Method
- Abstract Factory
- Builder
- Prototype
- Singleton
