# Runtime Safety Guidelines

Prevent code injection, prototype pollution, and ensure safe async patterns.

---

### no-eval

- **Severity**: critical
- **OWASP**: A03 (Injection)

**Risk**: `eval()`, `new Function()`, and dynamic `setTimeout/setInterval` with strings can execute arbitrary code, enabling remote code execution if user input reaches them.

**Secure Pattern**:

```typescript
// DO: Use structured data instead of eval for configuration
interface PluginConfig {
  name: string
  enabled: boolean
  options: Record<string, unknown>
}

function loadPlugin(config: PluginConfig): Plugin {
  // Use a registry pattern instead of eval
  const pluginFactory = PLUGIN_REGISTRY.get(config.name)

  if (!pluginFactory) {
    throw new Error(`Unknown plugin: ${config.name}`)
  }

  return pluginFactory(config.options)
}

// DO: Use JSON.parse for data, not eval
function parseConfig(jsonString: string): Config {
  return JSON.parse(jsonString) // Safe - only parses data, not code
}

// DO: Use function references for callbacks
function scheduleTask(callback: () => void, delay: number): void {
  setTimeout(callback, delay) // Function reference, not string
}

// DO: Use template literals for string building
function buildMessage(name: string, value: number): string {
  return `Hello ${name}, your value is ${value}`
}
```

**Insecure Pattern**:

```typescript
// DON'T: eval() with any input
const result = eval(userInput) // Remote Code Execution!

// DON'T: new Function() with user input
const fn = new Function('x', userCode) // Code injection!

// DON'T: setTimeout/setInterval with strings
setTimeout('doSomething()', 1000) // Evaluates string as code
setTimeout(`process('${userInput}')`, 1000) // Code injection!

// DON'T: Dynamic require/import with user input
const module = require(userInput) // Arbitrary module loading
const mod = await import(userInput) // Same issue
```

---

### safe-child-process

- **Severity**: critical
- **OWASP**: A03 (Injection)

**Risk**: Using `exec()` or `execSync()` with user input allows command injection. Shell metacharacters can break out and execute arbitrary commands.

**Secure Pattern**:

```typescript
import { spawn, execFile } from 'node:child_process'
import path from 'node:path'

// DO: Use spawn with arguments array (no shell by default)
function convertImage(inputPath: string, outputPath: string): Promise<void> {
  return new Promise((resolve, reject) => {
    // Validate paths first
    const safeInput = path.resolve('/app/uploads', path.basename(inputPath))
    const safeOutput = path.resolve('/app/processed', path.basename(outputPath))

    const process = spawn(
      'convert',
      [safeInput, '-resize', '100x100', safeOutput],
      {
        shell: false, // Explicitly disable shell
        timeout: 30000, // Prevent hanging
      },
    )

    process.on('error', reject)
    process.on('close', (code) => {
      if (code === 0) resolve()
      else reject(new Error(`Process exited with code ${code}`))
    })
  })
}

// DO: Use execFile for simple commands (no shell, argument array)
import { execFile } from 'node:child_process'

function getGitBranch(): Promise<string> {
  return new Promise((resolve, reject) => {
    execFile('git', ['rev-parse', '--abbrev-ref', 'HEAD'], (error, stdout) => {
      if (error) reject(error)
      else resolve(stdout.trim())
    })
  })
}

// DO: If shell is absolutely needed, use allowlist validation
const ALLOWED_COMMANDS = new Set(['ls', 'date', 'whoami'])

function runAllowedCommand(command: string): Promise<string> {
  if (!ALLOWED_COMMANDS.has(command)) {
    throw new Error(`Command not allowed: ${command}`)
  }

  return new Promise((resolve, reject) => {
    execFile(command, [], (error, stdout) => {
      if (error) reject(error)
      else resolve(stdout)
    })
  })
}
```

**Insecure Pattern**:

```typescript
import { exec, execSync } from 'node:child_process'

// DON'T: exec with user input (command injection)
exec(`convert ${userFilename} output.jpg`) // Shell injection!
// If userFilename = "file.jpg; rm -rf /"

// DON'T: execSync with string concatenation
const output = execSync(`grep ${searchTerm} file.txt`) // Injection!

// DON'T: spawn with shell: true and user input
spawn('convert', [userInput], { shell: true }) // Shell enabled!
```

---

### vm-sandboxing

- **Severity**: high
- **OWASP**: A03 (Injection)

**Risk**: Node.js `vm` module is NOT a security sandbox. Malicious code can escape using prototype chains or constructor access. Only use for untrusted code with extreme caution.

**Secure Pattern**:

