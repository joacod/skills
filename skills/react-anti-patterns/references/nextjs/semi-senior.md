# Next.js Anti-Patterns - Semi-Senior Level

Moderate complexity Next.js issues requiring understanding of server/client boundaries, data fetching patterns, and bundle optimization.

---

### sequential-server-fetches

- **Category**: waterfall
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Await multiple independent fetches sequentially instead of in parallel.

**Injection Method**:

```tsx
// Before
async function Page() {
  const [user, posts, comments] = await Promise.all([
    getUser(),
    getPosts(),
    getComments(),
  ])
}

// After
async function Page() {
  const user = await getUser()
  const posts = await getPosts()
  const comments = await getComments()
}
```

**--comments**: `// ANTI-PATTERN: sequential-server-fetches`
**--comments-hint**: `// Hint: Each await waits for the previous to complete`
**--comments-fix**: `// Fix: Use Promise.all() for independent fetches to run them in parallel`

**Fix**: Use `Promise.all()` for independent data fetches.

---

### no-dynamic-import

- **Category**: bundle
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Import heavy client components statically instead of using dynamic imports.

**Injection Method**:

```tsx
// Before
import dynamic from 'next/dynamic'
const Chart = dynamic(() => import('./Chart'), { ssr: false })

// After
import Chart from './Chart'
```

**--comments**: `// ANTI-PATTERN: no-dynamic-import`
**--comments-hint**: `// Hint: Heavy components increase initial bundle size`
**--comments-fix**: `// Fix: Use next/dynamic for code splitting: dynamic(() => import('./Chart'), { ssr: false })`

**Fix**: Use `next/dynamic` for heavy client-only components.

---

### layout-data-refetch

- **Category**: waterfall
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Fetch same data in both layout and page instead of passing via props or using cache.

**Injection Method**:

```tsx
// Before (layout fetches and passes)
// layout.tsx
const user = await getUser()
return <>{children}</>
// Uses React cache or passes via context

// After (both fetch independently)
// layout.tsx
const user = await getUser()
// page.tsx
const user = await getUser() // Duplicate fetch
```

**--comments**: `// ANTI-PATTERN: layout-data-refetch`
**--comments-hint**: `// Hint: Same data is fetched in multiple places`
**--comments-fix**: `// Fix: Use React cache() to dedupe, or restructure to fetch once and pass down`

**Fix**: Use React `cache()` to deduplicate fetches, or pass data through props/context.

---

### client-heavy-barrel

- **Category**: bundle
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Import from barrel files in Client Components, pulling in unused code.

**Injection Method**:

```tsx
// Before
import { Button } from '@/components/ui/Button'

// After
import { Button } from '@/components/ui' // Barrel file with many exports
```

**--comments**: `// ANTI-PATTERN: client-heavy-barrel`
**--comments-hint**: `// Hint: Barrel imports may include tree-shaking-resistant code`
**--comments-fix**: `// Fix: Import directly from component file to ensure proper tree-shaking`

**Fix**: Import directly from specific modules, not barrel files, in Client Components.

---

### router-push-in-effect

- **Category**: rsc
- **Level**: semi-senior
- **Impact**: performance
- **Detectability**: moderate

**Anti-pattern**: Use client-side redirect in useEffect when server redirect would work.

**Injection Method**:

```tsx
// Before (in Server Component or middleware)
import { redirect } from 'next/navigation'
if (!user) redirect('/login')

// After (in Client Component)
;('use client')
useEffect(() => {
  if (!user) router.push('/login')
}, [user])
```

**--comments**: `// ANTI-PATTERN: router-push-in-effect`
**--comments-hint**: `// Hint: Page renders before redirect, causing flash`
**--comments-fix**: `// Fix: Use server-side redirect() in page/layout or middleware for instant redirects`

**Fix**: Use server-side `redirect()` for auth checks and mandatory redirects.

---

### suspense-missing-fallback

- **Category**: rsc
- **Level**: semi-senior
- **Impact**: visual
- **Detectability**: moderate

**Anti-pattern**: Not wrapping async Server Components in Suspense, blocking entire page.

**Injection Method**:

```tsx
// Before
<Suspense fallback={<Skeleton />}>
  <AsyncDataComponent />
</Suspense>

// After
<AsyncDataComponent /> {/* Blocks parent until resolved */}
```

**--comments**: `// ANTI-PATTERN: suspense-missing-fallback`
**--comments-hint**: `// Hint: Async component blocks entire parent from rendering`
**--comments-fix**: `// Fix: Wrap in <Suspense fallback={<Loading />}> to stream content progressively`

**Fix**: Wrap async components in Suspense with appropriate loading fallback.
