# Facade

## Category

Structural

## Intent

Provide a simple entry point to a complex subsystem.

## Problem It Solves

Use Facade when callers need to perform common tasks but currently must understand too many low-level details and call sequences.

## Signals

- many callers repeat the same orchestration steps
- subsystem APIs are broad and difficult to use correctly
- onboarding is slow because internal details leak everywhere

## Anti-Signals

- the subsystem is already small and clear
- callers genuinely need fine-grained control
- the real issue is incompatible interfaces, not complexity

## Structure

- facade
- subsystem services or modules
- simplified task-oriented API

## Refactoring Clues

- copy-pasted setup and teardown sequences
- long call chains that appear in many features

## Incremental Adoption

- identify the common high-level tasks
- wrap one noisy workflow behind a simpler entry point
- keep escape hatches for advanced use only where needed

## Tradeoffs

### Pros

- reduces cognitive load for callers
- centralizes common orchestration
- hides subsystem churn

### Cons

- can become a god object if too broad
- may hide useful subsystem capabilities
- risks becoming a second API to maintain

## Nearby Patterns

- Adapter
- Proxy
- Mediator

## AI-Agent Analogy

Expose a single tool command that coordinates several low-level tools the agent would otherwise need to call in sequence.

## Language Notes

Often a service object, module, or package-level function with a task-oriented API.
