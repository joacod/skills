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
- [ ] Desired end state describes the mature product, not only the first slice.
- [ ] `02-product-and-experience.md` is the last form; later-only workflows are
      labeled rather than dropped.
- [ ] Principles are project-specific, not a pasted manifesto.
- [ ] Non-goals block obvious scope creep.
- [ ] Important references and URLs were preserved, with borrow/don't-copy notes
      for material sources.

## Architecture

- [ ] Existing repository infrastructure is reused where sensible.
- [ ] Speculative architecture is labeled PROVISIONAL, HYPOTHESIS,
      NEEDS EXPERIMENT, or FUTURE POSSIBILITY.
- [ ] Known risks are documented.
- [ ] Premature abstractions are called out explicitly.
- [ ] Uncertain brainstorm ideas were not converted into accepted decisions.

## Roadmap and tasks

- [ ] The roadmap runs from the first version through the desired last form.
- [ ] The last roadmap version matches the desired end state.
- [ ] V0 is genuinely small and useful, and tests an important assumption
      rather than shrinking every final feature.
- [ ] V0 does not require later-version infrastructure.
- [ ] Every current-version task contributes directly to that version.
- [ ] Current-version tasks are sized for a focused coding-agent session and
      are executable without the original brainstorm.
- [ ] Acceptance criteria are objective.
- [ ] Verification steps are real for this repository, not a generic list.
- [ ] Far-future versions remain directional but are not omitted or left as
      "TBD".
- [ ] On update, completed work is marked done and the new current version is
      task-split.

## Handoff quality

- [ ] A capable but less intelligent model can execute the current task from
      the task writeup plus the spec files it is told to read.
- [ ] `07-agent-handoff.md` distinguishes current work from destination docs
      and says when to refresh the spec instead of inventing the next version
      during coding.
- [ ] The conversational reply follows the final-response contract in
      `SKILL.md`, then stops.

## Stop condition

If any item above failed, fix the documentation. Do not compensate by writing
code, scaffolding a framework, or implementing V0.
