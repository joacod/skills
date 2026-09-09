# Spec quality checklist

Run this pass after creating or updating the package. Fix material failures
before finishing. Do not start implementation to satisfy a checklist item.

## Package integrity

- [ ] The project lives in its own directory, using the repository's docs
      convention when one exists, otherwise `docs/<project-slug>/`.
- [ ] The slug is short, filesystem-safe, and matches the project identity.
- [ ] Existing spec files were read and updated rather than duplicated.
- [ ] Completed history was preserved; finished versions were not rewritten as
      if the new plan had always existed.
- [ ] `STATUS.md` matches what exists today, including `Last updated`.
- [ ] The documentation map in `README.md` matches the files that were written
      or honestly omitted.

## Brief and scope

- [ ] The brief matches the roadmap.
- [ ] Principles are project-specific, not a pasted manifesto.
- [ ] Non-goals block obvious scope creep.
- [ ] Product/experience is described independently from implementation.
- [ ] Important references and URLs were preserved, with borrow/don't-copy notes
      for material sources.

## Architecture

- [ ] Existing repository infrastructure is reused where sensible.
- [ ] Speculative architecture is labeled PROVISIONAL, HYPOTHESIS,
      NEEDS EXPERIMENT, or FUTURE POSSIBILITY.
- [ ] Known risks are documented.
- [ ] Premature abstractions are called out explicitly.
- [ ] Uncertain brainstorm ideas were not converted into accepted decisions.

## V0 and tasks

- [ ] V0 is genuinely small and useful.
- [ ] V0 tests an important assumption rather than shrinking every final
      feature.
- [ ] V0 does not require later-version infrastructure.
- [ ] Every V0 task contributes directly to V0.
- [ ] Near-term tasks are sized for a focused coding-agent session.
- [ ] Acceptance criteria are objective.
- [ ] Verification steps are real for this repository, not a generic list.
- [ ] Far-future versions remain directional.

## Handoff quality

- [ ] A capable but less intelligent model can execute V0-T01 from the task
      writeup plus `README.md` and `STATUS.md`.
- [ ] `07-agent-handoff.md` tells a future agent what to read, what not to
      invent, and how to report completion.
- [ ] The conversational reply follows the final-response contract in
      `SKILL.md`, then stops.

## Stop condition

If any item above failed, fix the documentation. Do not compensate by writing
code, scaffolding a framework, or implementing V0.
