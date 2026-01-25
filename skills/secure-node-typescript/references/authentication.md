# Authentication Guidelines

Secure authentication, authorization, sessions, and secrets management.

---

### argon2-hashing

- **Severity**: critical
- **OWASP**: A04 (Cryptographic Failures), A07 (Identification & Authentication Failures)

**Risk**: Weak password hashing (MD5, SHA1, bcrypt with low cost) allows offline brute-force attacks if the database is compromised.

**Secure Pattern**:

```typescript
import argon2 from 'argon2'

// DO: Use argon2id with secure parameters
const ARGON2_OPTIONS: argon2.Options = {
  type: argon2.argon2id, // Hybrid mode - best for passwords
  memoryCost: 65536, // 64 MB memory
  timeCost: 3, // 3 iterations
  parallelism: 4, // 4 parallel threads
}

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, ARGON2_OPTIONS)
}

async function verifyPassword(
  password: string,
  hash: string,
): Promise<boolean> {
  try {
    return await argon2.verify(hash, password)
  } catch {
    return false // Invalid hash format
  }
}

// DO: Rehash if parameters have been upgraded
async function verifyAndRehash(
  password: string,
  hash: string,
): Promise<{ valid: boolean; newHash?: string }> {
  const valid = await verifyPassword(password, hash)

  if (valid && argon2.needsRehash(hash, ARGON2_OPTIONS)) {
    const newHash = await hashPassword(password)
    return { valid: true, newHash }
  }

  return { valid }
}
```

**Insecure Pattern**:

```typescript
// DON'T: Weak hashing algorithms
import crypto from 'node:crypto'

function hashPassword(password: string): string {
  return crypto.createHash('sha256').update(password).digest('hex') // Too fast!
}

// DON'T: bcrypt with low cost factor
import bcrypt from 'bcrypt'
const hash = await bcrypt.hash(password, 4) // Cost factor too low
```

---

### secure-cookies

- **Severity**: critical
- **OWASP**: A07 (Identification & Authentication Failures)

**Risk**: Insecure cookie settings allow session hijacking through XSS, network interception, or CSRF attacks.

**Secure Pattern**:

```typescript
import session from 'express-session'
import RedisStore from 'connect-redis'
import { createClient } from 'redis'

// DO: Configure secure session cookies
const redisClient = createClient({ url: process.env.REDIS_URL })
await redisClient.connect()

app.use(
  session({
    store: new RedisStore({ client: redisClient }),
    name: '__Host-sessionId', // __Host- prefix enforces Secure + Path=/
    secret: process.env.SESSION_SECRET!,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true, // HTTPS only
      httpOnly: true, // Not accessible via JavaScript
      sameSite: 'strict', // Strict CSRF protection
      maxAge: 15 * 60 * 1000, // 15 minutes
      path: '/',
      domain: undefined, // Don't set domain - uses current host
    },
  }),
)

// DO: Regenerate session ID after authentication
app.post('/login', async (req, res) => {
  const user = await authenticateUser(req.body)

  if (user) {
    // Regenerate to prevent session fixation
    req.session.regenerate((err) => {
      if (err) {
        return res.status(500).json({ error: 'Session error' })
      }
      req.session.userId = user.id
      req.session.save(() => {
        res.json({ success: true })
      })
    })
  }
})
```

**Insecure Pattern**:

```typescript
// DON'T: Insecure cookie settings
app.use(
  session({
    secret: 'keyboard cat', // Weak secret
    cookie: {
      secure: false, // Transmitted over HTTP
      httpOnly: false, // Accessible via JavaScript (XSS)
      sameSite: 'none', // No CSRF protection
    },
  }),
)
```

---

### jwt-validation

- **Severity**: critical
- **OWASP**: A07 (Identification & Authentication Failures)

**Risk**: Improper JWT validation can allow token forgery, algorithm confusion attacks, or use of expired/revoked tokens.

**Secure Pattern**:

