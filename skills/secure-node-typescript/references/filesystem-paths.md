# Filesystem & Path Safety Guidelines

Prevent path traversal attacks and ensure safe file operations.

---

### path-sanitization

- **Severity**: critical
- **OWASP**: A01 (Broken Access Control), A05 (Injection)

**Risk**: Unsanitized file paths allow attackers to access files outside intended directories using sequences like `../` (path traversal).

**Secure Pattern**:

```typescript
import path from 'node:path'
import fs from 'node:fs/promises'

// DO: Define allowed base directories
const UPLOAD_DIR = '/app/uploads'
const PUBLIC_DIR = '/app/public'

// DO: Sanitize and validate paths
function sanitizePath(userInput: string, baseDir: string): string {
  // Remove null bytes (can bypass checks in some systems)
  const cleaned = userInput.replace(/\0/g, '')

  // Get just the filename, removing any directory components
  const filename = path.basename(cleaned)

  // Resolve the full path within the base directory
  const fullPath = path.resolve(baseDir, filename)

  // Verify the path is within the allowed directory
  if (!fullPath.startsWith(baseDir + path.sep) && fullPath !== baseDir) {
    throw new Error('Path traversal attempt detected')
  }

  return fullPath
}

// DO: Use realpath to resolve symlinks and verify final location
async function safeReadFile(
  userInput: string,
  baseDir: string,
): Promise<string> {
  const sanitizedPath = sanitizePath(userInput, baseDir)

  // Resolve symlinks to get actual path
  const realPath = await fs.realpath(sanitizedPath)

  // Re-verify after symlink resolution
  if (!realPath.startsWith(baseDir + path.sep)) {
    throw new Error('Symlink traversal attempt detected')
  }

  return fs.readFile(realPath, 'utf-8')
}

// DO: Validate file extensions with allowlist
const ALLOWED_EXTENSIONS = new Set(['.jpg', '.jpeg', '.png', '.gif', '.pdf'])

function validateExtension(filename: string): boolean {
  const ext = path.extname(filename).toLowerCase()
  return ALLOWED_EXTENSIONS.has(ext)
}

// Complete secure file read function
async function secureFileRead(
  userFilename: string,
  baseDir: string,
): Promise<Buffer> {
  // Validate extension
  if (!validateExtension(userFilename)) {
    throw new Error('File type not allowed')
  }

  // Sanitize path
  const safePath = sanitizePath(userFilename, baseDir)

  // Check file exists
  try {
    const stat = await fs.stat(safePath)

    if (!stat.isFile()) {
      throw new Error('Not a regular file')
    }
  } catch {
    throw new Error('File not found')
  }

  // Resolve symlinks and re-verify
  const realPath = await fs.realpath(safePath)

  if (!realPath.startsWith(baseDir + path.sep)) {
    throw new Error('Invalid file path')
  }

  return fs.readFile(realPath)
}
```

**Insecure Pattern**:

```typescript
// DON'T: Use user input directly in file paths
app.get('/files/:filename', async (req, res) => {
  const filePath = `/app/files/${req.params.filename}` // Path traversal!
  // filename = "../../../etc/passwd" reads system files!
  const content = await fs.readFile(filePath)
  res.send(content)
})

// DON'T: Only check for ".." without proper resolution
function badSanitize(input: string): string {
  if (input.includes('..')) {
    throw new Error('Invalid path')
  }
  return input // Can be bypassed with encoded sequences
}

// DON'T: Forget to handle symlinks
const safePath = path.resolve(baseDir, filename)
// safePath could be a symlink pointing outside baseDir!
```

---

### whitelist-directories

- **Severity**: high
- **OWASP**: A01 (Broken Access Control)

**Risk**: Without directory whitelisting, file operations could be performed on sensitive system directories or configuration files.

**Secure Pattern**:

