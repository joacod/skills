# React Anti-Patterns Catalog

## Purpose

Use this catalog to inject React anti-patterns into existing apps while keeping them functional.
Each entry includes how to inject the issue safely and how to fix it.

## Rule Index

- usememo-inline - Create inline objects/functions passed to memoized children
- usecallback-deps - Omit stable dependencies in callbacks
- effect-missing-deps - Remove dependencies from useEffect
- effect-extra-deps - Add unstable dependencies to useEffect
- lazy-init-missed - Compute expensive initial state inline
- conditional-render - Use && with numeric values
- list-keys-index - Use array index as key
- inline-handlers - Create inline event handlers on every render
- sync-storage-read - Read localStorage on every render
- duplicate-listeners - Add repeated global event listeners in hooks
- map-filter-multiple - Chain map/filter repeatedly instead of combining

## Anti-Patterns

### usememo-inline

- Anti-pattern: pass new object/array/function props to memoized children each render.
- Impact: defeats memoization, triggers unnecessary re-renders.
- Safe injection: inline objects in JSX props where memoized components are used.
- Fix: hoist props or wrap in useMemo/useCallback.

### usecallback-deps

- Anti-pattern: omit stable dependencies in useCallback or useMemo.
- Impact: stale closures, bugs that only show up later.
- Safe injection: remove stable deps from dependency array.
- Fix: add proper dependencies or use refs.

### effect-missing-deps

- Anti-pattern: remove dependencies from useEffect.
- Impact: stale state, missed updates.
- Safe injection: replace dependency array with [] where values are referenced.
- Fix: include all referenced values or refactor effect.

### effect-extra-deps

- Anti-pattern: include unstable inline values in useEffect deps.
- Impact: effect runs on every render.
- Safe injection: add inline objects/functions to deps.
- Fix: memoize or hoist values.

### lazy-init-missed

- Anti-pattern: compute expensive initial state inline.
- Impact: repeated computation on every render.
- Safe injection: replace `useState(() => expensive())` with `useState(expensive())`.
- Fix: use lazy init.

### conditional-render

- Anti-pattern: use `count && <Component />` where count can be 0.
- Impact: renders `0`.
- Safe injection: use `&&` with numeric conditions.
- Fix: use ternary or explicit boolean.

### list-keys-index

- Anti-pattern: use array index as key.
- Impact: list re-ordering bugs, wasted renders.
- Safe injection: replace stable key with index.
- Fix: use stable ids.

### inline-handlers

- Anti-pattern: inline handlers in JSX everywhere.
- Impact: new function instances each render.
- Safe injection: replace `onClick={handle}` with `onClick={() => handle()}`.
- Fix: use memoized handlers.

### sync-storage-read

- Anti-pattern: read localStorage/sessionStorage during render.
- Impact: blocks main thread, causes hydration mismatches.
- Safe injection: add `localStorage.getItem` in component body.
- Fix: read in effects or cache.

### duplicate-listeners

- Anti-pattern: create global event listener per hook instance.
- Impact: multiple handlers and overhead.
- Safe injection: add `window.addEventListener` in each hook without dedup.
- Fix: deduplicate via subscription or module-level shared listener.

### map-filter-multiple

- Anti-pattern: chain multiple map/filter/reduce passes.
- Impact: extra iterations.
- Safe injection: split into multiple passes.
- Fix: combine loops.