```typescript
import jwt from 'jsonwebtoken'
import { z } from 'zod'

// DO: Define strict token payload schema
const TokenPayloadSchema = z.object({
  sub: z.string().uuid(),
  email: z.string().email(),
  roles: z.array(z.string()),
  iat: z.number(),
  exp: z.number(),
})

type TokenPayload = z.infer<typeof TokenPayloadSchema>

interface JwtConfig {
  secret: string
  issuer: string
  audience: string
  expiresIn: string
}

const jwtConfig: JwtConfig = {
  secret: process.env.JWT_SECRET!,
  issuer: 'https://api.example.com',
  audience: 'https://example.com',
  expiresIn: '15m',
}

// DO: Sign with explicit algorithm
function signToken(payload: Omit<TokenPayload, 'iat' | 'exp'>): string {
  return jwt.sign(payload, jwtConfig.secret, {
    algorithm: 'HS256', // Explicitly set algorithm
    expiresIn: jwtConfig.expiresIn,
    issuer: jwtConfig.issuer,
    audience: jwtConfig.audience,
  })
}

// DO: Verify with strict options
function verifyToken(token: string): TokenPayload {
  const decoded = jwt.verify(token, jwtConfig.secret, {
    algorithms: ['HS256'], // Only allow expected algorithm
    issuer: jwtConfig.issuer,
    audience: jwtConfig.audience,
    complete: false,
  })

  // Validate payload structure
  return TokenPayloadSchema.parse(decoded)
}

// DO: Implement token blocklist for logout/revocation
const tokenBlocklist = new Set<string>()

async function isTokenRevoked(jti: string): Promise<boolean> {
  return tokenBlocklist.has(jti)
}

async function revokeToken(jti: string): Promise<void> {
  tokenBlocklist.add(jti)
  // In production, use Redis with TTL matching token expiry
}
```

**Insecure Pattern**:

```typescript
// DON'T: Verify without algorithm restriction
const decoded = jwt.verify(token, secret) // Allows alg:none attack!

// DON'T: Decode without verification
const decoded = jwt.decode(token) // Never use for authentication!

// DON'T: Use weak secrets
const token = jwt.sign(payload, 'secret123')
```

---

### rbac-implementation

- **Severity**: high
- **OWASP**: A01 (Broken Access Control)

**Risk**: Missing or incorrect authorization checks allow users to access resources or perform actions they shouldn't.

**Secure Pattern**:

```typescript
// DO: Define roles and permissions with types
const PERMISSIONS = {
  'users:read': true,
  'users:write': true,
  'users:delete': true,
  'admin:access': true,
} as const

type Permission = keyof typeof PERMISSIONS

const ROLE_PERMISSIONS: Record<string, readonly Permission[]> = {
  admin: ['users:read', 'users:write', 'users:delete', 'admin:access'],
  editor: ['users:read', 'users:write'],
  viewer: ['users:read'],
} as const

// DO: Create middleware for permission checks
function requirePermission(permission: Permission): RequestHandler {
  return (req, res, next) => {
    const user = req.user

    if (!user) {
      return res.status(401).json({ error: 'Authentication required' })
    }

    const userPermissions = ROLE_PERMISSIONS[user.role] ?? []

    if (!userPermissions.includes(permission)) {
      return res.status(403).json({ error: 'Insufficient permissions' })
    }

    next()
  }
}

// DO: Check ownership for resource-level access
async function requireOwnership(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const resourceId = req.params.id
  const userId = req.user?.id

  const resource = await getResource(resourceId)

  if (!resource) {
    return res.status(404).json({ error: 'Not found' })
  }

  if (resource.ownerId !== userId && req.user?.role !== 'admin') {
    return res.status(403).json({ error: 'Access denied' })
  }

  req.resource = resource
  next()
}

// Apply to routes
app.get('/users', requirePermission('users:read'), listUsers)
app.delete(
  '/users/:id',
  requirePermission('users:delete'),
  requireOwnership,
  deleteUser,
)
```

