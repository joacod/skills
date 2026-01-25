# Error Handling & Logging Guidelines

Secure error handling, structured logging, and monitoring.

---

### global-error-handlers

- **Severity**: high
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Unhandled exceptions and promise rejections can crash the application, cause resource leaks, or leave the system in an inconsistent state.

**Secure Pattern**:

```typescript
// DO: Register global error handlers early in application startup
process.on('uncaughtException', (error: Error) => {
  console.error('Uncaught exception:', {
    name: error.name,
    message: error.message,
    stack: error.stack,
  })

  // Perform cleanup
  gracefulShutdown()
    .then(() => process.exit(1))
    .catch(() => process.exit(1))
})

process.on(
  'unhandledRejection',
  (reason: unknown, promise: Promise<unknown>) => {
    console.error('Unhandled rejection:', {
      reason: reason instanceof Error ? reason.message : String(reason),
      promise: String(promise),
    })

    // In production, treat as fatal
    if (process.env.NODE_ENV === 'production') {
      gracefulShutdown()
        .then(() => process.exit(1))
        .catch(() => process.exit(1))
    }
  },
)

// DO: Implement graceful shutdown
async function gracefulShutdown(): Promise<void> {
  console.log('Shutting down gracefully...')

  // Stop accepting new connections
  server.close()

  // Close database connections
  await db.end()

  // Flush logs
  await logger.flush()

  // Allow time for cleanup
  await new Promise((resolve) => setTimeout(resolve, 5000))
}

// DO: Handle termination signals
process.on('SIGTERM', gracefulShutdown)
process.on('SIGINT', gracefulShutdown)

// DO: Express error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // Log full error internally
  console.error('Request error:', {
    method: req.method,
    path: req.path,
    error: err.message,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
  })

  // Send generic error to client
  res.status(500).json({ error: 'Internal server error' })
})
```

**Insecure Pattern**:

```typescript
// DON'T: Leave errors unhandled
async function main() {
  await riskyOperation() // Unhandled rejection crashes process
}
main()

// DON'T: Catch and ignore errors
process.on('uncaughtException', () => {
  // Silently ignore - bad!
})

// DON'T: Continue running after uncaught exception
process.on('uncaughtException', (error) => {
  console.log('Error:', error)
  // Continue running in corrupted state
})
```

---

### custom-error-types

- **Severity**: medium
- **OWASP**: A04 (Insecure Design)

**Risk**: Without custom error types, it's difficult to distinguish between different error conditions, leading to incorrect error handling and security bypasses.

**Secure Pattern**:

```typescript
// DO: Define custom error classes
abstract class AppError extends Error {
  abstract readonly statusCode: number
  abstract readonly code: string
  readonly isOperational: boolean = true

  constructor(message: string) {
    super(message)
    this.name = this.constructor.name
    Error.captureStackTrace(this, this.constructor)
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
    }
  }
}

class ValidationError extends AppError {
  readonly statusCode = 400
  readonly code = 'VALIDATION_ERROR'

  constructor(
    message: string,
    public readonly field?: string,
    public readonly details?: unknown,
  ) {
    super(message)
  }
}

class AuthenticationError extends AppError {
  readonly statusCode = 401
  readonly code = 'AUTHENTICATION_ERROR'
}

class AuthorizationError extends AppError {
  readonly statusCode = 403
  readonly code = 'AUTHORIZATION_ERROR'

  constructor(
    message: string,
    public readonly requiredPermission?: string,
  ) {
    super(message)
  }
}

class NotFoundError extends AppError {
  readonly statusCode = 404
  readonly code = 'NOT_FOUND'

  constructor(
    message: string,
    public readonly resource?: string,
  ) {
    super(message)
  }
}

class RateLimitError extends AppError {
  readonly statusCode = 429
  readonly code = 'RATE_LIMIT_EXCEEDED'

  constructor(
    message: string,
    public readonly retryAfter?: number,
  ) {
    super(message)
  }
}

// DO: Use type guards for error handling
function isAppError(error: unknown): error is AppError {
  return error instanceof AppError
}

function isOperationalError(error: unknown): boolean {
  return isAppError(error) && error.isOperational
}

// DO: Error handling middleware with type checking
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  if (isAppError(err)) {
    // Operational error - send appropriate response
    res.status(err.statusCode).json(err.toJSON())
  } else {
    // Unknown error - log and send generic response
    console.error('Unknown error:', err)
    res
      .status(500)
      .json({ code: 'INTERNAL_ERROR', message: 'Internal server error' })
  }
})
```

