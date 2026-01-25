# HTTP Security Guidelines

Secure HTTP headers, rate limiting, and request handling for web endpoints.

---

### helmet-middleware

- **Severity**: high
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Missing security headers leave applications vulnerable to XSS, clickjacking, MIME sniffing, and other browser-based attacks.

**Secure Pattern**:

```typescript
import helmet from 'helmet'
import express from 'express'

const app = express()

// DO: Use helmet with strict configuration
app.use(
  helmet({
    // Strict Transport Security - force HTTPS
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true,
    },
    // Content Security Policy
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"], // No 'unsafe-inline' or 'unsafe-eval'
        styleSrc: ["'self'", "'unsafe-inline'"], // inline styles often needed
        imgSrc: ["'self'", 'data:', 'https:'],
        fontSrc: ["'self'"],
        objectSrc: ["'none'"],
        frameAncestors: ["'none'"], // Prevent framing
        formAction: ["'self'"],
        baseUri: ["'self'"],
        upgradeInsecureRequests: [],
      },
    },
    // Prevent clickjacking
    frameguard: { action: 'deny' },
    // Prevent MIME type sniffing
    noSniff: true,
    // Referrer policy
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
    // Cross-Origin policies
    crossOriginEmbedderPolicy: true,
    crossOriginOpenerPolicy: { policy: 'same-origin' },
    crossOriginResourcePolicy: { policy: 'same-origin' },
  }),
)

// DO: Remove X-Powered-By header
app.disable('x-powered-by')
```

**Insecure Pattern**:

```typescript
// DON'T: Missing security headers
const app = express()
// No helmet, no security headers set

// DON'T: Overly permissive CSP
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ['*'], // Allows everything!
        scriptSrc: ["'unsafe-inline'", "'unsafe-eval'"], // XSS vulnerable
      },
    },
  }),
)
```

---

### csp-policy

- **Severity**: high
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Missing or permissive Content Security Policy allows XSS attacks by permitting execution of injected scripts.

**Secure Pattern**:

```typescript
// DO: Strict CSP with nonces for inline scripts
import crypto from 'node:crypto'
import helmet from 'helmet'

// Generate nonce per request
app.use((req, res, next) => {
  res.locals.cspNonce = crypto.randomBytes(16).toString('base64')
  next()
})

app.use((req, res, next) => {
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", `'nonce-${res.locals.cspNonce}'`],
      styleSrc: ["'self'", `'nonce-${res.locals.cspNonce}'`],
      imgSrc: ["'self'", 'data:'],
      fontSrc: ["'self'"],
      connectSrc: ["'self'", 'https://api.example.com'],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"],
      formAction: ["'self'"],
      baseUri: ["'self'"],
      reportUri: '/csp-report',
    },
  })(req, res, next)
})

// DO: Set up CSP violation reporting
app.post(
  '/csp-report',
  express.json({ type: 'application/csp-report' }),
  (req, res) => {
    console.warn('CSP Violation:', req.body)
    res.status(204).end()
  },
)

// In templates, use the nonce
// <script nonce="<%= cspNonce %>">...</script>
```

**Insecure Pattern**:

```typescript
// DON'T: Disable CSP or use unsafe directives
app.use(helmet({ contentSecurityPolicy: false }));

// DON'T: Allow unsafe-inline and unsafe-eval
contentSecurityPolicy: {
  directives: {
    scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
  },
},
```

---

### cors-configuration

- **Severity**: high
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Overly permissive CORS allows malicious websites to make authenticated requests on behalf of users.

**Secure Pattern**:

```typescript
import cors from 'cors'

// DO: Strict CORS with explicit origin allowlist
const ALLOWED_ORIGINS = new Set([
  'https://app.example.com',
  'https://admin.example.com',
])

const corsOptions: cors.CorsOptions = {
  origin: (origin, callback) => {
    // Allow requests with no origin (mobile apps, curl, etc.) only in specific cases
    if (!origin) {
      // Decide based on your security requirements
      return callback(null, false)
    }

    if (ALLOWED_ORIGINS.has(origin)) {
      return callback(null, true)
    }

    callback(new Error('Not allowed by CORS'))
  },
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true, // Only if cookies/auth needed
  maxAge: 86400, // Cache preflight for 24 hours
}

app.use(cors(corsOptions))

// DO: Apply stricter CORS to sensitive endpoints
const strictCors = cors({
  origin: 'https://app.example.com', // Single trusted origin
  credentials: true,
})

app.post('/api/admin/*', strictCors, adminRoutes)
```

