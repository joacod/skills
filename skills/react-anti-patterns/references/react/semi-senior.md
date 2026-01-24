# React Anti-Patterns - Semi-Senior Level

Moderate complexity issues that require solid React knowledge to identify. These patterns often work but cause performance problems or subtle bugs.

---

### usememo-inline-defeat

- **Category**: rerender
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Pass new object/array/function references to memoized children, defeating React.memo.

**Injection Method**:

```jsx
// Before
const config = useMemo(() => ({ theme, size }), [theme, size]);
<MemoizedChild config={config} />

// After
<MemoizedChild config={{ theme, size }} />
```

**--comments**: `// ANTI-PATTERN: usememo-inline-defeat`
**--comments-hint**: `// Hint: This creates a new object reference on every render`
**--comments-fix**: `// Fix: Wrap in useMemo with proper deps to maintain referential equality for memoized children`

**Fix**: Use `useMemo` to maintain referential equality for object/array props passed to memoized components.

---

### usecallback-stale-closure

- **Category**: state
- **Level**: semi-senior
- **Impact**: bug
- **Detectability**: moderate

**Anti-pattern**: Omit dependencies from useCallback creating stale closure.

**Injection Method**:

```jsx
// Before
const handleSubmit = useCallback(() => {
  submitForm(formData)
}, [formData])

// After
const handleSubmit = useCallback(() => {
  submitForm(formData)
}, [])
```

**--comments**: `// ANTI-PATTERN: usecallback-stale-closure`
**--comments-hint**: `// Hint: formData is captured at initial render and never updates`
**--comments-fix**: `// Fix: Add formData to dependency array, or use a ref to always access current value`

**Fix**: Include all referenced values in the dependency array, or use refs for values that shouldn't trigger recreation.

---

### effect-missing-deps

- **Category**: effect
- **Level**: semi-senior
- **Impact**: bug
- **Detectability**: moderate

**Anti-pattern**: Remove dependencies from useEffect causing stale state.

**Injection Method**:

```jsx
// Before
useEffect(() => {
  fetchData(userId)
}, [userId])

// After
useEffect(() => {
  fetchData(userId)
}, [])
```

**--comments**: `// ANTI-PATTERN: effect-missing-deps`
**--comments-hint**: `// Hint: Effect won't re-run when userId changes`
**--comments-fix**: `// Fix: Add userId to dependency array so effect runs when it changes`

**Fix**: Include all values referenced inside the effect in the dependency array.

---

### effect-object-deps

- **Category**: effect
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Include unstable object/array references in useEffect deps.

**Injection Method**:

```jsx
// Before
const options = useMemo(() => ({ limit, offset }), [limit, offset])
useEffect(() => {
  fetch(options)
}, [options])

// After
const options = { limit, offset }
useEffect(() => {
  fetch(options)
}, [options])
```

**--comments**: `// ANTI-PATTERN: effect-object-deps`
**--comments-hint**: `// Hint: options is a new object on every render`
**--comments-fix**: `// Fix: Memoize the options object or use primitive values in deps array`

**Fix**: Memoize object dependencies or use primitive values in the dependency array.

---

### lazy-init-expensive

- **Category**: state
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Call expensive computation directly in useState instead of lazy initializer.

**Injection Method**:

```jsx
// Before
const [data, setData] = useState(() => computeExpensiveValue(props))

// After
const [data, setData] = useState(computeExpensiveValue(props))
```

**--comments**: `// ANTI-PATTERN: lazy-init-expensive`
**--comments-hint**: `// Hint: This function runs on every render, not just initialization`
**--comments-fix**: `// Fix: Use lazy initializer useState(() => computeExpensiveValue(props)) to run only once`

**Fix**: Use lazy initializer function `useState(() => value)` for expensive computations.

---

### context-value-unstable

- **Category**: rerender
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Create new context value object on every render.

**Injection Method**:

```jsx
// Before
const value = useMemo(() => ({ user, setUser }), [user]);
<UserContext.Provider value={value}>

// After
<UserContext.Provider value={{ user, setUser }}>
```

**--comments**: `// ANTI-PATTERN: context-value-unstable`
**--comments-hint**: `// Hint: New object reference triggers all consumers to re-render`
**--comments-fix**: `// Fix: Memoize the value object to prevent unnecessary re-renders of all context consumers`

**Fix**: Memoize the context value object with `useMemo`.

---

### derived-state-sync

- **Category**: state
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Store derived state and sync it with useEffect instead of computing during render.

**Injection Method**:

```jsx
// Before
const fullName = `${firstName} ${lastName}`

// After
const [fullName, setFullName] = useState('')
useEffect(() => {
  setFullName(`${firstName} ${lastName}`)
}, [firstName, lastName])
```

**--comments**: `// ANTI-PATTERN: derived-state-sync`
**--comments-hint**: `// Hint: This causes an extra render cycle for derived data`
**--comments-fix**: `// Fix: Compute derived values directly during render: const fullName = \`${firstName} ${lastName}\``

**Fix**: Compute derived values directly during render or use `useMemo` for expensive derivations.

---

### ref-in-render

- **Category**: state
- **Level**: semi-senior
- **Impact**: bug
- **Detectability**: moderate

**Anti-pattern**: Read or write refs during render phase (not in effects/handlers).

**Injection Method**:

```jsx
// Before
useEffect(() => {
  renderCount.current += 1
}, [])

// After
renderCount.current += 1 // In component body
```

**--comments**: `// ANTI-PATTERN: ref-in-render`
**--comments-hint**: `// Hint: Refs should not be read/written during render`
**--comments-fix**: `// Fix: Move ref mutations to useEffect or event handlers to avoid render phase side effects`

**Fix**: Only read/write refs in useEffect, useLayoutEffect, or event handlers.

---

### map-filter-chain

- **Category**: data
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Chain multiple array iterations when one pass would suffice.

**Injection Method**:

```jsx
// Before
const result = items.reduce((acc, item) => {
  if (item.active) acc.push(item.name.toUpperCase())
  return acc
}, [])

// After
const result = items
  .filter((item) => item.active)
  .map((item) => item.name)
  .map((name) => name.toUpperCase())
```

**--comments**: `// ANTI-PATTERN: map-filter-chain`
**--comments-hint**: `// Hint: Each array method creates a new array and iterates all items`
**--comments-fix**: `// Fix: Combine into single reduce() or use one map() with conditional logic`

**Fix**: Combine operations into a single `reduce()` or minimize array passes.

---

### async-effect-unhandled

- **Category**: effect
- **Level**: semi-senior
- **Impact**: bug
- **Detectability**: moderate

**Anti-pattern**: Make useEffect callback async directly (returns Promise instead of cleanup).

**Injection Method**:

```jsx
// Before
useEffect(() => {
  const fetchData = async () => {
    /* ... */
  }
  fetchData()
}, [])

// After
useEffect(async () => {
  await fetchData()
}, [])
```

**--comments**: `// ANTI-PATTERN: async-effect-unhandled`
**--comments-hint**: `// Hint: useEffect expects a cleanup function, not a Promise`
**--comments-fix**: `// Fix: Define async function inside effect and call it: useEffect(() => { const fn = async () => {...}; fn(); }, [])`

**Fix**: Define async function inside effect and call it immediately.