```typescript
import path from 'node:path'

// DO: Define explicit directory whitelist
const ALLOWED_DIRECTORIES = Object.freeze({
  uploads: '/app/data/uploads',
  temp: '/app/data/temp',
  exports: '/app/data/exports',
  avatars: '/app/data/avatars',
} as const)

type DirectoryKey = keyof typeof ALLOWED_DIRECTORIES

// DO: Type-safe directory access
function getBaseDir(key: DirectoryKey): string {
  return ALLOWED_DIRECTORIES[key]
}

// DO: Validate directory access before operations
function validateDirectoryAccess(
  requestedPath: string,
  allowedKeys: DirectoryKey[],
): string {
  const resolvedPath = path.resolve(requestedPath)

  for (const key of allowedKeys) {
    const baseDir = ALLOWED_DIRECTORIES[key]

    if (
      resolvedPath.startsWith(baseDir + path.sep) ||
      resolvedPath === baseDir
    ) {
      return resolvedPath
    }
  }

  throw new Error('Access to directory not allowed')
}

// DO: Create directory-scoped file operations
class SecureFileStore {
  constructor(private readonly baseDir: string) {
    // Ensure base directory exists and is absolute
    if (!path.isAbsolute(baseDir)) {
      throw new Error('Base directory must be absolute path')
    }
  }

  private resolvePath(filename: string): string {
    const safeName = path.basename(filename)
    const fullPath = path.join(this.baseDir, safeName)

    if (!fullPath.startsWith(this.baseDir + path.sep)) {
      throw new Error('Invalid filename')
    }

    return fullPath
  }

  async read(filename: string): Promise<Buffer> {
    return fs.readFile(this.resolvePath(filename))
  }

  async write(filename: string, data: Buffer): Promise<void> {
    return fs.writeFile(this.resolvePath(filename), data)
  }

  async delete(filename: string): Promise<void> {
    return fs.unlink(this.resolvePath(filename))
  }
}

// Usage
const uploadStore = new SecureFileStore(ALLOWED_DIRECTORIES.uploads)
await uploadStore.write('user-avatar.jpg', imageBuffer)
```

**Insecure Pattern**:

```typescript
// DON'T: Allow arbitrary directory access
app.get('/read', async (req, res) => {
  const dir = req.query.dir as string
  const file = req.query.file as string
  const content = await fs.readFile(path.join(dir, file)) // No restrictions!
  res.send(content)
})

// DON'T: Use relative paths that could resolve anywhere
const uploadDir = './uploads' // Could be anywhere after resolve()
```

---

### path-normalization

- **Severity**: high
- **OWASP**: A01 (Broken Access Control)

**Risk**: Non-normalized paths with `.`, `..`, or redundant separators can bypass simple string checks and access unintended files.

**Secure Pattern**:

```typescript
import path from 'node:path'

// DO: Always normalize and resolve paths before comparison
function isPathWithinBase(userPath: string, baseDir: string): boolean {
  // Normalize both paths
  const normalizedBase = path.resolve(baseDir)
  const normalizedUser = path.resolve(baseDir, userPath)

  // Compare normalized paths
  return (
    normalizedUser.startsWith(normalizedBase + path.sep) ||
    normalizedUser === normalizedBase
  )
}

// DO: Use path.resolve() instead of path.join() for security checks
function secureJoin(base: string, ...parts: string[]): string {
  // path.resolve handles "..", ".", and normalizes separators
  const resolved = path.resolve(base, ...parts)

  // Verify result is within base
  if (!resolved.startsWith(path.resolve(base) + path.sep)) {
    throw new Error('Path traversal detected')
  }

  return resolved
}

// DO: Handle URL-encoded paths
function decodeAndNormalize(encodedPath: string): string {
  // Decode URL encoding first
  const decoded = decodeURIComponent(encodedPath)

  // Check for null bytes
  if (decoded.includes('\0')) {
    throw new Error('Invalid path: contains null byte')
  }

  // Normalize
  return path.normalize(decoded)
}

// DO: Handle case sensitivity based on platform
function comparePaths(path1: string, path2: string): boolean {
  const normalized1 = path.resolve(path1)
  const normalized2 = path.resolve(path2)

  // On Windows, paths are case-insensitive
  if (process.platform === 'win32') {
    return normalized1.toLowerCase() === normalized2.toLowerCase()
  }

  return normalized1 === normalized2
}
```

