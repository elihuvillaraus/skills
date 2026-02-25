# PRD: [Feature Name]

**Status**: 🔴 NOT STARTED
**Branch**: `feature/<branch-name>`
**Author**: Architect Agent
**Date**: YYYY-MM-DD
**Description**: One-line summary of what this PRD delivers.

## Tech Stack

- **Runtime**: (e.g., Next.js 15, Expo 54)
- **Language**: TypeScript
- **Key Libs**: (list specific libraries needed)

## Quality Gates

Commands that MUST pass for every user story:

```bash
# Example - adjust per project
pnpm typecheck
pnpm lint
```

## Context

Brief technical context. Reference existing files, patterns, or architecture the developer needs to understand. Include links to source-of-truth files.

## User Stories

### Priority 1: [Category Name]

> Tasks in this group are **independent** and can run in parallel.

- [ ] **US001: [Task Title]**
  - **Story**: As a [role], I want [feature] so that [benefit]
  - **Files**: `path/to/file.ts`, `path/to/other.ts`
  - **Technical Specs**:
    - Step-by-step implementation with code examples
    - Types/interfaces to create or modify
    - Function signatures with parameters and return types
    - Import paths for existing utilities
  - **Acceptance Criteria**:
    - [ ] Specific, verifiable criterion
    - [ ] Another criterion
    - [ ] Quality gates pass

- [ ] **US002: [Task Title]**
  - **Story**: As a [role], I want [feature] so that [benefit]
  - **Files**: `path/to/different-file.ts`
  - **Technical Specs**:
    - (detailed implementation guide)
  - **Acceptance Criteria**:
    - [ ] Criterion
    - [ ] Quality gates pass

### Priority 2: [Category Name]

> Depends on Priority 1 completion. Tasks in this group are **independent** of each other.

- [ ] **US003: [Task Title]**
  - **Story**: As a [role], I want [feature] so that [benefit]
  - **Files**: `path/to/file.ts` (may now use types from US001)
  - **Technical Specs**:
    - (detailed implementation guide)
  - **Acceptance Criteria**:
    - [ ] Criterion
    - [ ] Quality gates pass

### Priority 3: [Integration / Polish]

> Depends on Priority 2. Often involves connecting pieces built in earlier priorities.

- [ ] **US004: [Task Title]**
  - (same structure)

## Non-Goals

- What this PRD explicitly does NOT cover
- Features deferred to future work
