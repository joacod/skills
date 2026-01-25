# Security Guidelines Index

Master index of all security guidelines with OWASP Top 10 mapping for quick reference and filtering.

## OWASP Top 10 (2021) Reference

| ID  | Category                  | Description                                         |
| --- | ------------------------- | --------------------------------------------------- |
| A01 | Broken Access Control     | Authorization failures, privilege escalation        |
| A02 | Cryptographic Failures    | Weak crypto, exposed secrets, missing encryption    |
| A03 | Injection                 | SQL, NoSQL, OS command, LDAP injection              |
| A04 | Insecure Design           | Missing security controls, threat modeling gaps     |
| A05 | Security Misconfiguration | Default configs, verbose errors, missing headers    |
| A06 | Vulnerable Components     | Outdated dependencies with known CVEs               |
| A07 | Authentication Failures   | Weak passwords, session issues, credential stuffing |
| A08 | Data Integrity Failures   | Untrusted deserialization, CI/CD compromise         |
| A09 | Logging Failures          | Missing audit logs, log injection, no monitoring    |
| A10 | SSRF                      | Server-side request forgery, URL validation         |

---

## Guidelines by Category

### TypeScript Safety

| Guideline ID          | Severity | OWASP | Reference File       |
| --------------------- | -------- | ----- | -------------------- |
| strict-typescript     | high     | A04   | typescript-safety.md |
| no-any-type           | high     | A04   | typescript-safety.md |
| access-modifiers      | medium   | A01   | typescript-safety.md |
| readonly-properties   | medium   | A04   | typescript-safety.md |
| node-protocol-imports | medium   | A06   | typescript-safety.md |
| freeze-globals        | medium   | A03   | typescript-safety.md |
| typed-async-functions | medium   | A04   | typescript-safety.md |

### Input Validation

| Guideline ID           | Severity | OWASP | Reference File      |
| ---------------------- | -------- | ----- | ------------------- |
| schema-validation      | critical | A03   | input-validation.md |
| allowlist-validation   | critical | A03   | input-validation.md |
| sanitize-outputs       | critical | A03   | input-validation.md |
| body-size-limit        | high     | A05   | input-validation.md |
| content-type-check     | medium   | A05   | input-validation.md |
| url-validation         | high     | A10   | input-validation.md |
| json-schema-validation | high     | A03   | input-validation.md |

### Authentication

| Guideline ID          | Severity | OWASP    | Reference File    |
| --------------------- | -------- | -------- | ----------------- |
| argon2-hashing        | critical | A02, A07 | authentication.md |
| secure-cookies        | critical | A07      | authentication.md |
| jwt-validation        | critical | A07      | authentication.md |
| rbac-implementation   | high     | A01      | authentication.md |
| mfa-support           | high     | A07      | authentication.md |
| typed-tokens          | medium   | A07      | authentication.md |
| oauth2-implementation | high     | A07      | authentication.md |

### HTTP Security

| Guideline ID           | Severity | OWASP | Reference File   |
| ---------------------- | -------- | ----- | ---------------- |
| helmet-middleware      | high     | A05   | http-security.md |
| disable-legacy-headers | medium   | A05   | http-security.md |
| hpp-middleware         | medium   | A03   | http-security.md |
| rate-limiting          | high     | A05   | http-security.md |
| exponential-backoff    | medium   | A07   | http-security.md |
| sri-hashes             | medium   | A08   | http-security.md |
| csp-policy             | high     | A05   | http-security.md |
| cors-configuration     | high     | A05   | http-security.md |

### Runtime Safety

| Guideline ID          | Severity | OWASP | Reference File    |
| --------------------- | -------- | ----- | ----------------- |
| no-eval               | critical | A03   | runtime-safety.md |
| safe-child-process    | critical | A03   | runtime-safety.md |
| vm-sandboxing         | high     | A03   | runtime-safety.md |
| object-freeze         | medium   | A03   | runtime-safety.md |
| frozen-intrinsics     | medium   | A03   | runtime-safety.md |
| async-await-patterns  | medium   | A04   | runtime-safety.md |
| event-loop-monitoring | medium   | A05   | runtime-safety.md |

### Filesystem & Paths

| Guideline ID          | Severity | OWASP    | Reference File      |
| --------------------- | -------- | -------- | ------------------- |
| path-sanitization     | critical | A01, A03 | filesystem-paths.md |
| whitelist-directories | high     | A01      | filesystem-paths.md |
| path-normalization    | high     | A01      | filesystem-paths.md |
| typed-paths           | medium   | A04      | filesystem-paths.md |
| safe-regex            | high     | A05      | filesystem-paths.md |
| regex-validation      | medium   | A05      | filesystem-paths.md |

### Dependencies

| Guideline ID        | Severity | OWASP    | Reference File  |
| ------------------- | -------- | -------- | --------------- |
| pin-versions        | high     | A06, A08 | dependencies.md |
| type-safe-libraries | medium   | A06      | dependencies.md |
| npm-audit           | high     | A06      | dependencies.md |
| snyk-integration    | high     | A06      | dependencies.md |
| no-experimental     | medium   | A06      | dependencies.md |
| lockfile-integrity  | high     | A08      | dependencies.md |

### Error Handling & Logging