**Insecure Pattern**:

```typescript
// DON'T: Check authorization only on frontend
app.delete('/users/:id', async (req, res) => {
  await deleteUser(req.params.id) // No authorization check!
})

// DON'T: Role check without permission granularity
if (user.role === 'admin' || user.role === 'editor') {
  // Too coarse - editor shouldn't delete
}
```

---

### mfa-support

- **Severity**: high
- **OWASP**: A07 (Identification & Authentication Failures)

**Risk**: Single-factor authentication is vulnerable to credential stuffing, phishing, and password reuse attacks.

**Secure Pattern**:

```typescript
import { authenticator } from 'otplib'
import QRCode from 'qrcode'

// DO: Generate TOTP secret for user enrollment
async function enrollMfa(
  userId: string,
): Promise<{ secret: string; qrCode: string }> {
  const secret = authenticator.generateSecret()
  const otpauth = authenticator.keyuri(userId, 'MyApp', secret)
  const qrCode = await QRCode.toDataURL(otpauth)

  // Store secret encrypted, marked as unverified
  await storeMfaSecret(userId, secret, { verified: false })

  return { secret, qrCode }
}

// DO: Verify TOTP with time window tolerance
function verifyTotp(token: string, secret: string): boolean {
  // Allow 1 step (30 seconds) window for clock drift
  return authenticator.verify({ token, secret })
}

// DO: Require MFA verification to complete enrollment
async function confirmMfaEnrollment(
  userId: string,
  token: string,
): Promise<boolean> {
  const mfaData = await getMfaSecret(userId)

  if (!mfaData || mfaData.verified) {
    return false
  }

  if (!verifyTotp(token, mfaData.secret)) {
    return false
  }

  await markMfaVerified(userId)
  return true
}

// DO: Implement backup codes
function generateBackupCodes(): string[] {
  const codes: string[] = []
  for (let i = 0; i < 10; i++) {
    codes.push(crypto.randomBytes(4).toString('hex').toUpperCase())
  }
  return codes
}
```

**Insecure Pattern**:

```typescript
// DON'T: Store MFA secrets in plain text
await db.query('INSERT INTO users (mfa_secret) VALUES ($1)', [secret])

// DON'T: Skip rate limiting on MFA verification
app.post('/verify-mfa', async (req, res) => {
  const valid = verifyTotp(req.body.token, user.secret) // Brute-forceable!
})
```

---

### env-variables

- **Severity**: critical
- **OWASP**: A04 (Cryptographic Failures)

**Risk**: Hardcoded secrets in source code can be exposed through version control, logs, or error messages.

**Secure Pattern**:

```typescript
// DO: Use dotenv-safe to ensure required variables exist
import 'dotenv-safe/config' // Throws if .env.example vars are missing

// DO: Validate required environment variables at startup
interface EnvConfig {
  DATABASE_URL: string
  JWT_SECRET: string
  SESSION_SECRET: string
  REDIS_URL: string
  NODE_ENV: 'development' | 'production' | 'test'
}

function loadEnvConfig(): EnvConfig {
  const required = ['DATABASE_URL', 'JWT_SECRET', 'SESSION_SECRET', 'REDIS_URL']

  for (const key of required) {
    if (!process.env[key]) {
      throw new Error(`Missing required environment variable: ${key}`)
    }
  }

  // Validate secret strength
  if (process.env.JWT_SECRET!.length < 32) {
    throw new Error('JWT_SECRET must be at least 32 characters')
  }

  return {
    DATABASE_URL: process.env.DATABASE_URL!,
    JWT_SECRET: process.env.JWT_SECRET!,
    SESSION_SECRET: process.env.SESSION_SECRET!,
    REDIS_URL: process.env.REDIS_URL!,
    NODE_ENV: (process.env.NODE_ENV as EnvConfig['NODE_ENV']) || 'development',
  }
}

const config = loadEnvConfig()
```

