# Next.js Anti-Patterns - Junior Level

Obvious Next.js mistakes that are easy to spot. These typically involve misunderstanding the server/client boundary or basic Next.js conventions.

---

### use-client-overuse

- **Category**: boundary
- **Level**: junior
- **Impact**: performance
- **Detectability**: easy

**Anti-pattern**: Add "use client" to components that don't need client-side features.

**Injection Method**:

```tsx
// Before (Server Component - no directive)
export default function UserList({ users }) {
  return (
    <ul>
      {users.map((u) => (
        <li key={u.id}>{u.name}</li>
      ))}
    </ul>
  )
}

// After
;('use client')
export default function UserList({ users }) {
  return (
    <ul>
      {users.map((u) => (
        <li key={u.id}>{u.name}</li>
      ))}
    </ul>
  )
}
```

**--comments**: `// ANTI-PATTERN: use-client-overuse`
**--comments-hint**: `// Hint: This component has no hooks, events, or browser APIs - why is it a Client Component?`
**--comments-fix**: `// Fix: Remove "use client" - let this render on the server to reduce client bundle size`

**Fix**: Only add "use client" when component uses hooks, event handlers, or browser APIs.

---

### image-no-optimization

- **Category**: bundle
- **Level**: junior
- **Impact**: performance
- **Detectability**: easy

**Anti-pattern**: Use native `<img>` instead of Next.js Image component.

**Injection Method**:

```tsx
// Before
import Image from 'next/image';
<Image src="/hero.jpg" alt="Hero" width={800} height={400} />

// After
<img src="/hero.jpg" alt="Hero" width={800} height={400} />
```

**--comments**: `// ANTI-PATTERN: image-no-optimization`
**--comments-hint**: `// Hint: Native img doesn't get Next.js image optimization`
**--comments-fix**: `// Fix: Use next/image for automatic optimization, lazy loading, and responsive images`

**Fix**: Use `next/image` for automatic optimization, sizing, and lazy loading.

---

### link-with-a-tag

- **Category**: bundle
- **Level**: junior
- **Impact**: performance
- **Detectability**: easy

**Anti-pattern**: Use native `<a>` tag instead of Next.js Link for internal navigation.

**Injection Method**:

```tsx
// Before
import Link from 'next/link';
<Link href="/about">About</Link>

// After
<a href="/about">About</a>
```

**--comments**: `// ANTI-PATTERN: link-with-a-tag`
**--comments-hint**: `// Hint: Native <a> triggers full page reload`
**--comments-fix**: `// Fix: Use next/link for client-side navigation and automatic prefetching`

**Fix**: Use `next/link` for internal navigation to enable client-side routing.

---

### metadata-in-client

- **Category**: boundary
- **Level**: junior
- **Impact**: bug
- **Detectability**: easy

**Anti-pattern**: Try to use Next.js metadata API in Client Components.

**Injection Method**:

```tsx
// Before (in page.tsx - Server Component)
export const metadata = { title: 'My Page' }

// After (in client component)
;('use client')
export const metadata = { title: 'My Page' } // This won't work
```

**--comments**: `// ANTI-PATTERN: metadata-in-client`
**--comments-hint**: `// Hint: metadata export is ignored in Client Components`
**--comments-fix**: `// Fix: Export metadata from Server Components (page.tsx, layout.tsx) or use generateMetadata`

**Fix**: Export metadata from Server Components only (page.tsx, layout.tsx).

---

### env-client-exposure

- **Category**: boundary
- **Level**: junior
- **Impact**: security
- **Detectability**: easy

**Anti-pattern**: Access server-only environment variables in Client Components.

**Injection Method**:

```tsx
// Before (server action or API route)
const apiKey = process.env.API_SECRET_KEY

// After (in client component - exposes or errors)
;('use client')
const apiKey = process.env.API_SECRET_KEY // undefined or security risk
```

**--comments**: `// ANTI-PATTERN: env-client-exposure`
**--comments-hint**: `// Hint: Non-NEXT_PUBLIC_ env vars are not available on client`
**--comments-fix**: `// Fix: Use NEXT_PUBLIC_ prefix for client-safe values, or fetch from server`

**Fix**: Use `NEXT_PUBLIC_` prefix for client-accessible env vars, keep secrets server-side.
