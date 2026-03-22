# Template Method

## Category

Behavioral

## Intent

Define the skeleton of an algorithm once while allowing specific steps to vary.

## Problem It Solves

Use Template Method when several flows share the same high-level sequence but differ in a few steps.

## Signals

- workflows repeat the same ordering with minor variations
- duplicated algorithms differ only at a few points
- the sequence should remain fixed while some steps change

## Anti-Signals

- there is no stable overall sequence
- composition with Strategy would be clearer
- inheritance would create unnecessary rigidity

## Structure

- template method
- primitive operations or hooks
- subclasses or step providers

## Refactoring Clues

- nearly identical methods with duplicated setup, process, and cleanup phases
- subclass overrides that keep reimplementing the same outer flow

## Incremental Adoption

- identify the stable sequence
- extract the varying steps
- keep the template narrow and move variability out where possible

## Tradeoffs

### Pros

- removes duplicated algorithm structure
- preserves a stable workflow shape
- makes variation points explicit

### Cons

- can overcommit to inheritance
- hooks may become confusing
- less flexible than composition-based designs

## Nearby Patterns

- Strategy
- State
- Command

## AI-Agent Analogy

Keep a fixed workflow like plan -> execute -> validate while swapping the implementation of each step.

## Language Notes

In inheritance-light languages, the same idea may be better expressed with higher-order functions or composed step callbacks.
