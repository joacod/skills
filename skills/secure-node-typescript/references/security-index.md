# Security Guidelines Index

Master index of all security guidelines with OWASP Top 10 mapping for quick reference and filtering.

## OWASP Top 10 (2025) Reference

| ID  | Category                              | Description                                          |
| --- | ------------------------------------- | ---------------------------------------------------- |
| A01 | Broken Access Control                 | Authorization failures, privilege escalation, SSRF   |
| A02 | Security Misconfiguration             | Default configs, verbose errors, missing headers     |
| A03 | Software Supply Chain Failures        | Vulnerable dependencies, compromised packages, CI/CD |
| A04 | Cryptographic Failures                | Weak crypto, exposed secrets, missing encryption     |
| A05 | Injection                             | SQL, NoSQL, OS command, LDAP injection               |
| A06 | Insecure Design                       | Missing security controls, threat modeling gaps      |
| A07 | Identification & Authentication       | Weak passwords, session issues, credential stuffing  |
| A08 | Software & Data Integrity Failures    | Untrusted deserialization, CI/CD compromise          |
| A09 | Logging & Monitoring Failures         | Missing audit logs, log injection, no monitoring     |
| A10 | Mishandling of Exceptional Conditions | Improper error handling, unhandled exceptions        |

---

## Guidelines by Category

### TypeScript Safety

| Guideline ID          | Severity | OWASP | Reference File       |
| --------------------- | -------- | ----- | -------------------- |
| strict-typescript     | high     | A06   | typescript-safety.md |
| no-any-type           | high     | A06   | typescript-safety.md |
| access-modifiers      | medium   | A01   | typescript-safety.md |
| readonly-properties   | medium   | A06   | typescript-safety.md |
| node-protocol-imports | medium   | A03   | typescript-safety.md |
| freeze-globals        | medium   | A05   | typescript-safety.md |
| typed-async-functions | medium   | A06   | typescript-safety.md |

### Input Validation

| Guideline ID           | Severity | OWASP | Reference File      |
| ---------------------- | -------- | ----- | ------------------- |
| schema-validation      | critical | A05   | input-validation.md |
| allowlist-validation   | critical | A05   | input-validation.md |
| sanitize-outputs       | critical | A05   | input-validation.md |
| body-size-limit        | high     | A02   | input-validation.md |
| content-type-check     | medium   | A02   | input-validation.md |
| url-validation         | high     | A01   | input-validation.md |
| json-schema-validation | high     | A05   | input-validation.md |

### Authentication

| Guideline ID          | Severity | OWASP    | Reference File    |
| --------------------- | -------- | -------- | ----------------- |
| argon2-hashing        | critical | A04, A07 | authentication.md |
| secure-cookies        | critical | A07      | authentication.md |
| jwt-validation        | critical | A07      | authentication.md |
| rbac-implementation   | high     | A01      | authentication.md |
| mfa-support           | high     | A07      | authentication.md |
| typed-tokens          | medium   | A07      | authentication.md |
| oauth2-implementation | high     | A07      | authentication.md |

### HTTP Security

| Guideline ID           | Severity | OWASP | Reference File   |
| ---------------------- | -------- | ----- | ---------------- |
| helmet-middleware      | high     | A02   | http-security.md |
| disable-legacy-headers | medium   | A02   | http-security.md |
| hpp-middleware         | medium   | A05   | http-security.md |
| rate-limiting          | high     | A02   | http-security.md |
| exponential-backoff    | medium   | A07   | http-security.md |
| sri-hashes             | medium   | A08   | http-security.md |
| csp-policy             | high     | A02   | http-security.md |
| cors-configuration     | high     | A02   | http-security.md |

### Runtime Safety

| Guideline ID          | Severity | OWASP | Reference File    |
| --------------------- | -------- | ----- | ----------------- |
| no-eval               | critical | A05   | runtime-safety.md |
| safe-child-process    | critical | A05   | runtime-safety.md |
| vm-sandboxing         | high     | A05   | runtime-safety.md |
| object-freeze         | medium   | A05   | runtime-safety.md |
| frozen-intrinsics     | medium   | A05   | runtime-safety.md |
| async-await-patterns  | medium   | A06   | runtime-safety.md |
| event-loop-monitoring | medium   | A02   | runtime-safety.md |

### Filesystem & Paths

| Guideline ID          | Severity | OWASP    | Reference File      |
| --------------------- | -------- | -------- | ------------------- |
| path-sanitization     | critical | A01, A05 | filesystem-paths.md |
| whitelist-directories | high     | A01      | filesystem-paths.md |
| path-normalization    | high     | A01      | filesystem-paths.md |
| typed-paths           | medium   | A06      | filesystem-paths.md |
| safe-regex            | high     | A02      | filesystem-paths.md |
| regex-validation      | medium   | A02      | filesystem-paths.md |

### Dependencies