**Insecure Pattern**:

```typescript
// DON'T: Allow all origins
app.use(cors({ origin: '*' })) // Open to all websites

// DON'T: Reflect origin without validation
app.use(
  cors({
    origin: (origin, callback) => callback(null, true), // Reflects any origin!
    credentials: true, // Especially dangerous with credentials
  }),
)

// DON'T: Allow credentials with wildcard origin
app.use(cors({ origin: '*', credentials: true })) // Browsers block this, but shows intent
```

---

### rate-limiting

- **Severity**: high
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Without rate limiting, attackers can perform brute-force attacks, credential stuffing, or denial-of-service.

**Secure Pattern**:

```typescript
import rateLimit from 'express-rate-limit'
import RedisStore from 'rate-limit-redis'
import { createClient } from 'redis'

const redisClient = createClient({ url: process.env.REDIS_URL })

// DO: Different rate limits for different endpoints
const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    sendCommand: (...args: string[]) => redisClient.sendCommand(args),
  }),
  message: { error: 'Too many requests, please try again later' },
})

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    sendCommand: (...args: string[]) => redisClient.sendCommand(args),
    prefix: 'rl:auth:',
  }),
  skipSuccessfulRequests: true, // Don't count successful logins
  message: { error: 'Too many login attempts, please try again later' },
})

const apiLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 30, // 30 requests per minute
  keyGenerator: (req) => req.user?.id || req.ip, // Per user or IP
  store: new RedisStore({
    sendCommand: (...args: string[]) => redisClient.sendCommand(args),
    prefix: 'rl:api:',
  }),
})

// Apply limiters
app.use(generalLimiter)
app.post('/auth/login', authLimiter, loginHandler)
app.use('/api/', apiLimiter)
```

**Insecure Pattern**:

```typescript
// DON'T: No rate limiting
app.post('/login', loginHandler) // Unlimited attempts allowed

// DON'T: In-memory rate limiting in clustered environment
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  // No store specified - uses memory, not shared between instances
})
```

---

### exponential-backoff

- **Severity**: medium
- **OWASP**: A07 (Authentication Failures)

**Risk**: Fixed delays allow attackers to calculate optimal attack rates. Exponential backoff makes brute-force impractical.

**Secure Pattern**:

```typescript
import { RateLimiterRedis } from 'rate-limiter-flexible'
import { createClient } from 'redis'

const redisClient = createClient({ url: process.env.REDIS_URL })

// DO: Implement exponential backoff for failed attempts
const loginLimiter = new RateLimiterRedis({
  storeClient: redisClient,
  keyPrefix: 'login_fail',
  points: 5, // 5 attempts
  duration: 60 * 15, // Per 15 minutes
  blockDuration: 60 * 15, // Block for 15 minutes when exceeded
})

async function handleLogin(req: Request, res: Response) {
  const ipKey = req.ip
  const emailKey = req.body.email

  try {
    // Check both IP and email limits
    await Promise.all([
      loginLimiter.consume(ipKey),
      loginLimiter.consume(emailKey),
    ])
  } catch (rateLimiterRes) {
    const retrySecs = Math.ceil(rateLimiterRes.msBeforeNext / 1000)
    res.set('Retry-After', String(retrySecs))
    return res.status(429).json({
      error: 'Too many attempts',
      retryAfter: retrySecs,
    })
  }

  const user = await authenticateUser(req.body.email, req.body.password)

  if (!user) {
    // Failed - consume points (already consumed above, but track for backoff)
    return res.status(401).json({ error: 'Invalid credentials' })
  }

  // Success - reset limits for this IP/email
  await Promise.all([loginLimiter.delete(ipKey), loginLimiter.delete(emailKey)])

  res.json({ token: createAccessToken(user) })
}

// DO: Implement account lockout after repeated failures
const LOCKOUT_THRESHOLD = 10
const LOCKOUT_DURATION = 60 * 60 * 1000 // 1 hour

async function checkAccountLockout(email: string): Promise<boolean> {
  const key = `lockout:${email}`
  const attempts = await redisClient.get(key)
  return parseInt(attempts || '0', 10) >= LOCKOUT_THRESHOLD
}
```

**Insecure Pattern**:

