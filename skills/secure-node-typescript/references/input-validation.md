# Input Validation Guidelines

Validate and sanitize all external input to prevent injection attacks.

---

### schema-validation

- **Severity**: critical
- **OWASP**: A05 (Injection)

**Risk**: Unvalidated input can contain malicious payloads that exploit application logic or inject code.

**Secure Pattern**:

```typescript
// DO: Use Zod for type-safe validation
import { z } from 'zod'

const CreateUserSchema = z.object({
  email: z.string().email().max(254),
  password: z.string().min(12).max(128),
  name: z
    .string()
    .min(1)
    .max(100)
    .regex(/^[\p{L}\s'-]+$/u),
  age: z.number().int().min(0).max(150).optional(),
})

type CreateUserInput = z.infer<typeof CreateUserSchema>

// In Express route handler
app.post('/users', async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body)

  if (!result.success) {
    return res.status(400).json({
      error: 'Validation failed',
      details: result.error.issues.map((i) => ({
        path: i.path.join('.'),
        message: i.message,
      })),
    })
  }

  const validatedData: CreateUserInput = result.data
  // Safe to use validatedData
})
```

**Insecure Pattern**:

```typescript
// DON'T: Trust input without validation
app.post('/users', async (req, res) => {
  const { email, password, name } = req.body // Unvalidated!
  await createUser(email, password, name)
})
```

---

### allowlist-validation

- **Severity**: critical
- **OWASP**: A05 (Injection)

**Risk**: Blocklist (denylist) validation can be bypassed with new attack patterns. Allowlist validation only accepts known-good values.

**Secure Pattern**:

```typescript
// DO: Allowlist approach - only accept known-good values
const ALLOWED_SORT_FIELDS = ['name', 'email', 'createdAt'] as const
type SortField = (typeof ALLOWED_SORT_FIELDS)[number]

function isSortField(value: unknown): value is SortField {
  return (
    typeof value === 'string' &&
    ALLOWED_SORT_FIELDS.includes(value as SortField)
  )
}

const QuerySchema = z.object({
  sortBy: z.enum(ALLOWED_SORT_FIELDS).optional().default('createdAt'),
  order: z.enum(['asc', 'desc']).optional().default('asc'),
  limit: z.number().int().min(1).max(100).optional().default(20),
})

// DO: Validate file extensions with allowlist
const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif'] as const

function isAllowedExtension(filename: string): boolean {
  const ext = path.extname(filename).toLowerCase()
  return ALLOWED_EXTENSIONS.includes(ext as (typeof ALLOWED_EXTENSIONS)[number])
}
```

**Insecure Pattern**:

```typescript
// DON'T: Blocklist approach - can always be bypassed
const BLOCKED_EXTENSIONS = ['.exe', '.bat', '.sh']

function isBlockedExtension(filename: string): boolean {
  const ext = path.extname(filename).toLowerCase()
  return BLOCKED_EXTENSIONS.includes(ext) // Misses .cmd, .ps1, .jar, etc.
}

// DON'T: Use user input directly in queries
const sortBy = req.query.sortBy // Could be "1; DROP TABLE users--"
const query = `SELECT * FROM users ORDER BY ${sortBy}`
```

---

### sanitize-outputs

- **Severity**: critical
- **OWASP**: A05 (Injection)

**Risk**: Unsanitized output can execute malicious code in different contexts (HTML, SQL, shell, etc.).

**Secure Pattern**:

```typescript
// DO: Context-aware output encoding
import { escape as escapeHtml } from 'lodash'

// HTML context - prevent XSS
function renderUserName(name: string): string {
  return escapeHtml(name)
}

// SQL context - use parameterized queries
async function findUser(email: string): Promise<User | null> {
  const result = await db.query('SELECT * FROM users WHERE email = $1', [email])
  return result.rows[0] ?? null
}

// Shell context - avoid if possible, escape if necessary
import { spawn } from 'node:child_process'

function runCommand(filename: string): void {
  // DO: Use spawn with arguments array (no shell interpretation)
  const sanitizedFilename = filename.replace(/[^a-zA-Z0-9._-]/g, '')
  spawn('convert', [sanitizedFilename, '-resize', '100x100', 'output.jpg'])
}

// JSON context - ensure proper serialization
function sendJsonResponse(res: Response, data: unknown): void {
  res.setHeader('Content-Type', 'application/json')
  res.send(JSON.stringify(data)) // JSON.stringify handles encoding
}
```

**Insecure Pattern**:

```typescript
// DON'T: Direct string interpolation in HTML
const html = `<h1>Welcome, ${userName}</h1>` // XSS if userName contains <script>

// DON'T: String concatenation in SQL
const query = `SELECT * FROM users WHERE email = '${email}'` // SQL injection

// DON'T: Shell command with user input
exec(`convert ${filename} -resize 100x100 output.jpg`) // Command injection
```

---

### body-size-limit

- **Severity**: high
- **OWASP**: A02 (Security Misconfiguration)

**Risk**: Unlimited request body size allows denial-of-service attacks through memory exhaustion.

**Secure Pattern**:

```typescript
import express from 'express'

const app = express()

// DO: Set strict body limits based on expected payload size
app.use(express.json({ limit: '1kb' })) // For small JSON APIs
app.use(express.urlencoded({ extended: true, limit: '1kb' }))

// DO: Different limits for different routes
const smallJsonParser = express.json({ limit: '1kb' })
const largeJsonParser = express.json({ limit: '100kb' })

app.post('/api/login', smallJsonParser, loginHandler)
app.post('/api/upload-metadata', largeJsonParser, uploadHandler)

// DO: Limit file uploads separately
import multer from 'multer'

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB
    files: 1,
    fields: 10,
  },
})
```