| Guideline ID          | Severity | OWASP | Reference File   |
| --------------------- | -------- | ----- | ---------------- |
| global-error-handlers | high     | A05   | error-logging.md |
| custom-error-types    | medium   | A04   | error-logging.md |
| structured-logging    | high     | A09   | error-logging.md |
| hide-error-details    | high     | A05   | error-logging.md |
| no-sensitive-logging  | critical | A09   | error-logging.md |

### Secrets & Configuration

| Guideline ID      | Severity | OWASP | Reference File       |
| ----------------- | -------- | ----- | -------------------- |
| env-variables     | critical | A02   | authentication.md    |
| secret-management | critical | A02   | authentication.md    |
| encrypt-secrets   | high     | A02   | authentication.md    |
| typed-config      | medium   | A05   | typescript-safety.md |

### Operational

| Guideline ID     | Severity | OWASP | Reference File |
| ---------------- | -------- | ----- | -------------- |
| eslint-security  | high     | A04   | operational.md |
| static-analysis  | high     | A04   | operational.md |
| pre-commit-hooks | medium   | A04   | operational.md |
| threat-modeling  | high     | A04   | operational.md |
| tsdoc-comments   | medium   | A04   | operational.md |
| ci-cd-security   | high     | A08   | operational.md |

---

## Guidelines by Severity

### Critical (Must Fix Immediately)

| Guideline ID         | Category         | OWASP    |
| -------------------- | ---------------- | -------- |
| schema-validation    | Input Validation | A03      |
| allowlist-validation | Input Validation | A03      |
| sanitize-outputs     | Input Validation | A03      |
| argon2-hashing       | Authentication   | A02, A07 |
| secure-cookies       | Authentication   | A07      |
| jwt-validation       | Authentication   | A07      |
| no-eval              | Runtime          | A03      |
| safe-child-process   | Runtime          | A03      |
| path-sanitization    | Filesystem       | A01, A03 |
| env-variables        | Secrets          | A02      |
| secret-management    | Secrets          | A02      |
| no-sensitive-logging | Logging          | A09      |

### High

| Guideline ID          | Category         | OWASP    |
| --------------------- | ---------------- | -------- |
| strict-typescript     | TypeScript       | A04      |
| no-any-type           | TypeScript       | A04      |
| body-size-limit       | Input Validation | A05      |
| url-validation        | Input Validation | A10      |
| rbac-implementation   | Authentication   | A01      |
| mfa-support           | Authentication   | A07      |
| helmet-middleware     | HTTP             | A05      |
| rate-limiting         | HTTP             | A05      |
| vm-sandboxing         | Runtime          | A03      |
| whitelist-directories | Filesystem       | A01      |
| path-normalization    | Filesystem       | A01      |
| safe-regex            | Filesystem       | A05      |
| pin-versions          | Dependencies     | A06, A08 |
| npm-audit             | Dependencies     | A06      |
| global-error-handlers | Error Handling   | A05      |
| structured-logging    | Logging          | A09      |
| hide-error-details    | Error Handling   | A05      |
| encrypt-secrets       | Secrets          | A02      |
| eslint-security       | Operational      | A04      |
| static-analysis       | Operational      | A04      |
| threat-modeling       | Operational      | A04      |
| ci-cd-security        | Operational      | A08      |

### Medium

| Guideline ID           | Category         | OWASP |
| ---------------------- | ---------------- | ----- |
| access-modifiers       | TypeScript       | A01   |
| readonly-properties    | TypeScript       | A04   |
| node-protocol-imports  | TypeScript       | A06   |
| freeze-globals         | TypeScript       | A03   |
| typed-async-functions  | TypeScript       | A04   |
| content-type-check     | Input Validation | A05   |
| typed-tokens           | Authentication   | A07   |
| disable-legacy-headers | HTTP             | A05   |
| hpp-middleware         | HTTP             | A03   |
| exponential-backoff    | HTTP             | A07   |
| sri-hashes             | HTTP             | A08   |
| object-freeze          | Runtime          | A03   |
| frozen-intrinsics      | Runtime          | A03   |
| async-await-patterns   | Runtime          | A04   |
| event-loop-monitoring  | Runtime          | A05   |
| typed-paths            | Filesystem       | A04   |
| regex-validation       | Filesystem       | A05   |
| type-safe-libraries    | Dependencies     | A06   |
| no-experimental        | Dependencies     | A06   |
| custom-error-types     | Error Handling   | A04   |
| typed-config           | Secrets          | A05   |
| pre-commit-hooks       | Operational      | A04   |
| tsdoc-comments         | Operational      | A04   |

---

## Quick Selection Guide

### New Project Setup

Load: `typescript-safety.md`, `dependencies.md`, `operational.md`

Key guidelines: strict-typescript, pin-versions, eslint-security, npm-audit

### API Endpoint Development

Load: `input-validation.md`, `http-security.md`, `error-logging.md`

Key guidelines: schema-validation, helmet-middleware, rate-limiting, hide-error-details

### Authentication Feature

Load: `authentication.md`, `input-validation.md`

Key guidelines: argon2-hashing, secure-cookies, jwt-validation, rbac-implementation

### File Upload/Download

Load: `filesystem-paths.md`, `input-validation.md`

Key guidelines: path-sanitization, whitelist-directories, body-size-limit

### Security Audit/Review

Load all reference files. Prioritize by severity: critical > high > medium.