```typescript
// DON'T: Fixed delay that can be parallelized
async function handleLogin(req, res) {
  await sleep(1000) // Attacker can make parallel requests
  // ... authentication logic
}

// DON'T: No lockout mechanism
app.post('/login', async (req, res) => {
  const user = await authenticate(req.body) // Unlimited attempts
})
```

---

### hpp-middleware

- **Severity**: medium
- **OWASP**: A03 (Injection)

**Risk**: HTTP Parameter Pollution can bypass validation by sending duplicate parameters, causing the application to use unexpected values.

**Secure Pattern**:

```typescript
import hpp from 'hpp'
import express from 'express'

const app = express()

// DO: Use hpp middleware to prevent parameter pollution
app.use(hpp())

// DO: Whitelist parameters that legitimately accept arrays
app.use(
  hpp({
    whitelist: ['tags', 'ids', 'filters'], // These can be arrays
  }),
)

// DO: Manually validate array parameters when needed
app.get('/search', (req, res) => {
  // After hpp, req.query.sort will be a single value (last one wins)
  const sort = req.query.sort as string | undefined

  // For whitelisted array params, explicitly handle as array
  const tags = Array.isArray(req.query.tags)
    ? req.query.tags
    : req.query.tags
      ? [req.query.tags]
      : []

  // Validate each tag
  const validTags = tags.filter(
    (tag) => typeof tag === 'string' && tag.length < 50,
  )

  // ... use validated parameters
})
```

**Insecure Pattern**:

```typescript
// DON'T: Trust query parameters without hpp
app.get('/users', (req, res) => {
  // Attacker sends: /users?role=admin&role=user
  // req.query.role could be "admin" or ["admin", "user"] depending on framework
  const role = req.query.role // Unpredictable!

  if (role === 'user') {
    // Validation bypassed if role is array
  }
})
```

---

### disable-legacy-headers

- **Severity**: medium
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Legacy headers like X-Powered-By reveal technology stack information, aiding reconnaissance. X-XSS-Protection is deprecated and can introduce vulnerabilities.

**Secure Pattern**:

```typescript
import express from 'express'
import helmet from 'helmet'

const app = express()

// DO: Disable X-Powered-By
app.disable('x-powered-by')

// DO: Use helmet which handles this automatically
app.use(helmet())

// DO: Explicitly disable deprecated X-XSS-Protection
app.use((req, res, next) => {
  res.removeHeader('X-XSS-Protection') // Deprecated, can cause issues
  next()
})

// DO: Set custom Server header or remove it
app.use((req, res, next) => {
  res.setHeader('Server', '') // Empty or generic value
  next()
})
```

**Insecure Pattern**:

```typescript
// DON'T: Leave default headers that reveal stack info
// Response includes: X-Powered-By: Express

// DON'T: Use deprecated X-XSS-Protection
res.setHeader('X-XSS-Protection', '1; mode=block') // Can introduce vulnerabilities
```

---

### sri-hashes

- **Severity**: medium
- **OWASP**: A08 (Data Integrity Failures)

**Risk**: Without Subresource Integrity, compromised CDNs or MITM attacks can serve malicious scripts that execute in users' browsers.

**Secure Pattern**:

```typescript
// DO: Use SRI hashes for external scripts
const SCRIPT_HASHES = {
  'https://cdn.example.com/lib.js':
    'sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC',
}

function renderScriptTag(src: string): string {
  const integrity = SCRIPT_HASHES[src]

  if (integrity) {
    return `<script src="${src}" integrity="${integrity}" crossorigin="anonymous"></script>`
  }

  // For first-party scripts, no SRI needed if same-origin
  return `<script src="${src}"></script>`
}

// DO: Generate SRI hashes at build time
import crypto from 'node:crypto'
import { readFileSync } from 'node:fs'

function generateSriHash(filePath: string): string {
  const content = readFileSync(filePath)
  const hash = crypto.createHash('sha384').update(content).digest('base64')
  return `sha384-${hash}`
}

// DO: Use require-sri-for CSP directive (deprecated but still useful)
// contentSecurityPolicy: {
//   directives: {
//     requireSriFor: ["script", "style"],
//   },
// }
```

**Insecure Pattern**:

```html
<!-- DON'T: Load external scripts without SRI -->
<script src="https://cdn.example.com/jquery.min.js"></script>

<!-- DON'T: Use SRI with http:// (MITM can strip it) -->
<script src="http://cdn.example.com/lib.js" integrity="sha384-..."></script>
```