**Insecure Pattern**:

```typescript
// DON'T: Use generic errors for everything
throw new Error('Something went wrong')

// DON'T: Use magic strings for error types
if (error.message === 'Not found') {
  // Fragile comparison
}

// DON'T: Expose internal error details
res.status(500).json({ error: error.message, stack: error.stack })
```

---

### structured-logging

- **Severity**: high
- **OWASP**: A09 (Logging Failures)

**Risk**: Unstructured logs are difficult to search, analyze, and monitor. Missing security events prevent detection of attacks.

**Secure Pattern**:

```typescript
import pino from 'pino'

// DO: Configure structured logging
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  redact: {
    // Redact sensitive fields
    paths: [
      'password',
      'token',
      'authorization',
      'cookie',
      'req.headers.authorization',
      'req.headers.cookie',
      '*.password',
      '*.secret',
      '*.apiKey',
    ],
    censor: '[REDACTED]',
  },
  timestamp: pino.stdTimeFunctions.isoTime,
})

// DO: Create child loggers with context
function createRequestLogger(req: Request) {
  return logger.child({
    requestId: req.id,
    method: req.method,
    path: req.path,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
  })
}

// DO: Log security-relevant events
const securityLogger = logger.child({ category: 'security' })

function logAuthenticationAttempt(
  email: string,
  success: boolean,
  ip: string,
  reason?: string,
): void {
  securityLogger.info({
    event: 'authentication_attempt',
    email: hashForLog(email), // Hash PII
    success,
    ip,
    reason,
    timestamp: new Date().toISOString(),
  })
}

function logAuthorizationFailure(
  userId: string,
  resource: string,
  action: string,
): void {
  securityLogger.warn({
    event: 'authorization_failure',
    userId,
    resource,
    action,
    timestamp: new Date().toISOString(),
  })
}

function logSuspiciousActivity(
  type: string,
  details: Record<string, unknown>,
): void {
  securityLogger.warn({
    event: 'suspicious_activity',
    type,
    ...details,
    timestamp: new Date().toISOString(),
  })
}

// DO: Hash PII in logs
import crypto from 'node:crypto'

function hashForLog(value: string): string {
  return crypto.createHash('sha256').update(value).digest('hex').slice(0, 16)
}
```

**Insecure Pattern**:

```typescript
// DON'T: Use console.log in production
console.log('User logged in:', email, password) // Logs password!

// DON'T: Log sensitive data
logger.info({ user: { email, password, ssn } }) // Exposes secrets

// DON'T: Use unstructured logs
console.log(`[${new Date()}] User ${email} logged in from ${ip}`)
// Hard to parse and search

// DON'T: Forget to log security events
async function login(email: string, password: string): Promise<User | null> {
  const user = await authenticate(email, password)
  if (!user) {
    return null // No logging of failed attempt!
  }
  return user
}
```

---

### hide-error-details

- **Severity**: high
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Detailed error messages expose system internals, file paths, database structure, and technology stack to attackers.

**Secure Pattern**:

```typescript
// DO: Map internal errors to safe external messages
const ERROR_MESSAGES: Record<string, string> = {
  ValidationError: 'Invalid input provided',
  AuthenticationError: 'Authentication failed',
  AuthorizationError: 'Access denied',
  NotFoundError: 'Resource not found',
  RateLimitError: 'Too many requests',
  DEFAULT: 'An error occurred',
}

function getPublicErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return ERROR_MESSAGES[error.name] || ERROR_MESSAGES.DEFAULT
  }
  return ERROR_MESSAGES.DEFAULT
}

// DO: Create safe error responses
interface ErrorResponse {
  error: {
    code: string
    message: string
    requestId?: string
  }
}

function createErrorResponse(
  error: unknown,
  requestId?: string,
): ErrorResponse {
  const message = getPublicErrorMessage(error)
  const code = error instanceof AppError ? error.code : 'INTERNAL_ERROR'

  return {
    error: {
      code,
      message,
      requestId,
    },
  }
}

// DO: Different error detail levels by environment
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  const requestId = req.id

  // Log full error internally
  logger.error({
    requestId,
    error: err instanceof Error ? err.message : String(err),
    stack: err instanceof Error ? err.stack : undefined,
    path: req.path,
    method: req.method,
  })

  // Send safe response to client
  const statusCode = err instanceof AppError ? err.statusCode : 500
  const response = createErrorResponse(err, requestId)

  // Only add details in development
  if (process.env.NODE_ENV === 'development') {
    ;(response.error as Record<string, unknown>).debug = {
      message: err instanceof Error ? err.message : String(err),
      stack: err instanceof Error ? err.stack : undefined,
    }
  }

  res.status(statusCode).json(response)
})
```

