# React Anti-Patterns - Junior Level

Obvious issues that should be easy to spot during code review. These are common mistakes made by developers new to React.

---

### list-keys-index

- **Category**: list
- **Level**: junior
- **Impact**: bug
- **Detectability**: easy

**Anti-pattern**: Use array index as key in list rendering.

**Injection Method**:

```jsx
// Before
{
  items.map((item) => <Item key={item.id} {...item} />)
}

// After
{
  items.map((item, index) => <Item key={index} {...item} />)
}
```

**--comments**: `// ANTI-PATTERN: list-keys-index`
**--comments-hint**: `// Hint: Array index as key causes issues when list order changes`
**--comments-fix**: `// Fix: Use a stable unique identifier (item.id) instead of index to preserve component state during reordering`

**Fix**: Use stable unique identifiers from the data (e.g., `item.id`) instead of array index.

---

### conditional-render-zero

- **Category**: conditional
- **Level**: junior
- **Impact**: visual
- **Detectability**: easy

**Anti-pattern**: Use `&&` with numeric values that can be 0 or falsy.

**Injection Method**:

```jsx
// Before
{
  items.length > 0 && <ItemList items={items} />
}

// After
{
  items.length && <ItemList items={items} />
}
```

**--comments**: `// ANTI-PATTERN: conditional-render-zero`
**--comments-hint**: `// Hint: What happens when items.length is 0?`
**--comments-fix**: `// Fix: Use explicit boolean (items.length > 0) or ternary to prevent rendering '0' in the DOM`

**Fix**: Use explicit boolean check (`items.length > 0`) or ternary operator.

---

### inline-handlers-simple

- **Category**: rerender
- **Level**: junior
- **Impact**: performance
- **Detectability**: easy

**Anti-pattern**: Create new function instances inline in JSX for every render.

**Injection Method**:

```jsx
// Before
const handleClick = useCallback(() => doSomething(id), [id]);
<Button onClick={handleClick} />

// After
<Button onClick={() => doSomething(id)} />
```

**--comments**: `// ANTI-PATTERN: inline-handlers-simple`
**--comments-hint**: `// Hint: This creates a new function on every render`
**--comments-fix**: `// Fix: Extract handler to useCallback or define outside JSX to prevent unnecessary re-renders of memoized children`

**Fix**: Use `useCallback` or define handlers outside JSX when passed to memoized components.

---

### missing-key-prop

- **Category**: list
- **Level**: junior
- **Impact**: bug
- **Detectability**: easy

**Anti-pattern**: Omit the key prop entirely in list rendering.

**Injection Method**:

```jsx
// Before
{
  items.map((item) => <Item key={item.id} data={item} />)
}

// After
{
  items.map((item) => <Item data={item} />)
}
```

**--comments**: `// ANTI-PATTERN: missing-key-prop`
**--comments-hint**: `// Hint: React needs keys to track list items`
**--comments-fix**: `// Fix: Add key={item.id} to help React identify which items changed, added, or removed`

**Fix**: Always provide a unique key prop to list items.

---

### state-object-mutation

- **Category**: state
- **Level**: junior
- **Impact**: bug
- **Detectability**: easy

**Anti-pattern**: Mutate state object directly instead of creating new reference.

**Injection Method**:

```jsx
// Before
setUser({ ...user, name: newName })

// After
user.name = newName
setUser(user)
```

**--comments**: `// ANTI-PATTERN: state-object-mutation`
**--comments-hint**: `// Hint: React uses reference equality to detect changes`
**--comments-fix**: `// Fix: Create a new object with spread operator: setUser({ ...user, name: newName })`

**Fix**: Always create new object/array references when updating state.

---

### state-array-mutation

- **Category**: state
- **Level**: junior
- **Impact**: bug
- **Detectability**: easy

**Anti-pattern**: Use mutating array methods like push, pop, splice on state.

**Injection Method**:

```jsx
// Before
setItems([...items, newItem])

// After
items.push(newItem)
setItems(items)
```

**--comments**: `// ANTI-PATTERN: state-array-mutation`
**--comments-hint**: `// Hint: push/pop/splice mutate the original array`
**--comments-fix**: `// Fix: Use spread operator [...items, newItem] or toSorted()/toSpliced() for immutable updates`

**Fix**: Use spread operator, concat, filter, map, or immutable methods like `toSorted()`.

---

### useeffect-no-cleanup

- **Category**: effect
- **Level**: junior
- **Impact**: bug
- **Detectability**: easy

**Anti-pattern**: Add event listeners or subscriptions without cleanup.

**Injection Method**:

```jsx
// Before
useEffect(() => {
  window.addEventListener('resize', handleResize)
  return () => window.removeEventListener('resize', handleResize)
}, [])

// After
useEffect(() => {
  window.addEventListener('resize', handleResize)
}, [])
```

**--comments**: `// ANTI-PATTERN: useeffect-no-cleanup`
**--comments-hint**: `// Hint: What happens when this component unmounts?`
**--comments-fix**: `// Fix: Return a cleanup function that removes the listener to prevent memory leaks`

**Fix**: Return a cleanup function from useEffect to remove listeners/subscriptions.

---

### props-spreading-uncontrolled

- **Category**: state
- **Level**: junior
- **Impact**: bug
- **Detectability**: easy

**Anti-pattern**: Spread unknown props directly to DOM elements without filtering.

**Injection Method**:

```jsx
// Before
const { className, onClick, ...safeProps } = props;
<div className={className} onClick={onClick} />

// After
<div {...props} />
```

**--comments**: `// ANTI-PATTERN: props-spreading-uncontrolled`
**--comments-hint**: `// Hint: Unknown props may cause React DOM warnings`
**--comments-fix**: `// Fix: Destructure known props and only spread safe ones, or filter out non-DOM attributes`

**Fix**: Destructure and explicitly pass known props, or filter props before spreading.
