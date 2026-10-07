---
name: ticket-to-pr
description: >
  Explicit manual invocation only. With no other text, ship the current work:
  on the default branch, create a branch from the related uncommitted changes
  and open a pull request; on any other branch, commit, push, and update that
  branch's pull request so its title and body cover the whole branch. Text
  after the invocation overrides that default. Do not run this workflow unless
  the user invoked the skill.
user-invocable: true
disable-model-invocation: true
---

# Ticket to PR

## Activation

A manual invocation through the harness's native skill-command mechanism is a
complete request. Skill command syntax is host-specific. This skill does not
define a portable slash or sigil prefix. When a harness drops the command text
and supplies only this skill, that is a bare invocation.

Use the bare-invocation procedure only when the invocation has no other text.
Text after the invocation is an explicit request and takes precedence. Follow
it for what to change, which changes to include, the branch, the base, and the
pull request. Use the bare procedure only for a choice that text leaves open.
A label with no direction, such as a ticket name, leaves those choices open
and becomes the summary.

Apply this workflow only when the user invoked the skill. Finish in this turn,
then stop. On success, the last thing you report is the pull request URL.

## Inspect

Before editing files, determine the current branch, the repository default
branch, uncommitted and untracked changes, commits on this branch that are not
on the default branch, and whether an open pull request already exists
(`gh pr view`).

## Bare invocation

The sections below apply when the invocation has no other text.

### Default branch

When the current branch is the default branch, create a new branch from it.
Creating the branch keeps the working tree.

Name it from a documented repository convention. Otherwise use
`<type>/<short-kebab-case-description>` with a type such as
`feat`, `fix`, `docs`, `refactor`, `test`, or `chore`, for example
`feat/csv-export`. Add an agent-name prefix only when the user asks for one.

Commit the uncommitted changes that belong to this work, including related
untracked files. Leave unrelated dirty paths unstaged and list them. Derive
the summary from the diff.

When the default branch is clean, report that there is nothing to ship and
stop.

### Any other branch

Stay on the current branch. Commit its uncommitted and untracked changes. The
pull request covers every change on this branch relative to its base, including
commits already on the branch.

A clean branch with an open pull request needs no empty commit. Push when the
remote is behind, and update the pull request when its title or body does not
cover the branch.

## With other text

Follow the invocation text. Implement work it asks for, on the branch and base
it names, and include only the changes it scopes. Add no separate planning,
architecture, review, subagent, or workflow-state layer.

Then commit, push, and create or update the pull request. Where the text is
silent, use the bare-invocation procedure for that choice.

## Commits

Use one commit for a small cohesive change. Split only independent slices, and
keep coupled implementation and tests together. Follow a repository commit
convention when one exists; otherwise use a short imperative subject. Leave
secrets such as `.env` files and credentials unstaged and name them.

## Push and pull request

Push without force and without rewriting history.

When `gh pr view` finds an open pull request, update its title and body with
`gh pr edit`. Otherwise create one with `gh`. On a new branch from the default
branch, the pull request base is the default branch unless this invocation
named another base. On any other branch, leave the existing pull request base
unchanged.

Use a repository pull-request template when one clearly applies. Otherwise
write a concise title and body: resulting behavior, meaningful implementation
details, and validation that was actually run. Keep a ticket identifier that
was supplied in the invocation or already present on the pull request.

Never merge, enable auto-merge, monitor CI, or delete the branch.

When `gh` authentication, a merge conflict, or detached `HEAD` blocks the run,
report the current branch and any paths still uncommitted, then stop.
