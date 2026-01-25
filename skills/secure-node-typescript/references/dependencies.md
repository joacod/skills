# Dependency Security Guidelines

Secure dependency management and supply chain protection.

---

### pin-versions

- **Severity**: high
- **OWASP**: A03 (Software Supply Chain Failures), A08 (Software & Data Integrity Failures)

**Risk**: Unpinned dependencies can auto-update to compromised versions, and version ranges allow supply chain attacks through malicious updates.

**Secure Pattern**:

```json
// package.json - DO: Use exact versions
{
  "dependencies": {
    "express": "4.18.2",
    "zod": "3.22.4",
    "argon2": "0.31.2"
  },
  "devDependencies": {
    "typescript": "5.3.3",
    "eslint": "8.56.0"
  }
}
```

```ini
# .npmrc - DO: Enforce exact versions
save-exact=true
package-lock=true
```

```typescript
// DO: Verify package-lock.json integrity in CI
import { execSync } from 'node:child_process'

function verifyLockfile(): void {
  try {
    // This fails if package-lock.json is out of sync
    execSync('npm ci', { stdio: 'inherit' })
  } catch {
    throw new Error('Lockfile integrity check failed')
  }
}

// DO: Use npm ci instead of npm install in production
// npm ci uses exact versions from package-lock.json
```

```yaml
# GitHub Actions - DO: Verify lockfile
- name: Install dependencies
  run: npm ci # NOT npm install

- name: Verify lockfile is up to date
  run: |
    npm install --package-lock-only
    git diff --exit-code package-lock.json
```

**Insecure Pattern**:

```json
// DON'T: Use version ranges
{
  "dependencies": {
    "express": "^4.18.0", // Could get 4.19.0 with vulnerabilities
    "lodash": "~4.17.0", // Could get 4.17.99
    "axios": "*" // Gets any version!
  }
}
```

```bash
# DON'T: Use npm install in production
npm install  # May update packages

# DON'T: Ignore lockfile
npm install --no-package-lock
```

---

### lockfile-integrity

- **Severity**: high
- **OWASP**: A08 (Software & Data Integrity Failures)

**Risk**: Corrupted or tampered lockfiles can cause installation of malicious packages. Missing lockfile verification allows supply chain attacks.

**Secure Pattern**:

```typescript
// DO: Verify lockfile hash in CI/CD
import crypto from 'node:crypto'
import fs from 'node:fs'

function hashLockfile(): string {
  const content = fs.readFileSync('package-lock.json')
  return crypto.createHash('sha256').update(content).digest('hex')
}

// Store expected hash securely
const EXPECTED_LOCKFILE_HASH = process.env.LOCKFILE_HASH

function verifyLockfileIntegrity(): void {
  const currentHash = hashLockfile()

  if (currentHash !== EXPECTED_LOCKFILE_HASH) {
    throw new Error('Lockfile integrity verification failed')
  }
}
```

```yaml
# GitHub Actions - DO: Use npm ci and verify
jobs:
  build:
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci --ignore-scripts # Skip postinstall scripts initially

      - name: Run allowed postinstall scripts
        run: npm rebuild # Only rebuild native modules
```

```json
// package.json - DO: Use npm audit signatures
{
  "scripts": {
    "preinstall": "npm audit signatures"
  }
}
```

**Insecure Pattern**:

```bash
# DON'T: Install without lockfile
rm package-lock.json
npm install

# DON'T: Force update lockfile without review
npm update
git add -A && git commit -m "update deps"

# DON'T: Run arbitrary postinstall scripts in CI
npm install  # Runs all postinstall scripts automatically
```

---

### npm-audit

- **Severity**: high
- **OWASP**: A03 (Software Supply Chain Failures)

**Risk**: Known vulnerabilities in dependencies can be exploited if not detected and patched promptly.

**Secure Pattern**:

```bash
# DO: Run npm audit in CI with failure threshold
npm audit --audit-level=high  # Fail on high+ vulnerabilities
```

```json
// package.json - DO: Add audit scripts
{
  "scripts": {
    "audit": "npm audit --audit-level=high",
    "audit:fix": "npm audit fix",
    "audit:report": "npm audit --json > audit-report.json"
  }
}
```

```yaml
# GitHub Actions - DO: Automated security scanning
name: Security Audit

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *' # Daily

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Check for outdated packages
        run: npm outdated || true # Don't fail, just report
```

```typescript
// DO: Parse audit results programmatically
import { execSync } from 'node:child_process'

interface AuditResult {
  vulnerabilities: {
    [severity: string]: number
  }
}

function runSecurityAudit(): AuditResult {
  try {
    const output = execSync('npm audit --json', { encoding: 'utf-8' })
    return JSON.parse(output)
  } catch (error) {
    // npm audit exits with non-zero when vulnerabilities found
    const output = (error as { stdout?: string }).stdout || '{}'
    return JSON.parse(output)
  }
}

function hasHighSeverityVulnerabilities(): boolean {
  const result = runSecurityAudit()
  return (
    (result.vulnerabilities?.high ?? 0) > 0 ||
    (result.vulnerabilities?.critical ?? 0) > 0
  )
}
```

**Insecure Pattern**:

```bash
# DON'T: Ignore audit warnings
npm install  # Ignores security warnings

# DON'T: Use --force to bypass security
npm install --force
npm audit fix --force  # May introduce breaking changes

# DON'T: Skip audit in CI
npm ci --ignore-scripts --no-audit
```

