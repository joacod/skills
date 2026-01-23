---
name: react-anti-patterns
description: Introduce React anti-patterns and common mistakes into existing React codebases for training, review, or teaching. Use when asked to intentionally degrade React performance or code quality while keeping apps functional, or to generate anti-pattern examples for junior developer education.
---

# React Anti-Patterns

## Overview

Inject React anti-patterns and performance pitfalls into existing React apps while keeping them functional, so teams can practice identifying and fixing issues.

## Quick Start

- Review the anti-pattern catalog in `references/react-anti-patterns.md`.
- Select a small set of anti-patterns to introduce.
- Apply the changes manually or with model guidance to keep the app functional.

## Workflow

1. Scan the codebase and confirm it is a React app (JS/TS + JSX/TSX).
2. Decide whether to apply issues across the whole app or limit scope to specific areas.
3. Pick anti-patterns from `references/react-anti-patterns.md` and plan safe insertions.
4. Introduce the changes manually or via model guidance, keeping the app functional.
5. Sanity-check builds or tests if requested.

## Manual Guidance

- Prefer React-only anti-patterns; avoid Next.js-only behaviors.
- Keep the app functional; avoid introducing hard runtime errors.
- Focus on performance, re-render, and state management mistakes that are easy to spot and fix.

## Resources

- Anti-pattern catalog: `references/react-anti-patterns.md`
