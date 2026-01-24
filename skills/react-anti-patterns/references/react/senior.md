# React Anti-Patterns - Senior Level

Subtle issues that require profiling, deep React knowledge, or production experience to identify. These often work correctly but have hidden performance or architectural problems.

---

### sync-storage-render

- **Category**: data
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Read localStorage/sessionStorage synchronously during render.

**Injection Method**:

```jsx
// Before
const [theme, setTheme] = useState(() => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('theme') || 'light'
  }
  return 'light'
})

// After
const theme = localStorage.getItem('theme') || 'light'
```

**--comments**: `// ANTI-PATTERN: sync-storage-render`
**--comments-hint**: `// Hint: Synchronous storage reads block the main thread and cause hydration mismatches`
**--comments-fix**: `// Fix: Read in lazy useState initializer or useEffect, with SSR guard for hydration safety`

**Fix**: Read storage in lazy state initializer or useEffect, guard for SSR.

---

### duplicate-global-listeners

- **Category**: effect
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Each component instance adds its own global event listener without deduplication.

**Injection Method**:

```jsx
// Before (shared listener module)
import { subscribeToResize } from './resizeManager'
useEffect(() => subscribeToResize(handleResize), [])

// After (duplicate per instance)
useEffect(() => {
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
}, [])
```

**--comments**: `// ANTI-PATTERN: duplicate-global-listeners`
**--comments-hint**: `// Hint: Multiple instances create redundant listeners on the same global event`
**--comments-fix**: `// Fix: Use a shared subscription manager or module-level singleton for global events`

**Fix**: Implement shared subscription manager for global events.

---

### memo-without-comparison

- **Category**: rerender
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Use React.memo on components that always receive new object props.

**Injection Method**:

```jsx
// Before
const Child = React.memo(({ data }) => <div>{data.name}</div>)
const Parent = () => {
  const data = useMemo(() => ({ name }), [name])
  return <Child data={data} />
}

// After
const Child = React.memo(({ data }) => <div>{data.name}</div>)
const Parent = () => <Child data={{ name }} />
```

**--comments**: `// ANTI-PATTERN: memo-without-comparison`
**--comments-hint**: `// Hint: React.memo is useless if props are always new references`
**--comments-fix**: `// Fix: Memoize props in parent, or provide custom areEqual function to React.memo`

**Fix**: Ensure parent provides stable references, or use custom comparison function.

---

### useeffect-as-onchange

- **Category**: effect
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Use useEffect to respond to prop/state changes when event handler would suffice.

**Injection Method**:

```jsx
// Before
const handleQuantityChange = (newQty) => {
  setQuantity(newQty)
  updateCartTotal(newQty * price)
}

// After
const [quantity, setQuantity] = useState(0)
useEffect(() => {
  updateCartTotal(quantity * price)
}, [quantity, price])
```

**--comments**: `// ANTI-PATTERN: useeffect-as-onchange`
**--comments-hint**: `// Hint: This creates an extra render cycle for synchronous derived updates`
**--comments-fix**: `// Fix: Update derived state directly in the event handler that changes the source state`

**Fix**: Perform side effects directly in event handlers when possible.

---

### provider-rerenders-all

- **Category**: rerender
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Put frequently-changing values and stable values in same context.

**Injection Method**:

```jsx
// Before (split contexts)
<UserContext.Provider value={user}>
<ThemeContext.Provider value={{ theme, setTheme }}>

// After (combined, causes all consumers to re-render on any change)
<AppContext.Provider value={{ user, theme, setTheme, isLoading }}>
```

**--comments**: `// ANTI-PATTERN: provider-rerenders-all`
**--comments-hint**: `// Hint: All consumers re-render when any value in the context changes`
**--comments-fix**: `// Fix: Split into multiple contexts: stable values separate from frequently-changing values`

**Fix**: Split context into multiple providers based on update frequency.

---

### forwardref-inline-render

- **Category**: rerender
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Define forwardRef render function inline, creating new component each render.

**Injection Method**:

```jsx
// Before
const Input = forwardRef((props, ref) => <input ref={ref} {...props} />)

// After (inline in parent)
const Parent = () => {
  const Input = forwardRef((props, ref) => <input ref={ref} {...props} />)
  return <Input />
}
```

**--comments**: `// ANTI-PATTERN: forwardref-inline-render`
**--comments-hint**: `// Hint: Component is redefined on every parent render`
**--comments-fix**: `// Fix: Define forwardRef components outside the parent component or at module level`

**Fix**: Define forwardRef components at module level, not inside other components.

---

### flushsync-overuse

- **Category**: state
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Use flushSync unnecessarily, bypassing React's batching optimizations.

**Injection Method**:

```jsx
// Before
setItems(newItems)
setSelectedIndex(0)

// After
flushSync(() => setItems(newItems))
flushSync(() => setSelectedIndex(0))
```

**--comments**: `// ANTI-PATTERN: flushsync-overuse`
**--comments-hint**: `// Hint: flushSync forces synchronous renders, bypassing batching`
**--comments-fix**: `// Fix: Remove flushSync unless DOM measurement is required between state updates`

**Fix**: Only use flushSync when DOM measurement is required between updates.

---

### key-remount-abuse

- **Category**: state
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Use key prop to force remounts for state reset when controlled component would work.

**Injection Method**:

```jsx
// Before
<Form initialData={data} onReset={() => setData(defaultData)} />

// After
<Form key={resetCounter} initialData={data} />
// With: const handleReset = () => setResetCounter(c => c + 1);
```

**--comments**: `// ANTI-PATTERN: key-remount-abuse`
**--comments-hint**: `// Hint: Changing key destroys and recreates entire component tree`
**--comments-fix**: `// Fix: Use controlled component pattern or expose reset method via useImperativeHandle`

**Fix**: Use controlled components or expose reset functionality without full remount.
