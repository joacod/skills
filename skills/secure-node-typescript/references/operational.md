# Operational Security Guidelines

Linters, CI/CD security, documentation, and threat modeling.

---

### eslint-security

- **Severity**: high
- **OWASP**: A06 (Insecure Design)

**Risk**: Without security-focused linting, common vulnerabilities slip through code review and reach production.

**Secure Pattern**:

```javascript
// eslint.config.js - DO: Configure security plugins
import js from '@eslint/js'
import tseslint from '@typescript-eslint/eslint-plugin'
import tsparser from '@typescript-eslint/parser'
import security from 'eslint-plugin-security'

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: './tsconfig.json',
      },
    },
    plugins: {
      '@typescript-eslint': tseslint,
      security,
    },
    rules: {
      // TypeScript strict rules
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/strict-boolean-expressions': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
      '@typescript-eslint/await-thenable': 'error',

      // Security plugin rules
      'security/detect-buffer-noassert': 'error',
      'security/detect-child-process': 'error',
      'security/detect-disable-mustache-escape': 'error',
      'security/detect-eval-with-expression': 'error',
      'security/detect-new-buffer': 'error',
      'security/detect-no-csrf-before-method-override': 'error',
      'security/detect-non-literal-fs-filename': 'warn',
      'security/detect-non-literal-regexp': 'warn',
      'security/detect-non-literal-require': 'error',
      'security/detect-object-injection': 'warn',
      'security/detect-possible-timing-attacks': 'warn',
      'security/detect-pseudoRandomBytes': 'error',
      'security/detect-unsafe-regex': 'error',

      // Built-in security-relevant rules
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'no-new-func': 'error',
      'no-script-url': 'error',
    },
  },
]
```

```json
// package.json - DO: Add lint scripts
{
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "lint:fix": "eslint . --fix",
    "lint:security": "eslint . --config eslint-security.config.js"
  }
}
```

**Insecure Pattern**:

```javascript
// DON'T: Disable security rules
/* eslint-disable security/detect-eval-with-expression */
eval(userInput);

// DON'T: Use lenient configurations
{
  "rules": {
    "security/detect-object-injection": "off",
    "@typescript-eslint/no-explicit-any": "off"
  }
}

// DON'T: Skip linting
npm run build --ignore-scripts
```

---

### static-analysis

- **Severity**: high
- **OWASP**: A06 (Insecure Design)

**Risk**: Code review alone misses subtle security issues. Static analysis tools catch patterns that humans overlook.

**Secure Pattern**:

```yaml
# .github/workflows/security.yml - DO: Integrate multiple tools
name: Security Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  codeql:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: typescript

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/typescript
            p/nodejs

  sonarcloud:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

```yaml
# sonar-project.properties - DO: Configure quality gates
sonar.projectKey=my-project
sonar.organization=my-org

# Security hotspots must be reviewed
sonar.security.hotspots.reviewed.rating=A

# No new security issues allowed
sonar.qualitygate.wait=true
```

```json
// package.json - DO: Add static analysis scripts
{
  "scripts": {
    "analyze": "npm run lint && npm run audit",
    "analyze:security": "semgrep --config auto .",
    "analyze:types": "tsc --noEmit --strict"
  }
}
```

**Insecure Pattern**:

```yaml
# DON'T: Skip analysis on branches
on:
  push:
    branches: [main]  # Only main, not PRs

# DON'T: Continue on errors
- name: Run analysis
  run: npm run lint || true  # Ignores failures
  continue-on-error: true

# DON'T: Disable security checks
jobs:
  build:
    steps:
      # No security scanning at all
      - run: npm ci
      - run: npm run build
```

---

### pre-commit-hooks

- **Severity**: medium
- **OWASP**: A06 (Insecure Design)

**Risk**: Without pre-commit checks, developers can commit code with security issues, secrets, or lint violations.

**Secure Pattern**:

```json
// package.json - DO: Configure husky and lint-staged
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix --max-warnings 0", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

```bash
# .husky/pre-commit - DO: Run checks before commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run lint-staged
npx lint-staged

# Check for secrets
npx secretlint "**/*"

# Type check
npx tsc --noEmit
```