---

### snyk-integration

- **Severity**: high
- **OWASP**: A03 (Software Supply Chain Failures)

**Risk**: npm audit alone may miss vulnerabilities. Snyk and similar tools provide broader coverage and earlier detection.

**Secure Pattern**:

```yaml
# GitHub Actions - DO: Integrate Snyk scanning
name: Snyk Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

```json
// package.json - DO: Add Snyk scripts
{
  "scripts": {
    "snyk:test": "snyk test --severity-threshold=high",
    "snyk:monitor": "snyk monitor",
    "security": "npm audit && snyk test"
  }
}
```

```typescript
// DO: Use multiple security scanning tools
const SECURITY_SCANNERS = [
  { name: 'npm-audit', command: 'npm audit --audit-level=high' },
  { name: 'snyk', command: 'snyk test --severity-threshold=high' },
  { name: 'socket', command: 'socket scan' },
]

async function runSecurityScanners(): Promise<void> {
  const results = await Promise.allSettled(
    SECURITY_SCANNERS.map(async (scanner) => {
      try {
        execSync(scanner.command, { stdio: 'inherit' })
        return { scanner: scanner.name, passed: true }
      } catch {
        return { scanner: scanner.name, passed: false }
      }
    }),
  )

  const failures = results.filter(
    (r) => r.status === 'fulfilled' && !r.value.passed,
  )

  if (failures.length > 0) {
    throw new Error(
      `Security scanners failed: ${failures.map((f) => f.value?.scanner).join(', ')}`,
    )
  }
}
```

**Insecure Pattern**:

```bash
# DON'T: Rely on npm audit alone
npm audit  # May miss vulnerabilities that Snyk catches

# DON'T: Ignore Snyk warnings in PR
# Merge despite security warnings because "we'll fix it later"
```

---

### type-safe-libraries

- **Severity**: medium
- **OWASP**: A03 (Software Supply Chain Failures)

**Risk**: Libraries without TypeScript types lose compile-time safety benefits and may have incorrect type assumptions that lead to runtime errors.

**Secure Pattern**:

```json
// package.json - DO: Check for types availability
{
  "dependencies": {
    "express": "4.18.2",
    "zod": "3.22.4" // Built-in types
  },
  "devDependencies": {
    "@types/express": "4.17.21" // Separate types package
  }
}
```

```typescript
// DO: Verify type coverage
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "skipLibCheck": false  // Check types in node_modules
  }
}
```

```bash
# DO: Check for missing types
npx typesync  # Finds missing @types packages
```

```typescript
// DO: Create type declarations for untyped libraries
// types/untyped-lib.d.ts
declare module 'untyped-lib' {
  export function unsafeFunction(input: string): unknown
}

// DO: Wrap untyped libraries with type-safe interfaces
import untypedLib from 'untyped-lib'
import { z } from 'zod'

const ResultSchema = z.object({
  data: z.string(),
  status: z.number(),
})

export function safeWrapper(input: string): z.infer<typeof ResultSchema> {
  const result = untypedLib.unsafeFunction(input)
  return ResultSchema.parse(result)
}
```

**Insecure Pattern**:

```typescript
// DON'T: Use libraries without checking for types
import someLib from 'untyped-library' // No type safety

// DON'T: Use any for library return types
const result: any = someLib.doSomething()
result.nonExistent.property // Runtime error

// DON'T: Disable type checking for convenience
// @ts-ignore
import badLib from 'bad-lib'
```

---

### no-experimental

- **Severity**: medium
- **OWASP**: A03 (Software Supply Chain Failures)

**Risk**: Experimental Node.js features and unstable APIs may have undiscovered security vulnerabilities, breaking changes, or unexpected behavior.

**Secure Pattern**:

```json
// package.json - DO: Specify stable Node.js version
{
  "engines": {
    "node": ">=20.0.0 <21.0.0"
  }
}
```

```ini
# .nvmrc - DO: Pin to LTS version
20.11.0
```

```typescript
// DO: Check for stable APIs before use
import { availableParallelism } from 'node:os'

// Check if API exists (added in Node.js 19.4.0)
const parallelism =
  typeof availableParallelism === 'function'
    ? availableParallelism()
    : require('node:os').cpus().length

// DO: Use feature flags carefully
const USE_EXPERIMENTAL_FEATURE = process.env.ENABLE_EXPERIMENTAL === 'true'

if (USE_EXPERIMENTAL_FEATURE) {
  console.warn('Using experimental feature - not recommended for production')
}
```

```bash
# DON'T: Use experimental flags in production
# node --experimental-loader ./loader.mjs app.js
# node --experimental-vm-modules app.js

# DO: Document any experimental usage
```

```typescript
// DO: Wrap experimental features with fallbacks
async function parseModule(code: string): Promise<unknown> {
  if (process.env.NODE_ENV === 'production') {
    // Use stable parsing in production
    return JSON.parse(code)
  }

  // Experimental only in development
  // ...
}
```

**Insecure Pattern**:

```bash
# DON'T: Use experimental flags in production
node --experimental-modules --experimental-wasm-modules app.js

# DON'T: Use Node.js odd-numbered versions in production
# Node.js 21.x is "current" not "LTS"
```

```typescript
// DON'T: Rely on experimental APIs without fallbacks
import { someExperimentalApi } from 'node:experimental'

// DON'T: Use unstable TypeScript features
// tsconfig.json: "experimentalDecorators": true
```
