# Refactoring Workflow

Use this workflow before naming a pattern.

## 1. Diagnose the pressure

Describe the real issue in plain language.
Examples:
- too many branches to choose behavior
- construction logic is duplicated and fragile
- a subsystem is hard to use because callers know too much
- state is spread across flags and conditionals
- a new integration requires repeated glue code

## 2. Check whether a pattern is justified

A pattern is more likely to help when:
- the same pain shows up repeatedly
- the code needs more than one variation today, not just maybe later
- the current design makes extension risky or repetitive
- the new abstraction creates a simpler mental model

A pattern is less likely to help when:
- the change is speculative
- there is only one stable implementation
- the pattern would add more types and indirection than value
- a local extraction or boundary cleanup would solve the problem

## 3. Route by category

- Creation problem -> Creational
- Composition or compatibility problem -> Structural
- Behavior, state, or collaboration problem -> Behavioral

## 4. Compare nearby patterns

Do not stop at the first plausible pattern.
Check the most likely alternatives and explain why they fit worse or better.
Examples:
- Strategy vs State
- Adapter vs Facade
- Decorator vs Proxy
- Factory Method vs Builder
- Observer vs Mediator

## 5. Recommend the smallest useful change

Prefer an incremental path such as:
1. isolate the changing behavior
2. introduce the minimal interface or boundary
3. move one concrete case behind it
4. keep old call sites working while the design settles
5. finish the migration only if the new shape proves worthwhile

## 6. Tailor to the language

The pattern stays the same, but the expression changes.
Examples:
- interfaces and classes in Java or C#
- protocols, enums, or value types in Swift
- first-class functions and modules in JavaScript, TypeScript, Python, Ruby, or Go
- traits and enums in Rust

Prefer idiomatic constructs over textbook ceremony.

## 7. Explain tradeoffs

Every recommendation should mention:
- what becomes easier
- what becomes more complex
- when to stop refactoring