```bash
# .husky/pre-push - DO: Run tests before push
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

# Run tests
npm test

# Security audit
npm audit --audit-level=high
```

```json
// .secretlintrc.json - DO: Configure secret detection
{
  "rules": [
    {
      "id": "@secretlint/secretlint-rule-preset-recommend"
    },
    {
      "id": "@secretlint/secretlint-rule-aws",
      "options": {
        "allows": []
      }
    },
    {
      "id": "@secretlint/secretlint-rule-gcp"
    },
    {
      "id": "@secretlint/secretlint-rule-privatekey"
    }
  ]
}
```

**Insecure Pattern**:

```bash
# DON'T: Allow bypassing hooks
git commit --no-verify  # Skips all hooks

# DON'T: Make hooks optional
# Missing .husky directory or disabled hooks
```

---

### ci-cd-security

- **Severity**: high
- **OWASP**: A08 (Software & Data Integrity Failures)

**Risk**: Insecure CI/CD pipelines can be exploited to inject malicious code, steal secrets, or compromise production deployments.

**Secure Pattern**:

```yaml
# .github/workflows/ci.yml - DO: Secure CI configuration
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read # Minimal permissions

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Pin action versions to full SHA
      - uses: actions/setup-node@v4
        with:
          node-version-file: '.nvmrc'
          cache: 'npm'

      # Use npm ci, not npm install
      - name: Install dependencies
        run: npm ci --ignore-scripts

      # Run allowed postinstall explicitly
      - name: Build native modules
        run: npm rebuild

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Build
        run: npm run build

  security:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run security audit
        run: npm audit --audit-level=high

      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  deploy:
    needs: [build, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production # Requires approval
    steps:
      - name: Deploy
        run: |
          # Deployment logic
        env:
          # Use OIDC instead of long-lived secrets when possible
          AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
```

```yaml
# DO: Protect secrets in workflows
jobs:
  deploy:
    steps:
      - name: Deploy
        env:
          # Secrets are masked in logs
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          # Don't echo secrets
          # DON'T: echo $API_KEY
          deploy --key "$API_KEY"
```

**Insecure Pattern**:

```yaml
# DON'T: Use excessive permissions
permissions: write-all

# DON'T: Use unpinned actions
- uses: actions/checkout@main  # Could change unexpectedly

# DON'T: Echo secrets
- run: echo ${{ secrets.API_KEY }}  # Exposed in logs

# DON'T: Run arbitrary code from PRs
on:
  pull_request_target:  # Dangerous - runs with write access
    types: [opened]
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # Untrusted code!
      - run: npm install  # Runs untrusted postinstall scripts
```

---

### threat-modeling

- **Severity**: high
- **OWASP**: A06 (Insecure Design)

**Risk**: Without threat modeling, security controls may miss actual threats while adding complexity for non-existent risks.

**Secure Pattern**:

```markdown
# THREAT_MODEL.md - DO: Document security analysis

## Overview

Brief description of the system and its security requirements.

## Assets

What needs to be protected:

- User credentials and sessions
- Personal data (PII)
- API keys and secrets
- Business data

## Trust Boundaries

Where different trust levels interact:

1. Internet → Load balancer (untrusted → DMZ)
2. Load balancer → Application (DMZ → internal)
3. Application → Database (internal → data tier)

## Threats (STRIDE)

### Spoofing

| Threat            | Mitigation                       | Status      |
| ----------------- | -------------------------------- | ----------- |
| Session hijacking | Secure cookies, session rotation | Implemented |
| Token forgery     | JWT signing, validation          | Implemented |

### Tampering

| Threat                 | Mitigation                    | Status      |
| ---------------------- | ----------------------------- | ----------- |
| Parameter manipulation | Input validation, Zod schemas | Implemented |
| SQL injection          | Parameterized queries         | Implemented |

### Repudiation

| Threat         | Mitigation               | Status      |
| -------------- | ------------------------ | ----------- |
| Denied actions | Structured audit logging | Implemented |

### Information Disclosure

| Threat                | Mitigation                    | Status      |
| --------------------- | ----------------------------- | ----------- |
| Error message leakage | Generic error responses       | Implemented |
| Log exposure          | Log redaction, access control | Implemented |

### Denial of Service

| Threat           | Mitigation       | Status      |
| ---------------- | ---------------- | ----------- |
| Request flooding | Rate limiting    | Implemented |
| Large payload    | Body size limits | Implemented |

### Elevation of Privilege

| Threat      | Mitigation       | Status      |
| ----------- | ---------------- | ----------- |
| IDOR        | Ownership checks | Implemented |
| Role bypass | RBAC middleware  | Implemented |

## Security Controls Mapping

| Control             | OWASP | Implementation               |
| ------------------- | ----- | ---------------------------- |
| Input validation    | A05   | Zod schemas on all endpoints |
| Authentication      | A07   | Argon2 + JWT + session       |
| Authorization       | A01   | RBAC middleware              |
| Security headers    | A02   | Helmet middleware            |
| Dependency security | A03   | npm audit + Snyk             |

## Review Schedule

- Quarterly review of threat model
- After significant architecture changes
- After security incidents
```