| Guideline ID        | Severity | OWASP    | Reference File  |
| ------------------- | -------- | -------- | --------------- |
| pin-versions        | high     | A03, A08 | dependencies.md |
| type-safe-libraries | medium   | A03      | dependencies.md |
| npm-audit           | high     | A03      | dependencies.md |
| snyk-integration    | high     | A03      | dependencies.md |
| no-experimental     | medium   | A03      | dependencies.md |
| lockfile-integrity  | high     | A08      | dependencies.md |

### Error Handling & Logging

| Guideline ID          | Severity | OWASP    | Reference File   |
| --------------------- | -------- | -------- | ---------------- |
| global-error-handlers | high     | A02, A10 | error-logging.md |
| custom-error-types    | medium   | A06, A10 | error-logging.md |
| structured-logging    | high     | A09      | error-logging.md |
| hide-error-details    | high     | A02      | error-logging.md |
| no-sensitive-logging  | critical | A09      | error-logging.md |

### Secrets & Configuration

| Guideline ID      | Severity | OWASP | Reference File       |
| ----------------- | -------- | ----- | -------------------- |
| env-variables     | critical | A04   | authentication.md    |
| secret-management | critical | A04   | authentication.md    |
| encrypt-secrets   | high     | A04   | authentication.md    |
| typed-config      | medium   | A02   | typescript-safety.md |

### Operational

| Guideline ID     | Severity | OWASP | Reference File |
| ---------------- | -------- | ----- | -------------- |
| eslint-security  | high     | A06   | operational.md |
| static-analysis  | high     | A06   | operational.md |
| pre-commit-hooks | medium   | A06   | operational.md |
| threat-modeling  | high     | A06   | operational.md |
| tsdoc-comments   | medium   | A06   | operational.md |
| ci-cd-security   | high     | A08   | operational.md |

---

## Guidelines by Severity

### Critical (Must Fix Immediately)

| Guideline ID         | Category         | OWASP    |
| -------------------- | ---------------- | -------- |
| schema-validation    | Input Validation | A05      |
| allowlist-validation | Input Validation | A05      |
| sanitize-outputs     | Input Validation | A05      |
| argon2-hashing       | Authentication   | A04, A07 |
| secure-cookies       | Authentication   | A07      |
| jwt-validation       | Authentication   | A07      |
| no-eval              | Runtime          | A05      |
| safe-child-process   | Runtime          | A05      |
| path-sanitization    | Filesystem       | A01, A05 |
| env-variables        | Secrets          | A04      |
| secret-management    | Secrets          | A04      |
| no-sensitive-logging | Logging          | A09      |

### High

| Guideline ID          | Category         | OWASP    |
| --------------------- | ---------------- | -------- |
| strict-typescript     | TypeScript       | A06      |
| no-any-type           | TypeScript       | A06      |
| body-size-limit       | Input Validation | A02      |
| url-validation        | Input Validation | A01      |
| rbac-implementation   | Authentication   | A01      |
| mfa-support           | Authentication   | A07      |
| helmet-middleware     | HTTP             | A02      |
| rate-limiting         | HTTP             | A02      |
| vm-sandboxing         | Runtime          | A05      |
| whitelist-directories | Filesystem       | A01      |
| path-normalization    | Filesystem       | A01      |
| safe-regex            | Filesystem       | A02      |
| pin-versions          | Dependencies     | A03, A08 |
| npm-audit             | Dependencies     | A03      |
| global-error-handlers | Error Handling   | A02, A10 |
| structured-logging    | Logging          | A09      |
| hide-error-details    | Error Handling   | A02      |
| encrypt-secrets       | Secrets          | A04      |
| eslint-security       | Operational      | A06      |
| static-analysis       | Operational      | A06      |
| threat-modeling       | Operational      | A06      |
| ci-cd-security        | Operational      | A08      |

### Medium

| Guideline ID           | Category         | OWASP    |
| ---------------------- | ---------------- | -------- |
| access-modifiers       | TypeScript       | A01      |
| readonly-properties    | TypeScript       | A06      |
| node-protocol-imports  | TypeScript       | A03      |
| freeze-globals         | TypeScript       | A05      |
| typed-async-functions  | TypeScript       | A06      |
| content-type-check     | Input Validation | A02      |
| typed-tokens           | Authentication   | A07      |
| disable-legacy-headers | HTTP             | A02      |
| hpp-middleware         | HTTP             | A05      |
| exponential-backoff    | HTTP             | A07      |
| sri-hashes             | HTTP             | A08      |
| object-freeze          | Runtime          | A05      |
| frozen-intrinsics      | Runtime          | A05      |
| async-await-patterns   | Runtime          | A06      |
| event-loop-monitoring  | Runtime          | A02      |
| typed-paths            | Filesystem       | A06      |
| regex-validation       | Filesystem       | A02      |
| type-safe-libraries    | Dependencies     | A03      |
| no-experimental        | Dependencies     | A03      |
| custom-error-types     | Error Handling   | A06, A10 |
| typed-config           | Secrets          | A02      |
| pre-commit-hooks       | Operational      | A06      |
| tsdoc-comments         | Operational      | A06      |

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
