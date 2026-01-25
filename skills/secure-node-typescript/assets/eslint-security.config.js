// @ts-check
import js from '@eslint/js'
import tseslint from '@typescript-eslint/eslint-plugin'
import tsparser from '@typescript-eslint/parser'
import security from 'eslint-plugin-security'

/**
 * ESLint configuration for secure Node.js/TypeScript development.
 *
 * Install required dependencies:
 * npm install -D eslint @eslint/js @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-plugin-security
 *
 * Usage:
 * 1. Copy this file to your project root as eslint.config.js
 * 2. Adjust paths and rules as needed
 * 3. Run: npx eslint .
 */
export default [
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx', '**/*.mts', '**/*.cts'],
    languageOptions: {
      parser: tsparser,
      parserOptions: {
        project: './tsconfig.json',
        ecmaVersion: 2022,
        sourceType: 'module',
      },
      globals: {
        // Node.js globals
        process: 'readonly',
        console: 'readonly',
        Buffer: 'readonly',
        __dirname: 'readonly',
        __filename: 'readonly',
        module: 'readonly',
        require: 'readonly',
        exports: 'readonly',
        global: 'readonly',
        setTimeout: 'readonly',
        setInterval: 'readonly',
        setImmediate: 'readonly',
        clearTimeout: 'readonly',
        clearInterval: 'readonly',
        clearImmediate: 'readonly',
      },
    },
    plugins: {
      '@typescript-eslint': tseslint,
      security,
    },
    rules: {
      // =====================================================
      // TypeScript Strict Rules
      // =====================================================

      // Prevent use of 'any' type
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unsafe-argument': 'error',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',

      // Strict boolean expressions
      '@typescript-eslint/strict-boolean-expressions': [
        'error',
        {
          allowString: false,
          allowNumber: false,
          allowNullableObject: false,
          allowNullableBoolean: false,
          allowNullableString: false,
          allowNullableNumber: false,
          allowAny: false,
        },
      ],

      // Async/Promise handling
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
      '@typescript-eslint/await-thenable': 'error',
      '@typescript-eslint/promise-function-async': 'error',
      '@typescript-eslint/require-await': 'error',

      // Type safety
      '@typescript-eslint/no-non-null-assertion': 'error',
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/no-unnecessary-condition': 'error',
      '@typescript-eslint/switch-exhaustiveness-check': 'error',

      // Code quality
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
      ],
      '@typescript-eslint/explicit-function-return-type': [
        'error',
        { allowExpressions: true },
      ],
      '@typescript-eslint/explicit-module-boundary-types': 'error',

      // =====================================================
      // Security Plugin Rules
      // =====================================================

      // Detect buffer operations without assertion
      'security/detect-buffer-noassert': 'error',

      // Detect child_process usage (review required)
      'security/detect-child-process': 'error',

      // Detect disabled mustache escape
      'security/detect-disable-mustache-escape': 'error',

      // Detect eval() with expression
      'security/detect-eval-with-expression': 'error',

      // Detect deprecated Buffer() constructor
      'security/detect-new-buffer': 'error',

      // Detect CSRF middleware order issues
      'security/detect-no-csrf-before-method-override': 'error',

      // Detect non-literal fs calls (warn - review required)
      'security/detect-non-literal-fs-filename': 'warn',

      // Detect non-literal RegExp (warn - review required)
      'security/detect-non-literal-regexp': 'warn',

      // Detect non-literal require
      'security/detect-non-literal-require': 'error',

      // Detect object injection (warn - many false positives)
      'security/detect-object-injection': 'warn',

      // Detect timing attacks (warn - review required)
      'security/detect-possible-timing-attacks': 'warn',

      // Detect pseudorandom bytes (should use crypto)
      'security/detect-pseudoRandomBytes': 'error',

      // Detect unsafe regex (ReDoS)
      'security/detect-unsafe-regex': 'error',

      // =====================================================
      // Built-in Security Rules
      // =====================================================

      // Prevent eval
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'no-new-func': 'error',

      // Prevent script URLs
      'no-script-url': 'error',

      // Prevent with statement
      'no-with': 'error',

      // Require radix for parseInt
      radix: 'error',

      // Prevent comparing to -0
      'no-compare-neg-zero': 'error',

      // Prevent assignment in conditionals
      'no-cond-assign': 'error',

      // Prevent constant conditions
      'no-constant-condition': 'error',

      // Prevent control characters in regex
      'no-control-regex': 'error',

      // Prevent debugger statements
      'no-debugger': 'error',

      // Prevent duplicate case labels
      'no-duplicate-case': 'error',

      // Prevent empty character classes
      'no-empty-character-class': 'error',

      // Prevent reassigning exceptions
      'no-ex-assign': 'error',

      // Prevent unnecessary boolean casts
      'no-extra-boolean-cast': 'error',

      // Prevent reassigning function declarations
      'no-func-assign': 'error',

      // Prevent invalid regex
      'no-invalid-regexp': 'error',

      // Prevent irregular whitespace
      'no-irregular-whitespace': 'error',

      // Prevent calling global objects as functions
      'no-obj-calls': 'error',

      // Prevent returning values from setters
      'no-setter-return': 'error',

      // Prevent sparse arrays
      'no-sparse-arrays': 'error',

      // Prevent unreachable code
      'no-unreachable': 'error',

      // Prevent unsafe finally
      'no-unsafe-finally': 'error',

      // Prevent unsafe negation
      'no-unsafe-negation': 'error',

      // Require isNaN()
      'use-isnan': 'error',

      // Enforce valid typeof comparisons
      'valid-typeof': 'error',
    },
  },
  {
    // Less strict rules for test files
    files: ['**/*.test.ts', '**/*.spec.ts', '**/__tests__/**/*.ts'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-non-null-assertion': 'warn',
      'security/detect-object-injection': 'off',
    },
  },
  {
    // Ignore patterns
    ignores: [
      'node_modules/**',
      'dist/**',
      'build/**',
      'coverage/**',
      '*.config.js',
      '*.config.mjs',
    ],
  },
]