**Insecure Pattern**:

```markdown
# DON'T: Skip threat modeling

"We'll add security later"
"It's internal only, doesn't need security"

# DON'T: Create and forget

# Threat model from 2019, never updated

# DON'T: Generic threats without mitigations

## Threats

- SQL injection
- XSS
- CSRF

# (No details on how they're addressed)
```

---

### tsdoc-comments

- **Severity**: medium
- **OWASP**: A06 (Insecure Design)

**Risk**: Missing documentation for security-critical code leads to incorrect usage, bypassed controls, and regression when maintaining code.

**Secure Pattern**:

````typescript
/**
 * Validates and sanitizes user input for the registration endpoint.
 *
 * @security This function is a security boundary. All user input must
 * pass through this validation before being used elsewhere.
 *
 * @param input - Raw user input from request body
 * @returns Validated and sanitized user data
 * @throws {ValidationError} If input fails validation
 *
 * @example
 * ```typescript
 * const user = validateRegistrationInput(req.body);
 * // user is now safe to use
 * ```
 */
export function validateRegistrationInput(input: unknown): ValidatedUser {
  // Implementation
}

/**
 * Hashes a password using Argon2id.
 *
 * @security Uses Argon2id with secure parameters (64MB memory, 3 iterations).
 * Never log the input password or the resulting hash.
 *
 * @param password - Plain text password (will be cleared from memory)
 * @returns Argon2id hash string
 *
 * @see https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
 */
export async function hashPassword(password: string): Promise<string> {
  // Implementation
}

/**
 * Middleware that checks if the user has the required permission.
 *
 * @security This is an authorization control. Must be applied to all
 * protected routes. Fails closed (denies access on any error).
 *
 * @param permission - Required permission string
 * @returns Express middleware function
 *
 * @example
 * ```typescript
 * app.delete('/users/:id', requirePermission('users:delete'), handler);
 * ```
 */
export function requirePermission(permission: Permission): RequestHandler {
  // Implementation
}

/**
 * Reads a file from the uploads directory.
 *
 * @security Prevents path traversal by:
 * 1. Using basename to strip directory components
 * 2. Resolving full path within allowed directory
 * 3. Verifying resolved path is within allowed directory
 *
 * @param filename - User-provided filename (will be sanitized)
 * @returns File contents as Buffer
 * @throws {PathValidationError} If path traversal is detected
 */
export async function readUploadedFile(filename: string): Promise<Buffer> {
  // Implementation
}
````

**Insecure Pattern**:

```typescript
// DON'T: Skip documentation on security code
export function validateInput(input: unknown) {
  // What does this validate? How should it be used?
}

// DON'T: Incomplete security documentation
/**
 * Hashes password
 */
export function hashPassword(password: string) {
  // What algorithm? What parameters? Is it secure?
}

// DON'T: No examples for security-critical APIs
/**
 * Checks permissions
 */
export function checkAuth(user: User, resource: Resource) {
  // How should this be used? What does it return on failure?
}
```
