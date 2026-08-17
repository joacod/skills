# Report format

Keep the default assessment concise and evidence-based. Use this structure;
omit empty sections only when the user does not need them.

```markdown
# Testing health

**State:** No safety net | Foothold | Partial safety net | Reliable safety net | Strong enough
**Confidence:** Low | Medium | High

## What I found

- Stack and repository shape:
- Existing test infrastructure and commands:
- Commands executed and results:
- CI behavior:
- Representative test-quality observations:
- Important protected and unprotected risks:

## Biggest current risk

<Describe one important weakness, with file, symbol, command, or CI evidence.>

## Recommended pass

<Recommend exactly one coherent pass. State the seam and test level when
relevant. State what is explicitly out of scope.>

## Why this first

<Explain why this reduces more meaningful risk than the obvious alternatives.>

## Done when

- <observable behavior is protected or the reliability/CI defect is repaired>
- <the relevant command passes reliably>
- <CI executes it when in scope>
- <no unnecessary framework, coverage target, or architecture migration was added>

## Later

- <at most three short follow-ups, or “Good enough for now.”>
```

## Wording guidance

Separate facts from inference:

- **Observed:** “`pnpm test --filter api` exited 0 with 18 tests.”
- **Verified statically:** “CI's workflow runs `pytest` on pull requests.”
- **Inferred:** “The checkout boundary is likely the highest-risk seam because
  it combines persistence and payment decisions; no checkout test was found.”

If execution is unavailable, say so directly and lower confidence. Distinguish
failed, skipped, unavailable, and not-applicable checks. Do not write “tests
pass” when only a manifest was read.

Name the chosen state without a numeric score. Coverage and test counts can be
included as supporting facts, but never as the objective or the recommendation.

## Example: no safety net

**State:** No safety net
**Confidence:** Medium

The repository has a Python manifest and a `tests/` directory, but no runnable
test command is documented, no test files contain assertions, and CI does not
invoke a test runner. The smallest valuable pass is to establish the existing
ecosystem's runner and add one test around the public command's important
invalid-input behavior—not to create a full testing pyramid.

## Example: partial safety net

**State:** Partial safety net
**Confidence:** High

The existing suite runs in CI and protects pure pricing rules, but sampled
checkout tests mock the application collaborators and no test crosses the
persistence/payment seam. The next pass is one targeted integration test for a
successful checkout and its failure outcome, reusing the existing test
database or boundary fixture. Do not add more utility tests or set a coverage
 target in this pass.

## Example: strong enough

**State:** Strong enough
**Confidence:** High

Important public workflows, persistence boundaries, and failure paths have
reliable tests at appropriate levels; CI runs the relevant suite and sampled
tests assert outcomes through stable seams. No additional change currently
justifies its maintenance cost. **Good enough for now.**
