# Behavioral Patterns

Use behavioral patterns when the main challenge is communication, workflow, request routing, state transitions, interchangeable logic, or collaboration.

## Quick routing

- Need a request to pass through multiple handlers -> Chain of Responsibility
- Need to turn actions into objects -> Command
- Need to traverse a structure without exposing internals -> Iterator
- Need to reduce direct coupling among many collaborators -> Mediator
- Need snapshots and restoration -> Memento
- Need one-to-many notifications -> Observer
- Need behavior that changes with internal state -> State
- Need interchangeable algorithms -> Strategy
- Need fixed workflow skeleton with overridable steps -> Template Method
- Need new operations over a stable object structure -> Visitor

## Common caution

If behavior differences are tiny and stable, a function parameter or local extraction may be enough.