**Insecure Pattern**:

```typescript
// DON'T: String comparison without normalization
function badCheck(userPath: string, baseDir: string): boolean {
  return userPath.startsWith(baseDir) // Fails for "/base/dir/../secret"
}

// DON'T: Use path.join() alone for security checks
const joined = path.join(base, userInput)
// path.join doesn't prevent ".." from escaping base

// DON'T: Forget URL decoding
const filename = req.params.file // Could be "%2e%2e%2f" (../)
```

---

### typed-paths

- **Severity**: medium
- **OWASP**: A06 (Insecure Design)

**Risk**: Untyped path handling can lead to confusion between file paths, URLs, and directory paths, causing incorrect security checks.

**Secure Pattern**:

```typescript
// DO: Use branded types for different path types
declare const FilePathBrand: unique symbol
declare const DirPathBrand: unique symbol
declare const RelativePathBrand: unique symbol

type FilePath = string & { [FilePathBrand]: true }
type DirPath = string & { [DirPathBrand]: true }
type RelativePath = string & { [RelativePathBrand]: true }

// DO: Create factory functions that validate paths
function toFilePath(input: string, baseDir: DirPath): FilePath {
  const sanitized = sanitizePath(input, baseDir)

  // Verify it's a file, not a directory
  const stat = fs.statSync(sanitized)
  if (!stat.isFile()) {
    throw new Error('Path is not a file')
  }

  return sanitized as FilePath
}

function toDirPath(input: string): DirPath {
  const resolved = path.resolve(input)

  // Verify it's a directory
  const stat = fs.statSync(resolved)
  if (!stat.isDirectory()) {
    throw new Error('Path is not a directory')
  }

  return resolved as DirPath
}

function toRelativePath(input: string): RelativePath {
  if (path.isAbsolute(input)) {
    throw new Error('Path must be relative')
  }

  // Remove leading slashes and normalize
  const normalized = path.normalize(input).replace(/^[/\\]+/, '')

  return normalized as RelativePath
}

// DO: Use types in function signatures
async function readSecureFile(
  filename: RelativePath,
  baseDir: DirPath,
): Promise<Buffer> {
  const filePath = toFilePath(filename, baseDir)
  return fs.readFile(filePath)
}

// DO: Create path-specific error types
class PathValidationError extends Error {
  constructor(
    message: string,
    public readonly path: string,
    public readonly reason:
      | 'traversal'
      | 'invalid'
      | 'not_found'
      | 'permission',
  ) {
    super(message)
    this.name = 'PathValidationError'
  }
}
```

**Insecure Pattern**:

```typescript
// DON'T: Use plain strings for paths
function readFile(path: string): Promise<Buffer> {
  // Is this a file path? URL? Directory?
  return fs.readFile(path)
}

// DON'T: Mix path types
function process(input: string) {
  const url = new URL(input) // Throws if not URL
  const file = fs.readFileSync(input) // Different interpretation
}
```

---

### safe-regex

- **Severity**: high
- **OWASP**: A02 (Security Misconfiguration)

**Risk**: Regular expressions with nested quantifiers or overlapping patterns can cause catastrophic backtracking (ReDoS), freezing the event loop.

**Secure Pattern**:

```typescript
// DO: Use safe-regex to validate patterns
import safeRegex from 'safe-regex'

function createSafeRegex(pattern: string, flags?: string): RegExp {
  if (!safeRegex(pattern)) {
    throw new Error('Unsafe regex pattern detected')
  }

  return new RegExp(pattern, flags)
}

// DO: Use atomic groups or possessive quantifiers where available
// Note: JavaScript doesn't support these, so use alternatives

// DO: Set timeouts for regex operations
function matchWithTimeout(
  text: string,
  pattern: RegExp,
  timeoutMs: number,
): RegExpMatchArray | null {
  const worker = new Worker(
    `
    const { parentPort, workerData } = require('worker_threads');
    const result = workerData.text.match(new RegExp(workerData.pattern, workerData.flags));
    parentPort.postMessage(result);
  `,
    {
      eval: true,
      workerData: { text, pattern: pattern.source, flags: pattern.flags },
    },
  )

  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      worker.terminate()
      reject(new Error('Regex timeout'))
    }, timeoutMs)

    worker.on('message', (result) => {
      clearTimeout(timeout)
      resolve(result)
    })
  })
}

// DO: Use specific patterns instead of greedy quantifiers
// Instead of: /.*/ use: /[^<]*/
// Instead of: /\s*/ use: /[ \t]*/

// DO: Use non-backtracking alternatives
function validateEmail(email: string): boolean {
  // Simple, fast pattern - not 100% RFC compliant but safe
  const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return pattern.test(email)
}

// For complex validation, use a library like Zod instead of regex
import { z } from 'zod'
const emailSchema = z.string().email()
```

**Insecure Pattern**:

```typescript
// DON'T: Use nested quantifiers
const badPattern = /^(a+)+$/ // Exponential backtracking!
// Test with: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"

// DON'T: Use overlapping alternatives
const badPattern2 = /^(a|a)+$/ // ReDoS vulnerable

// DON'T: Greedy quantifiers with complex groups
const badPattern3 = /^([a-zA-Z]+)*$/ // Catastrophic backtracking

// DON'T: Accept user-provided regex
const userPattern = req.query.pattern as string
const regex = new RegExp(userPattern) // ReDoS from malicious pattern!
```

---

### regex-validation

- **Severity**: medium
- **OWASP**: A02 (Security Misconfiguration)

**Risk**: User-provided regex patterns can contain malicious patterns that cause ReDoS or unexpected matching behavior.

**Secure Pattern**:

```typescript
import safeRegex from 'safe-regex'

// DO: Validate user-provided regex patterns
function validateUserRegex(pattern: string): RegExp {
  // Length limit
  if (pattern.length > 100) {
    throw new Error('Pattern too long')
  }

  // Check for safe regex
  if (!safeRegex(pattern)) {
    throw new Error('Pattern may cause performance issues')
  }

  // Disallow certain dangerous constructs
  const dangerousPatterns = [
    /\(\?.*\)/, // No lookahead/lookbehind
    /\\[dswDSW]/, // Be careful with character classes
  ]

  for (const dangerous of dangerousPatterns) {
    if (dangerous.test(pattern)) {
      throw new Error('Pattern contains disallowed constructs')
    }
  }

  try {
    return new RegExp(pattern)
  } catch (error) {
    throw new Error('Invalid regex pattern')
  }
}

// DO: Use re2 for safe regex execution (no backtracking)
import RE2 from 're2'

function safeMatch(text: string, pattern: string): boolean {
  const re = new RE2(pattern)
  return re.test(text)
}

// DO: Prefer validation libraries over regex
import { z } from 'zod'
import validator from 'validator'

// Instead of regex for common patterns:
const schema = z.object({
  email: z.string().email(),
  url: z.string().url(),
  uuid: z.string().uuid(),
  ip: z.string().ip(),
})

// Or use validator.js
if (validator.isEmail(input)) {
  /* ... */
}
if (validator.isURL(input)) {
  /* ... */
}
```

**Insecure Pattern**:

```typescript
// DON'T: Allow arbitrary user regex
app.get('/search', (req, res) => {
  const pattern = new RegExp(req.query.pattern as string) // ReDoS!
  const results = data.filter((item) => pattern.test(item.name))
  res.json(results)
})

// DON'T: Trust regex from config files without validation
const config = JSON.parse(fs.readFileSync('config.json', 'utf-8'))
const pattern = new RegExp(config.searchPattern) // Could be malicious
```