**Insecure Pattern**:

```typescript
// DON'T: Send stack traces to clients
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  res.status(500).json({
    error: err.message, // May contain sensitive info
    stack: err.stack, // Exposes file paths and code structure
  })
})

// DON'T: Include database errors in responses
try {
  await db.query(sql)
} catch (error) {
  res.status(500).json({ error: error.message })
  // "relation 'users' does not exist" - reveals DB structure
}

// DON'T: Expose file system paths
res.status(500).json({
  error: `Failed to read file: /app/secrets/config.json`,
})
```

---

### no-sensitive-logging

- **Severity**: critical
- **OWASP**: A09 (Logging Failures)

**Risk**: Logging sensitive data (passwords, tokens, PII) can lead to credential theft if logs are accessed by attackers or shared for debugging.

**Secure Pattern**:

```typescript
// DO: Use log redaction
import pino from 'pino'

const logger = pino({
  redact: {
    paths: [
      // Authentication
      'password',
      '*.password',
      'newPassword',
      'oldPassword',
      'token',
      '*.token',
      'accessToken',
      'refreshToken',
      'apiKey',
      'secret',

      // Headers
      'req.headers.authorization',
      'req.headers.cookie',
      'res.headers.set-cookie',

      // PII
      'ssn',
      'socialSecurityNumber',
      'creditCard',
      '*.creditCard',

      // Request body sensitive fields
      'req.body.password',
      'req.body.creditCard',
    ],
    censor: '[REDACTED]',
  },
})

// DO: Sanitize objects before logging
function sanitizeForLogging<T extends object>(obj: T): Partial<T> {
  const SENSITIVE_KEYS = new Set([
    'password',
    'token',
    'secret',
    'apiKey',
    'authorization',
    'cookie',
    'creditCard',
    'ssn',
  ])

  return Object.fromEntries(
    Object.entries(obj)
      .filter(([key]) => !SENSITIVE_KEYS.has(key.toLowerCase()))
      .map(([key, value]) => {
        if (typeof value === 'object' && value !== null) {
          return [key, sanitizeForLogging(value)]
        }
        return [key, value]
      }),
  ) as Partial<T>
}

// DO: Create safe request logger
function logRequest(req: Request): void {
  logger.info({
    method: req.method,
    path: req.path,
    query: sanitizeForLogging(req.query),
    body: sanitizeForLogging(req.body),
    ip: req.ip,
    // Don't log full headers - use specific safe ones
    contentType: req.get('Content-Type'),
    userAgent: req.get('User-Agent'),
  })
}

// DO: Mask partial values when needed
function maskEmail(email: string): string {
  const [local, domain] = email.split('@')
  const maskedLocal = local.slice(0, 2) + '***'
  return `${maskedLocal}@${domain}`
}

function maskCreditCard(card: string): string {
  return '****' + card.slice(-4)
}
```

**Insecure Pattern**:

```typescript
// DON'T: Log credentials
logger.info('Login attempt', { email, password }) // Logs password!

// DON'T: Log full request objects
logger.info('Request received', { req }) // May contain auth headers

// DON'T: Log tokens
logger.debug('Token generated', { userId, token }) // Exposes token!

// DON'T: Log PII without masking
logger.info('User updated', { email, ssn, creditCard })

// DON'T: Use console.log with sensitive data
console.log('Debug:', JSON.stringify(req.body)) // May contain secrets
```