```typescript
import vm from 'node:vm'

// DO: Use vm with minimal context for semi-trusted code only
function evaluateExpression(
  expression: string,
  variables: Record<string, number>,
): number {
  // Only allow simple math expressions
  if (!/^[\d\s+\-*/().a-z]+$/i.test(expression)) {
    throw new Error('Invalid expression')
  }

  // Create minimal context with only needed values
  const context = vm.createContext({
    ...variables,
    Math: Object.freeze({ ...Math }), // Frozen copy of Math
  })

  // Use strict timeout
  const result = vm.runInContext(expression, context, {
    timeout: 100, // 100ms max
    displayErrors: false,
  })

  if (typeof result !== 'number' || !Number.isFinite(result)) {
    throw new Error('Expression must return a finite number')
  }

  return result
}

// DO: For true sandboxing, use isolated-vm or worker threads
import ivm from 'isolated-vm'

async function runUntrustedCode(code: string): Promise<unknown> {
  const isolate = new ivm.Isolate({ memoryLimit: 8 }) // 8MB limit

  try {
    const context = await isolate.createContext()

    // Only expose safe APIs
    const jail = context.global
    await jail.set('log', new ivm.Callback((msg: string) => console.log(msg)))

    const script = await isolate.compileScript(code)
    return await script.run(context, { timeout: 1000 })
  } finally {
    isolate.dispose()
  }
}
```

**Insecure Pattern**:

```typescript
// DON'T: Assume vm is a security sandbox
const context = vm.createContext({ console })
vm.runInContext(userCode, context) // Can escape sandbox!

// Example escape (DON'T USE):
// const code = "this.constructor.constructor('return process')().exit()";

// DON'T: Expose dangerous objects in context
vm.runInContext(code, {
  require, // Can load any module!
  process, // Can exit, access env, etc.
  global, // Full access to Node.js
})
```

---

### object-freeze

- **Severity**: medium
- **OWASP**: A03 (Injection)

**Risk**: Mutable objects can be modified through prototype pollution or accidental mutation, leading to security bypasses.

**Secure Pattern**:

```typescript
// DO: Freeze configuration and security-critical objects
const SECURITY_CONFIG = Object.freeze({
  allowedOrigins: Object.freeze(['https://example.com']),
  maxRequestSize: 1024,
  sessionTimeout: 3600000,
  requiredHeaders: Object.freeze(['Authorization', 'Content-Type']),
})

// DO: Deep freeze for nested objects
function deepFreeze<T extends object>(obj: T): Readonly<T> {
  Object.keys(obj).forEach((key) => {
    const value = (obj as Record<string, unknown>)[key]
    if (value && typeof value === 'object' && !Object.isFrozen(value)) {
      deepFreeze(value as object)
    }
  })
  return Object.freeze(obj)
}

const APP_CONFIG = deepFreeze({
  database: {
    host: 'localhost',
    port: 5432,
  },
  security: {
    jwtExpiry: 900,
    bcryptRounds: 12,
  },
})

// DO: Use Object.seal for objects that can be modified but not extended
const userPreferences = Object.seal({
  theme: 'light',
  language: 'en',
})
userPreferences.theme = 'dark' // OK
userPreferences.newProp = 'value' // Throws in strict mode

// DO: Use Object.defineProperty for truly immutable properties
class SecureService {
  constructor(private readonly apiKey: string) {
    Object.defineProperty(this, 'apiKey', {
      value: apiKey,
      writable: false,
      configurable: false,
      enumerable: false,
    })
  }
}
```

**Insecure Pattern**:

```typescript
// DON'T: Leave security config mutable
const config = {
  allowedRoles: ['user', 'admin'],
}

// Later, malicious code could do:
config.allowedRoles.push('superadmin')

// DON'T: Use spread without freezing (creates mutable copy)
const newConfig = { ...config } // Still mutable!
```

---

### frozen-intrinsics

- **Severity**: medium
- **OWASP**: A03 (Injection)

**Risk**: Prototype pollution attacks modify built-in prototypes (Object, Array, etc.) to inject malicious properties or methods that affect all instances.

**Secure Pattern**:

```typescript
// DO: Freeze prototypes early in application startup
// Place this at the very top of your entry point (before any other imports)

// Freeze Object prototype
Object.freeze(Object.prototype)

// Freeze Array prototype
Object.freeze(Array.prototype)

// Freeze Function prototype
Object.freeze(Function.prototype)

// Freeze String prototype
Object.freeze(String.prototype)

// Freeze Number prototype
Object.freeze(Number.prototype)

// DO: Use --frozen-intrinsics flag when available
// node --frozen-intrinsics app.js

// DO: Create objects without prototype for untrusted data
function parseUntrustedJson(json: string): Record<string, unknown> {
  const parsed = JSON.parse(json)

  // Create null-prototype object to prevent prototype access
  const safe = Object.create(null)

  for (const [key, value] of Object.entries(parsed)) {
    // Skip prototype-related keys
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      continue
    }
    safe[key] = value
  }

  return safe
}

// DO: Use Map instead of objects for untrusted keys
const userSettings = new Map<string, unknown>()
userSettings.set(untrustedKey, value) // Safe - no prototype chain
```