**Insecure Pattern**:

```typescript
// DON'T: Hardcode secrets
const JWT_SECRET = 'my-super-secret-key'

// DON'T: Use weak or default secrets
const secret = process.env.SECRET || 'default-secret' // Fallback is dangerous

// DON'T: Log environment variables
console.log('Config:', process.env) // Exposes secrets in logs!
```

---

### secret-management

- **Severity**: critical
- **OWASP**: A04 (Cryptographic Failures)

**Risk**: Secrets stored in files or environment variables can be leaked through container images, backups, or process listings.

**Secure Pattern**:

```typescript
// DO: Use secret management services in production
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from '@aws-sdk/client-secrets-manager'

const secretsClient = new SecretsManagerClient({ region: 'us-east-1' })

async function getSecret(secretId: string): Promise<string> {
  const command = new GetSecretValueCommand({ SecretId: secretId })
  const response = await secretsClient.send(command)

  if (!response.SecretString) {
    throw new Error(`Secret ${secretId} not found or empty`)
  }

  return response.SecretString
}

// DO: Cache secrets with TTL for performance
const secretCache = new Map<string, { value: string; expiry: number }>()
const CACHE_TTL = 5 * 60 * 1000 // 5 minutes

async function getCachedSecret(secretId: string): Promise<string> {
  const cached = secretCache.get(secretId)

  if (cached && cached.expiry > Date.now()) {
    return cached.value
  }

  const value = await getSecret(secretId)
  secretCache.set(secretId, { value, expiry: Date.now() + CACHE_TTL })

  return value
}

// DO: Rotate secrets gracefully
async function rotateJwtSecret(): Promise<void> {
  const newSecret = await getSecret('jwt-secret-v2')
  // Keep old secret for verifying existing tokens during transition
  jwtConfig.secrets = [newSecret, jwtConfig.secrets[0]]
}
```

**Insecure Pattern**:

```typescript
// DON'T: Store secrets in code or config files committed to git
const config = {
  dbPassword: 'production-password-123',
  apiKey: 'sk-live-abc123',
}

// DON'T: Pass secrets via command line arguments
// $ node app.js --db-password=secret123
// Visible in process listings!
```

---

### typed-tokens

- **Severity**: medium
- **OWASP**: A07 (Identification & Authentication Failures)

**Risk**: Untyped token payloads can lead to incorrect assumptions about token contents, causing authorization bugs.

**Secure Pattern**:

```typescript
// DO: Define strict interfaces for all token types
interface AccessTokenPayload {
  type: "access";
  sub: string; // User ID
  email: string;
  roles: string[];
  permissions: string[];
}

interface RefreshTokenPayload {
  type: "refresh";
  sub: string;
  tokenFamily: string; // For refresh token rotation
}

interface PasswordResetTokenPayload {
  type: "password_reset";
  sub: string;
  email: string;
}

type TokenPayload = AccessTokenPayload | RefreshTokenPayload | PasswordResetTokenPayload;

// DO: Type-safe token verification
function verifyAccessToken(token: string): AccessTokenPayload {
  const payload = verifyToken(token);

  if (payload.type !== "access") {
    throw new Error("Invalid token type");
  }

  return payload as AccessTokenPayload;
}

// DO: Branded types for different token strings
declare const AccessTokenBrand: unique symbol;
declare const RefreshTokenBrand: unique symbol;

type AccessToken = string & { [AccessTokenBrand]: true };
type RefreshToken = string & { [RefreshTokenBrand]: true };

function createAccessToken(user: User): AccessToken {
  return signToken({ type: "access", sub: user.id, ... }) as AccessToken;
}
```

**Insecure Pattern**:

```typescript
// DON'T: Use generic any for token payloads
function verifyToken(token: string): any {
  return jwt.verify(token, secret)
}

const payload = verifyToken(token)
// No type safety - easy to access wrong properties
console.log(payload.userId) // Should be payload.sub!
```
