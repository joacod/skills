---
name: ticket-to-pr
description: >
  Explicit-invocation-only wrapper for the literal `/ticket-to-pr <ticket>`
  command. Never activate for ordinary coding, ticket, branch, commit, push, or
  pull-request requests, even when they describe the same work. When that exact
  command is invoked, treat everything after `/ticket-to-pr` as the ticket,
  create a ticket branch, let the active harness implement it normally, make
  sensible commits, push the branch, create a GitHub pull request with `gh`,
  report its URL, and stop.
---

# Ticket to PR

## Activation

Run these instructions only when the user's actual invocation is the literal
`/ticket-to-pr <ticket>`. Do not infer invocation from intent or wording. If the
literal command is absent, decline this skill immediately and do not create or
modify branches, commits, pushes, or pull requests.

Treat everything after `/ticket-to-pr` as the ticket. Keep this skill active for
that ticket only until its pull request is created.

## Branch

Before changing ticket-related files, inspect the current branch and the
repository's default branch.

- If the current branch is the default branch, create a new ticket branch from
  it and continue.
- If the current branch is not the default branch, ask exactly: "Should the new
  ticket branch be based on the current branch or the repository's default
  branch?" Do not switch away from or rewrite the existing branch until the user
  answers. Use the selected branch as the new branch's base and as the pull
  request's base.
- Choose a short, descriptive branch name. Use a type that matches the work and
  follow a clear repository convention when one exists; otherwise use a concise
  kebab-case description, such as `feat/csv-export` or
  `fix/stale-session-recovery`.

## Implement and commit

After creating the branch, let the active harness implement the ticket normally.
Do not add a separate planning, architecture, testing, validation, review,
subagent, orchestration, or workflow-state layer.

Commit coherent completed parts when they make the history easier to understand.
A small cohesive task normally gets one commit; use multiple commits only for
meaningful independent slices. Keep tightly coupled implementation and tests
together. Follow repository commit conventions when they exist; otherwise use a
short imperative subject without an essay-like body or process narration. Stage
only ticket changes and leave unrelated pre-existing changes out of the commits.

## Push and pull request

After the harness completes the ticket, ensure all intended changes are
committed, push the ticket branch, and create the pull request with `gh`. Use an
existing repository pull-request template when one clearly applies. Otherwise,
use a concise title and description focused only on the resulting behavior and
meaningful implementation details; do not add sections for validation, tests,
review, agent activity, plans, commit plans, or workflow metadata.

Never merge, enable auto-merge, monitor CI, or clean up the branch. After the pull
request is successfully created, report its URL and stop.
