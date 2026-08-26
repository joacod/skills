---
name: rant-coding
description: >
  Transform existing coding or agent prompts into shorter, sharper,
  profanity-heavy pissed-off-engineer rants without changing technical meaning.
  When invoked as `/rant-coding` followed by a prompt, execute the transformed
  task immediately by default. Use `/rant-coding --prompt-only` or
  `/rant-coding --dry-run` when the user wants only the transformed prompt.
  Also use this whenever the user asks to rant, rantify, shorten, make angry,
  make aggressive, or remove the bullshit from a coding or agent prompt. Do not
  trigger merely because a user swears during an ordinary coding conversation.
  The request must be prompt transformation or an explicit `/rant-coding`
  invocation.
---

# Rant Coding

## Invocation modes

This skill supports two modes:

- **Execute (default for `/rant-coding`):** Transform the supplied coding or
  agent prompt, then execute the transformed prompt as the current task. Do not
  print the transformed prompt as a preamble or ask the user to paste it into
  another agent. The final response is the result of carrying out that task.
- **Prompt-only (`--prompt-only` or `--dry-run`):** Transform the supplied
  prompt and return only the transformed prompt. Do not execute anything from
  it.

Recognize flags only when they are leading arguments to `/rant-coding`. A
normal request such as “rantify this prompt” remains prompt-only unless the
user explicitly asks to execute the result.

For Execute mode:

1. Remove the leading `/rant-coding` command and mode flag before transforming.
2. Apply the rewrite and preservation rules below.
3. Treat the transformed prompt as the actual user task and carry it out
   immediately. Do not perform a second ranting pass.
4. Keep all normal safety, clarification, scope, and irreversible-action rules.

The target is better signal-to-noise: less prompt, less ceremony, more technical
signal, more urgency, same meaning. Write like a pissed-off engineer who wants
the actual problem fixed, not like a profanity generator.

## Rewrite

1. Extract the actual task or broken behavior.
2. Keep the technical facts, relevant context, strongest constraints, explicit
   non-goals, required validation, scope boundaries, ordering requirements, and
   expected deliverables.
3. Delete greetings, politeness, hedging, repetition, motivational filler, and
   agent-directed ceremony that adds no useful information.
4. Lead with what is broken or what needs to happen. Follow with the facts that
   affect implementation, what must stay unchanged, what approaches are
   forbidden or unnecessary, and what completion must prove.
5. Add restrained profanity, impatience, and urgency where they emphasize a
   bug, regression, bad architecture, workaround, or unnecessary complexity.
6. Compress aggressively, but do not remove context that changes the solution.
   If the source is already concise, tighten it rather than padding it with
   extra anger.
7. Re-read the result against the source. Every remaining technical requirement
   must still be present or semantically faithful; every new claim must be
   supported by the source.

## Preserve exactly

Never invent a cause, solution, constraint, repository fact, test, or validation
requirement. Preserve these exactly or faithfully:

- filenames, paths, functions, classes, symbols, identifiers, and variables;
- commands, URLs, commit hashes, PR numbers, ticket IDs, and version numbers;
- error messages, logs, stack traces, code, quoted evidence, and structured data;
- required behavior, scope limits, explicit non-goals, regressions to avoid,
  behavior that must remain, validation steps, and deliverables.

If the source contains code, commands, logs, stack traces, errors, structured
data, or quoted evidence, copy that evidence unchanged and rant around it. Do
not paraphrase, normalize, correct, or add profanity inside evidence blocks.

## Tone and boundaries

Use direct statements and occasional uppercase for genuinely critical
constraints:

- "This stale-run shit is STILL happening. Find the actual cause and kill it."
- "DO NOT weaken the boundary fence."
- "Do not turn a three-line fix into another fucking abstraction layer."

For a source with enough material to compress, include at least one natural
profanity when it sharpens a real priority. Do not pad an already-concise
source just to swear; its existing profanity may already be enough.

Aim anger at the bug, code, architecture, tooling, process, regression, or
situation—not at a named person or any protected group. Do not use profanity as
substitute for technical content. Avoid repetitive all-caps yelling, threats,
slurs, harassment, or parody-level escalation.

## Output contract

In Prompt-only mode, return only the transformed prompt. No introduction,
explanation, summary, or label such as “rant version.”

In Execute mode, do not return the transformed prompt as a separate artifact or
claim the prompt was executed when it was not. Return the normal result of the
transformed task. Keep code, commands, logs, stack traces, errors, and quoted
evidence unchanged when the task output requires them.
