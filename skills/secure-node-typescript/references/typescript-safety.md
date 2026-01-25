# TypeScript Safety Guidelines

Use TypeScript's type system to catch security issues at compile time.

---

### strict-typescript

- **Severity**: high
- **OWASP**: A06 (Insecure Design)

**Risk**: Disabled strict mode allows implicit any types, null reference errors, and type coercion bugs that can lead to runtime security vulnerabilities.

**Secure Pattern**:

```json
// tsconfig.json - Enable all strict checks
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "alwaysStrict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true
  }
}
```

**Insecure Pattern**:

```json
// DON'T: Permissive compiler settings
{
  "compilerOptions": {
    "strict": false,
    "noImplicitAny": false
  }
}
```

---

### no-any-type

- **Severity**: high
- **OWASP**: A06 (Insecure Design)

**Risk**: The `any` type bypasses all type checking, allowing unsafe operations and defeating TypeScript's security benefits.

**Secure Pattern**:

```typescript
// DO: Use unknown with type guards for dynamic data
function processInput(data: unknown): string {
  if (typeof data === 'string') {
    return data.trim()
  }
  if (typeof data === 'object' && data !== null && 'value' in data) {
    const obj = data as { value: unknown }
    if (typeof obj.value === 'string') {
      return obj.value
    }
  }
  throw new Error('Invalid input type')
}

// DO: Use generics for flexible but type-safe code
function parseResponse<T>(
  response: unknown,
  validator: (v: unknown) => v is T,
): T {
  if (validator(response)) {
    return response
  }
  throw new Error('Invalid response format')
}
```

**Insecure Pattern**:

```typescript
// DON'T: Using any defeats type safety
function processInput(data: any): string {
  return data.value.trim() // Runtime error if structure differs
}
```

---

### access-modifiers

- **Severity**: medium
- **OWASP**: A01 (Broken Access Control)

**Risk**: Without access modifiers, sensitive methods and data can be accessed from anywhere in the codebase.

**Secure Pattern**:

```typescript
// DO: Restrict access to sensitive members
class UserService {
  private readonly secretKey: string
  private passwordHasher: PasswordHasher

  protected async hashPassword(password: string): Promise<string> {
    return this.passwordHasher.hash(password)
  }

  public async createUser(email: string, password: string): Promise<User> {
    const hashedPassword = await this.hashPassword(password)
    // ...create user logic
  }
}
```

**Insecure Pattern**:

```typescript
// DON'T: All members publicly accessible
class UserService {
  secretKey: string // Exposed!
  passwordHasher: PasswordHasher

  hashPassword(password: string): Promise<string> {
    return this.passwordHasher.hash(password)
  }
}
```

---

### readonly-properties

- **Severity**: medium
- **OWASP**: A06 (Insecure Design)

**Risk**: Mutable properties can be accidentally or maliciously modified, leading to state corruption or security bypasses.

**Secure Pattern**:

```typescript
// DO: Use readonly for immutable data
interface UserConfig {
  readonly userId: string
  readonly permissions: readonly string[]
  readonly createdAt: Date
}

class SecurityContext {
  private readonly _user: UserConfig

  constructor(user: UserConfig) {
    this._user = Object.freeze({ ...user })
  }

  get user(): UserConfig {
    return this._user
  }
}

// DO: Use const assertions for literal types
const ALLOWED_ROLES = ['admin', 'user', 'guest'] as const
type Role = (typeof ALLOWED_ROLES)[number]
```

**Insecure Pattern**:

```typescript
// DON'T: Mutable security-critical properties
interface UserConfig {
  userId: string
  permissions: string[] // Can be modified!
}

const config: UserConfig = { userId: '123', permissions: ['read'] }
config.permissions.push('admin') // Privilege escalation!
```

---

### node-protocol-imports

- **Severity**: medium
- **OWASP**: A03 (Software Supply Chain Failures)

**Risk**: Without the `node:` protocol prefix, Node.js built-in modules can be shadowed by malicious npm packages with the same name (typosquatting).

**Secure Pattern**:

```typescript
// DO: Always use node: protocol for built-ins
import { createServer } from 'node:http'
import { readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'
import crypto from 'node:crypto'
import { Buffer } from 'node:buffer'
import { EventEmitter } from 'node:events'
import { spawn } from 'node:child_process'
```

