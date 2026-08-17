# README Quality Checklist

Run this pass after creating or changing the main README. Fix material failures
before completing the task. In review mode, report the findings instead of
editing. Do not publish a numeric score unless the user requests one.

## Immediate comprehension

- [ ] The first screen identifies the project and states a concrete value
      proposition rather than generic praise.
- [ ] A new visitor can tell who the project is for or what situation it serves.
- [ ] The most important links, trust signals, and authentic visual (if any)
      appear before a long explanation.
- [ ] The opening does not require the reader to understand internal names,
      architecture, or project-specific acronyms.

## 60-second onboarding

- [ ] Quick Start is easy to find and presents one obvious supported path.
- [ ] Commands are copy-pasteable and use the repository's real package manager,
      runtime, scripts, entrypoints, flags, and paths.
- [ ] Prerequisites and required configuration are limited to what blocks the
      happy path and are stated before the command that needs them.
- [ ] The path reaches a first useful result, or states a repository-supported
      next action when execution cannot be shown in the README.
- [ ] The normal usage example is the smallest representative example and does
      not make the reader choose among unnecessary variants.

## Repository accuracy and developer experience

- [ ] Documented commands exist and agree with manifests, scripts, task runners,
      CLI definitions, examples, tests, and current source behavior.
- [ ] Package names, imports, exports, flags, configuration keys, ports,
      filenames, runtime versions, and environment variables are confirmed.
- [ ] Internal links, images, external URLs, badges, and referenced documents
      resolve or are explicitly identified as unresolved rather than fabricated.
- [ ] The README does not claim that a command was tested when only static
      verification was possible.
- [ ] Existing canonical docs, examples, license, contribution, support, and
      security files are linked with the correct relative paths.
- [ ] The code examples match the current public API and specify a language for
      syntax highlighting.

## Scope and progressive disclosure

- [ ] Every substantial section answers a useful question for a new or
      prospective user.
- [ ] Features describe user outcomes, not implementation components or
      pipeline stages.
- [ ] Architecture, internals, exhaustive API/CLI/configuration material,
      deployment operations, long troubleshooting, changelogs, roadmaps, and
      full contributor workflows are linked out or omitted unless a small part
      is necessary for adoption.
- [ ] Deep content uses an existing canonical document and a substantive teaser;
      no fake or placeholder documents were created.
- [ ] Collapsed content is not hiding the primary value proposition, Quick
      Start, prerequisites, or normal usage.
- [ ] A manual table of contents is present only when the document's length or
      complexity makes it materially useful.

## Scan quality and voice

- [ ] Important information is front-loaded; paragraphs are short and bullets
      are concise.
- [ ] Headings describe reader questions or useful concepts rather than a
      generic template inventory.
- [ ] Badges are restrained and provide real trust or decision value.
- [ ] Visuals are authentic, relevant, accessible with useful alt text, and
      absent when they would not improve comprehension.
- [ ] Tables appear only where structured comparison or prerequisites are easier
      to understand as a table.
- [ ] The writing is direct, concrete, active, and project-specific without
      hype, repetitive summaries, decorative clutter, or flattened author voice.
- [ ] An improvement preserves accurate identity, terminology, strong examples,
      relevant visuals, and useful personality instead of regenerating blindly.

## Final reader pass

Read only the first screen, Quick Start, and first usage example as a stranger.
Ask:

1. What is this?
2. Why might it matter to me?
3. Can I tell whether I am the target user?
4. What do I run or install next?
5. What useful result should I expect?
6. Where do I go for deeper documentation or help?

If any answer requires guessing or hunting through deep content, fix the README
or link to a real canonical source before finishing.
