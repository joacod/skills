# Anti-Patterns Index

Master index of all available anti-patterns with metadata for quick reference and filtering.

## Categories

### React Categories

| ID            | Description                                 |
| ------------- | ------------------------------------------- |
| `rerender`    | Re-render and memoization issues            |
| `state`       | State management anti-patterns              |
| `effect`      | useEffect misuse                            |
| `list`        | List rendering issues                       |
| `conditional` | Conditional rendering bugs                  |
| `data`        | Client-side data fetching/processing issues |

### Next.js Categories

| ID          | Description                        |
| ----------- | ---------------------------------- |
| `waterfall` | Sequential async operations        |
| `bundle`    | Bundle size problems               |
| `boundary`  | Server/client boundary issues      |
| `actions`   | Server Actions security/validation |
| `rsc`       | React Server Component misuse      |

---

## React Patterns

### Junior Level

| Pattern ID                   | Category    | Impact      | Detectability | File            |
| ---------------------------- | ----------- | ----------- | ------------- | --------------- |
| list-keys-index              | list        | bug         | easy          | react/junior.md |
| conditional-render-zero      | conditional | visual      | easy          | react/junior.md |
| inline-handlers-simple       | rerender    | performance | easy          | react/junior.md |
| missing-key-prop             | list        | bug         | easy          | react/junior.md |
| state-object-mutation        | state       | bug         | easy          | react/junior.md |
| state-array-mutation         | state       | bug         | easy          | react/junior.md |
| useeffect-no-cleanup         | effect      | bug         | easy          | react/junior.md |
| props-spreading-uncontrolled | state       | bug         | easy          | react/junior.md |

### Semi-Senior Level

| Pattern ID                | Category | Impact      | Detectability | File                 |
| ------------------------- | -------- | ----------- | ------------- | -------------------- |
| usememo-inline-defeat     | rerender | performance | moderate      | react/semi-senior.md |
| usecallback-stale-closure | state    | bug         | moderate      | react/semi-senior.md |
| effect-missing-deps       | effect   | bug         | moderate      | react/semi-senior.md |
| effect-object-deps        | effect   | performance | moderate      | react/semi-senior.md |
| lazy-init-expensive       | state    | performance | moderate      | react/semi-senior.md |
| context-value-unstable    | rerender | performance | moderate      | react/semi-senior.md |
| derived-state-sync        | state    | performance | moderate      | react/semi-senior.md |
| ref-in-render             | state    | bug         | moderate      | react/semi-senior.md |
| map-filter-chain          | data     | performance | moderate      | react/semi-senior.md |
| async-effect-unhandled    | effect   | bug         | moderate      | react/semi-senior.md |

### Senior Level

| Pattern ID                 | Category | Impact      | Detectability | File            |
| -------------------------- | -------- | ----------- | ------------- | --------------- |
| sync-storage-render        | data     | performance | hard          | react/senior.md |
| duplicate-global-listeners | effect   | performance | hard          | react/senior.md |
| memo-without-comparison    | rerender | performance | hard          | react/senior.md |
| useeffect-as-onchange      | effect   | performance | hard          | react/senior.md |
| provider-rerenders-all     | rerender | performance | hard          | react/senior.md |
| forwardref-inline-render   | rerender | performance | hard          | react/senior.md |
| flushsync-overuse          | state    | performance | hard          | react/senior.md |
| key-remount-abuse          | state    | performance | hard          | react/senior.md |

---

## Next.js Patterns

### Junior Level

| Pattern ID            | Category | Impact      | Detectability | File             |
| --------------------- | -------- | ----------- | ------------- | ---------------- |
| use-client-overuse    | boundary | performance | easy          | nextjs/junior.md |
| image-no-optimization | bundle   | performance | easy          | nextjs/junior.md |
| link-with-a-tag       | bundle   | performance | easy          | nextjs/junior.md |
| metadata-in-client    | boundary | bug         | easy          | nextjs/junior.md |
| env-client-exposure   | boundary | security    | easy          | nextjs/junior.md |

### Semi-Senior Level

| Pattern ID                | Category  | Impact      | Detectability | File                  |
| ------------------------- | --------- | ----------- | ------------- | --------------------- |
| sequential-server-fetches | waterfall | performance | moderate      | nextjs/semi-senior.md |
| no-dynamic-import         | bundle    | performance | moderate      | nextjs/semi-senior.md |
| layout-data-refetch       | waterfall | performance | moderate      | nextjs/semi-senior.md |
| client-heavy-barrel       | bundle    | performance | moderate      | nextjs/semi-senior.md |
| router-push-in-effect     | rsc       | performance | moderate      | nextjs/semi-senior.md |
| suspense-missing-fallback | rsc       | visual      | moderate      | nextjs/semi-senior.md |

### Senior Level

| Pattern ID                   | Category | Impact      | Detectability | File             |
| ---------------------------- | -------- | ----------- | ------------- | ---------------- |
| server-action-no-auth        | actions  | security    | hard          | nextjs/senior.md |
| server-action-no-validation  | actions  | security    | hard          | nextjs/senior.md |
| over-serialization-props     | boundary | performance | hard          | nextjs/senior.md |
| use-hook-in-server           | boundary | build-error | hard          | nextjs/senior.md |
| revalidate-never-set         | rsc      | bug         | hard          | nextjs/senior.md |
| generatestaticparams-missing | rsc      | performance | hard          | nextjs/senior.md |

---

## Pattern Counts

| Level       | React  | Next.js | Total  |
| ----------- | ------ | ------- | ------ |
| Junior      | 8      | 5       | 13     |
| Semi-Senior | 10     | 6       | 16     |
| Senior      | 8      | 6       | 14     |
| **Total**   | **26** | **17**  | **43** |

---

## Selection Guidelines

### By Amount

- **low** (1-3 patterns): Pick 1-2 from target level, 0-1 from adjacent levels
- **medium** (5-8 patterns): Pick 3-4 from target level, 2-4 from mixed levels
- **high** (10+ patterns): Pick liberally, can include build-error impact patterns

### By Impact Priority

When selecting patterns, prioritize by impact:

1. **security** - Critical issues that must be understood
2. **bug** - Functional problems that cause incorrect behavior
3. **build-error** - Issues that prevent the app from building (high amount only)
4. **performance** - Slowdowns and inefficiencies
5. **visual** - UI glitches without functional impact