**Insecure Pattern**:

```typescript
// DON'T: Leave prototypes unfrozen
// Attacker can pollute via JSON parsing or object merge:
// {"__proto__": {"isAdmin": true}}

// DON'T: Merge untrusted data into objects
Object.assign(target, untrustedData) // Prototype pollution!

// DON'T: Use bracket notation with untrusted keys
obj[untrustedKey] = value // Could be "__proto__"
```

---

### async-await-patterns

- **Severity**: medium
- **OWASP**: A04 (Insecure Design)

**Risk**: Improper async handling can cause unhandled rejections, race conditions, or resource leaks that lead to denial of service or security bypasses.

**Secure Pattern**:

```typescript
// DO: Always handle errors in async functions
async function fetchUser(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`Failed to fetch user ${id}:`, error)
    return null
  }
}

// DO: Use Promise.allSettled for parallel operations that can fail independently
async function fetchMultipleUsers(
  ids: string[],
): Promise<Map<string, User | null>> {
  const results = await Promise.allSettled(ids.map((id) => fetchUser(id)))
  const users = new Map<string, User | null>()

  results.forEach((result, index) => {
    users.set(ids[index], result.status === 'fulfilled' ? result.value : null)
  })

  return users
}

// DO: Implement timeouts for async operations
async function fetchWithTimeout<T>(
  operation: () => Promise<T>,
  timeoutMs: number,
): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Operation timed out')), timeoutMs)
  })

  return Promise.race([operation(), timeoutPromise])
}

// DO: Clean up resources with try/finally
async function processFile(path: string): Promise<void> {
  const handle = await fs.open(path, 'r')

  try {
    const content = await handle.readFile('utf-8')
    await processContent(content)
  } finally {
    await handle.close() // Always close, even on error
  }
}

// DO: Use AbortController for cancellable operations
async function fetchWithCancel(
  url: string,
  signal: AbortSignal,
): Promise<Response> {
  return fetch(url, { signal })
}

const controller = new AbortController()
setTimeout(() => controller.abort(), 5000) // Cancel after 5s
```

**Insecure Pattern**:

```typescript
// DON'T: Ignore promise rejections
fetchUser(id) // Unhandled rejection if it fails!

// DON'T: Use Promise.all when failures should be independent
await Promise.all(ids.map(fetchUser)) // All fail if one fails

// DON'T: Forget to clean up resources
async function processFile(path: string) {
  const handle = await fs.open(path, 'r')
  await processContent(await handle.readFile()) // If this throws, handle is never closed
}

// DON'T: Create async functions that never complete
async function waitForever() {
  await new Promise(() => {}) // Never resolves - resource leak
}
```

---

### event-loop-monitoring

- **Severity**: medium
- **OWASP**: A05 (Security Misconfiguration)

**Risk**: Event loop blocking or overload can cause denial of service. CPU-intensive operations on the main thread freeze all request handling.

**Secure Pattern**:

```typescript
import toobusy from 'toobusy-js'
import { Worker } from 'node:worker_threads'

// DO: Monitor event loop lag and reject requests when overloaded
toobusy.maxLag(100) // 100ms max lag
toobusy.interval(500) // Check every 500ms

app.use((req, res, next) => {
  if (toobusy()) {
    res.status(503).json({
      error: 'Server is busy, please try again',
      retryAfter: 5,
    })
    return
  }
  next()
})

// DO: Offload CPU-intensive work to worker threads
function runCpuIntensiveTask(data: unknown): Promise<unknown> {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./workers/heavy-task.js', {
      workerData: data,
    })

    const timeout = setTimeout(() => {
      worker.terminate()
      reject(new Error('Worker timed out'))
    }, 30000)

    worker.on('message', (result) => {
      clearTimeout(timeout)
      resolve(result)
    })

    worker.on('error', (error) => {
      clearTimeout(timeout)
      reject(error)
    })
  })
}

// DO: Use setImmediate/process.nextTick to yield to event loop
async function processLargeArray<T>(
  items: T[],
  processor: (item: T) => Promise<void>,
): Promise<void> {
  const BATCH_SIZE = 100

  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE)
    await Promise.all(batch.map(processor))

    // Yield to event loop between batches
    await new Promise((resolve) => setImmediate(resolve))
  }
}
```

**Insecure Pattern**:

```typescript
// DON'T: Run CPU-intensive code on main thread
app.post('/hash', (req, res) => {
  // Blocks event loop for all other requests!
  const hash = computeExpensiveHash(req.body.data)
  res.json({ hash })
})

// DON'T: Process large arrays synchronously
function processAll(items: Item[]) {
  for (const item of items) {
    processItemSync(item) // Blocks for entire array
  }
}

// DON'T: Ignore event loop lag
app.post('/api/data', async (req, res) => {
  // No check if server is overloaded
  const result = await heavyComputation(req.body)
  res.json(result)
})
```