**Insecure Pattern**:

```typescript
// DON'T: Ambiguous imports could resolve to malicious packages
import { createServer } from 'http'
import { readFile } from 'fs/promises'
import path from 'path'
import crypto from 'crypto' // Could be npm package "crypto"!
```

---

### freeze-globals

- **Severity**: medium
- **OWASP**: A05 (Injection)

**Risk**: Unfrozen global objects can be modified through prototype pollution attacks, allowing attackers to inject malicious properties.

**Secure Pattern**:

```typescript
// DO: Freeze global objects early in application startup
// Place at the top of your main entry file

Object.freeze(Object.prototype)
Object.freeze(Array.prototype)
Object.freeze(Function.prototype)

// For maximum protection (may break some libraries)
// Object.freeze(globalThis);

// DO: Create frozen configuration objects
const APP_CONFIG = Object.freeze({
  maxRetries: 3,
  timeout: 5000,
  allowedOrigins: Object.freeze(['https://example.com']),
})
```

**Insecure Pattern**:

```typescript
// DON'T: Allow prototype modification
const userInput = JSON.parse(untrustedJson)
// If untrustedJson contains {"__proto__": {"isAdmin": true}}
// Object.prototype is now polluted!

const user = {}
console.log(user.isAdmin) // true - from polluted prototype!
```

---

### typed-async-functions

- **Severity**: medium
- **OWASP**: A06 (Insecure Design)

**Risk**: Untyped async functions can return unexpected types, leading to runtime errors and potential security issues when handling responses.

**Secure Pattern**:

```typescript
// DO: Explicitly type async function returns
interface User {
  id: string
  email: string
}

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`)
  }
  const data: unknown = await response.json()
  return validateUser(data) // Returns typed User or throws
}

// DO: Type error handling
async function safeOperation<T>(
  operation: () => Promise<T>,
  fallback: T,
): Promise<T> {
  try {
    return await operation()
  } catch (error) {
    console.error('Operation failed:', error)
    return fallback
  }
}
```

**Insecure Pattern**:

```typescript
// DON'T: Missing return type allows any shape
async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`)
  return response.json() // Returns Promise<any>
}

// Later code assumes wrong structure
const user = await fetchUser('123')
console.log(user.permissions.admin) // Runtime error!
```

---

### typed-config

- **Severity**: medium
- **OWASP**: A02 (Security Misconfiguration)

**Risk**: Untyped configuration objects can contain incorrect values or missing required fields, leading to security misconfigurations.

**Secure Pattern**:

```typescript
// DO: Define strict configuration interfaces
interface DatabaseConfig {
  readonly host: string
  readonly port: number
  readonly database: string
  readonly ssl: boolean
  readonly poolSize: number
}

interface AppConfig {
  readonly database: DatabaseConfig
  readonly jwtSecret: string
  readonly corsOrigins: readonly string[]
  readonly rateLimitWindow: number
  readonly rateLimitMax: number
}

// DO: Validate configuration at startup
function loadConfig(): AppConfig {
  const config: AppConfig = {
    database: {
      host: requireEnv('DB_HOST'),
      port: parseInt(requireEnv('DB_PORT'), 10),
      database: requireEnv('DB_NAME'),
      ssl: process.env.DB_SSL === 'true',
      poolSize: parseInt(process.env.DB_POOL_SIZE ?? '10', 10),
    },
    jwtSecret: requireEnv('JWT_SECRET'),
    corsOrigins: requireEnv('CORS_ORIGINS').split(','),
    rateLimitWindow: parseInt(process.env.RATE_LIMIT_WINDOW ?? '60000', 10),
    rateLimitMax: parseInt(process.env.RATE_LIMIT_MAX ?? '100', 10),
  }

  return Object.freeze(config)
}

function requireEnv(key: string): string {
  const value = process.env[key]
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`)
  }
  return value
}
```

**Insecure Pattern**:

```typescript
// DON'T: Untyped configuration
const config = {
  database: process.env.DB_HOST, // Could be undefined
  port: process.env.PORT, // String, not number
  secret: 'hardcoded', // Exposed secret
}
```
