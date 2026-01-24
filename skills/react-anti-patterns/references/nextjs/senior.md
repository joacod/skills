# Next.js Anti-Patterns - Senior Level

Advanced Next.js issues requiring deep knowledge of React Server Components, security practices, and performance optimization.

---

### server-action-no-auth

- **Category**: actions
- **Level**: senior
- **Impact**: security
- **Detectability**: hard

**Anti-pattern**: Server Actions without authentication/authorization checks.

**Injection Method**:

```tsx
// Before
'use server'
export async function deletePost(postId: string) {
  const session = await getSession()
  if (!session) throw new Error('Unauthorized')
  const post = await getPost(postId)
  if (post.authorId !== session.userId) throw new Error('Forbidden')
  await db.posts.delete(postId)
}

// After
;('use server')
export async function deletePost(postId: string) {
  await db.posts.delete(postId) // No auth check
}
```

**--comments**: `// ANTI-PATTERN: server-action-no-auth`
**--comments-hint**: `// Hint: Server Actions are public endpoints - anyone can call them`
**--comments-fix**: `// Fix: Always verify session and authorization before performing mutations`

**Fix**: Always verify authentication and authorization at the start of Server Actions.

---

### server-action-no-validation

- **Category**: actions
- **Level**: senior
- **Impact**: security
- **Detectability**: hard

**Anti-pattern**: Trust client input without validation in Server Actions.

**Injection Method**:

```tsx
// Before
'use server'
export async function updateProfile(data: unknown) {
  const validated = profileSchema.parse(data)
  await db.users.update(session.userId, validated)
}

// After
;('use server')
export async function updateProfile(data: { name: string; email: string }) {
  await db.users.update(session.userId, data) // Direct use
}
```

**--comments**: `// ANTI-PATTERN: server-action-no-validation`
**--comments-hint**: `// Hint: TypeScript types don't exist at runtime - input is untrusted`
**--comments-fix**: `// Fix: Use Zod or similar to validate all input at runtime before using`

**Fix**: Validate all Server Action inputs with Zod or similar runtime validation.

---

### over-serialization-props

- **Category**: boundary
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Pass large objects from Server to Client Components when only subset needed.

**Injection Method**:

```tsx
// Before
<ClientCard title={post.title} excerpt={post.excerpt} />

// After
<ClientCard post={post} /> {/* Serializes entire post object */}
```

**--comments**: `// ANTI-PATTERN: over-serialization-props`
**--comments-hint**: `// Hint: Full objects are serialized to JSON and sent to client`
**--comments-fix**: `// Fix: Pass only the specific fields needed to minimize serialization overhead`

**Fix**: Pass only necessary primitive values to Client Components.

---

### use-hook-in-server

- **Category**: boundary
- **Level**: senior
- **Impact**: build-error
- **Detectability**: hard

**Anti-pattern**: Accidentally use hooks in Server Components (often via imports).

**Injection Method**:

```tsx
// Before (Server Component without hooks)
export default async function Page() {
  const data = await getData()
  return <Display data={data} />
}

// After (introduces hook, will error)
export default async function Page() {
  const [filter, setFilter] = useState('all') // Error!
  const data = await getData()
  return <Display data={data} />
}
```

**--comments**: `// ANTI-PATTERN: use-hook-in-server`
**--comments-hint**: `// Hint: Hooks cannot be used in Server Components`
**--comments-fix**: `// Fix: Move interactive state to a Client Component child, keep data fetching in Server Component`

**Fix**: Extract interactive logic to Client Component children.

---

### revalidate-never-set

- **Category**: rsc
- **Level**: senior
- **Impact**: bug
- **Detectability**: hard

**Anti-pattern**: Not setting revalidation strategy for dynamic data, causing stale content.

**Injection Method**:

```tsx
// Before
export const revalidate = 60 // Revalidate every minute
// or: fetch(url, { next: { revalidate: 60 } })

// After
// No revalidate export, defaults to static or infinity
```

**--comments**: `// ANTI-PATTERN: revalidate-never-set`
**--comments-hint**: `// Hint: Without revalidation config, content may be cached indefinitely`
**--comments-fix**: `// Fix: Set revalidate export or use fetch cache options based on data freshness needs`

**Fix**: Explicitly set `revalidate` export or fetch cache options for dynamic content.

---

### generatestaticparams-missing

- **Category**: rsc
- **Level**: senior
- **Impact**: performance
- **Detectability**: hard

**Anti-pattern**: Dynamic routes without generateStaticParams when pages could be pre-rendered.

**Injection Method**:

```tsx
// Before
export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((post) => ({ slug: post.slug }))
}

// After
// No generateStaticParams - all pages render on-demand
```

**--comments**: `// ANTI-PATTERN: generatestaticparams-missing`
**--comments-hint**: `// Hint: Without static params, every page request hits the server`
**--comments-fix**: `// Fix: Add generateStaticParams to pre-render known pages at build time`

**Fix**: Implement `generateStaticParams` for dynamic routes with known paths.