**Insecure Pattern**:

```typescript
// DON'T: No body limit (default is 100kb, but explicit is better)
app.use(express.json())

// DON'T: Excessively large limits
app.use(express.json({ limit: '50mb' }))
```

---

### content-type-check

- **Severity**: medium
- **OWASP**: A02 (Security Misconfiguration)

**Risk**: Accepting mismatched Content-Type headers can lead to parser confusion attacks and CSRF bypasses.

**Secure Pattern**:

```typescript
import express from 'express'

// DO: Strict Content-Type checking middleware
function requireContentType(expectedType: string): express.RequestHandler {
  return (req, res, next) => {
    const contentType = req.get('Content-Type')

    if (!contentType || !contentType.includes(expectedType)) {
      return res.status(415).json({
        error: 'Unsupported Media Type',
        expected: expectedType,
      })
    }

    next()
  }
}

// Apply to JSON routes
app.post(
  '/api/users',
  requireContentType('application/json'),
  express.json({ limit: '1kb' }),
  createUserHandler,
)

// DO: Use type-is for more flexible checking
import typeIs from 'type-is'

function requireJsonOrForm(req: Request, res: Response, next: NextFunction) {
  if (!typeIs(req, ['json', 'urlencoded'])) {
    return res.status(415).json({ error: 'Unsupported Media Type' })
  }
  next()
}
```

**Insecure Pattern**:

```typescript
// DON'T: Parse body without checking Content-Type
app.use(express.json()) // Parses anything claiming to be JSON
app.post('/api/data', (req, res) => {
  // Body could be from form submission (CSRF) parsed as JSON
})
```

---

### url-validation

- **Severity**: high
- **OWASP**: A01 (Broken Access Control - SSRF)

**Risk**: User-supplied URLs can be used to access internal services, cloud metadata endpoints, or sensitive resources (Server-Side Request Forgery).

**Secure Pattern**:

```typescript
import { URL } from 'node:url'

// DO: Strict URL validation with allowlist
const ALLOWED_HOSTS = new Set(['api.example.com', 'cdn.example.com'])
const ALLOWED_PROTOCOLS = new Set(['https:'])

function validateExternalUrl(urlString: string): URL {
  let url: URL

  try {
    url = new URL(urlString)
  } catch {
    throw new Error('Invalid URL format')
  }

  // Check protocol
  if (!ALLOWED_PROTOCOLS.has(url.protocol)) {
    throw new Error(`Protocol not allowed: ${url.protocol}`)
  }

  // Check hostname against allowlist
  if (!ALLOWED_HOSTS.has(url.hostname)) {
    throw new Error(`Host not allowed: ${url.hostname}`)
  }

  // Block private IP ranges
  if (isPrivateHost(url.hostname)) {
    throw new Error('Private hosts not allowed')
  }

  return url
}

function isPrivateHost(hostname: string): boolean {
  // Check for localhost variants
  if (
    hostname === 'localhost' ||
    hostname === '127.0.0.1' ||
    hostname === '::1' ||
    hostname === '0.0.0.0'
  ) {
    return true
  }

  // Check for internal DNS names
  if (hostname.endsWith('.internal') || hostname.endsWith('.local')) {
    return true
  }

  // Check for cloud metadata endpoints
  if (
    hostname === '169.254.169.254' ||
    hostname === 'metadata.google.internal'
  ) {
    return true
  }

  return false
}
```

**Insecure Pattern**:

```typescript
// DON'T: Fetch user-supplied URLs without validation
app.get('/proxy', async (req, res) => {
  const url = req.query.url as string
  const response = await fetch(url) // SSRF vulnerability!
  res.send(await response.text())
})
```

---

### json-schema-validation

- **Severity**: high
- **OWASP**: A05 (Injection)

**Risk**: Complex nested payloads can contain unexpected fields that bypass validation or cause prototype pollution.

**Secure Pattern**:

```typescript
import { z } from 'zod'

// DO: Define strict schemas that reject extra fields
const AddressSchema = z
  .object({
    street: z.string().max(200),
    city: z.string().max(100),
    country: z.string().length(2), // ISO country code
    postalCode: z.string().max(20),
  })
  .strict() // Rejects unknown keys

const OrderSchema = z
  .object({
    items: z
      .array(
        z
          .object({
            productId: z.string().uuid(),
            quantity: z.number().int().min(1).max(99),
          })
          .strict(),
      )
      .min(1)
      .max(50),
    shippingAddress: AddressSchema,
    notes: z.string().max(500).optional(),
  })
  .strict()

// DO: Validate and strip unknown fields for lenient parsing
const LenientOrderSchema = OrderSchema.strip() // Removes unknown keys instead of rejecting

// DO: Prevent prototype pollution in JSON parsing
function safeJsonParse<T>(json: string, schema: z.ZodSchema<T>): T {
  const parsed = JSON.parse(json, (key, value) => {
    // Block prototype pollution attempts
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      return undefined
    }
    return value
  })

  return schema.parse(parsed)
}
```

**Insecure Pattern**:

```typescript
// DON'T: Parse JSON without validation
const data = JSON.parse(req.body) // Could contain __proto__
Object.assign(target, data) // Prototype pollution!

// DON'T: Allow extra fields
const schema = z.object({ name: z.string() }) // Allows any extra fields by default
```
