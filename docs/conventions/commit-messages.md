# Commit Messages

This article covers how commit and tag messages are written in this repository. It applies to everyone, human and AI assistant alike.

## The Generated Project's Rules, Unchanged

The template's history follows the same rules as a generated project's:

- **The 50/72 rule.** The subject is at most 50 characters, a blank line follows it, and every body line is wrapped at 72 characters.
- **A title-cased subject without a terminal period**, preserving the real casing of identifiers and tool names.
- **Past tense** in the subject and the body: "Added the License Question", never "Add" or "Adds".
- **No type or scope prefix.** These are not Conventional Commits.
- **Backticks around file names, paths, identifiers and code**, in the subject and the body alike.
- **A body that explains why**, as prose paragraphs, lists, or both, following the prose punctuation rule: periods, not semicolons. A small, self-explanatory change may be subject-only.

## Say Which Side Changed

A commit that changes the body changes every project generated from now on, and one that changes only the root does not. A reader of the history needs to tell the two apart, above all when deciding what a release is worth (see [versioning](versioning.md)).

So when a commit changes the body, the message describes the change from the generated project's point of view, and says so when it affects a consumer who runs `copier update`: a renamed file, a new question, a changed default. A commit that only touches the root's documentation, linters or scripts can say just that.

## Disclosing AI Involvement

Every commit message states whether AI was involved in producing it and, if it was, what exactly the AI did: wrote the documentation, rewrote a template file, tracked down a rendering bug. That sentence goes in the body, because the trailer alone does not say it.

A commit where AI was involved ends with one co-author trailer per AI model involved, after a blank line. The trailer names the AI tool's own no-reply address, which links the commit to the tool's account on the repository host, and the exact model and version that did the work:

```text
Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>
```

The trailer names the specific model and version, `Claude Opus 5.5 Medium`, never just the product, `Claude`. A product name covers many models of very different capabilities over the years, so only the model and its version tell a reader of the history what actually produced a change. Add a further detail, such as the size of the context window, only when the model name and version alone do not tell two models apart — when the same model is offered with two different context windows, for example. A model that always comes with the same context window needs no such detail.

Claude is only one example. Other AI tools have trailers of their own, and the same rule applies to them, with the model and version in the name:

```text
Co-Authored-By: <model and version> <175728472+Copilot@users.noreply.github.com>
Co-Authored-By: aider (<model and version>) <noreply@aider.chat>
```

The first is the address of GitHub Copilot, the second the form aider writes on its own. For any other tool, use the no-reply address it documents, or the one it writes into its own commits. When several models were involved, list one trailer per model, one per line. A commit written entirely by hand carries no such note.

## Tag Messages

Every release of the template is an annotated tag, and its message follows these rules:

- The subject reads `Release vX.Y.Z (Month D, YYYY)`, as in `Release v0.1.0 (October 19, 2026)`.
- The body is the release's list of changes from [`CHANGELOG.md`](../../CHANGELOG.md), one bullet per change, with no opening paragraph.
- No co-author trailer, since a tag records a release rather than authorship.
- A code span is never broken across a wrapped line. Reword the bullet instead.

Write the message into a file and pass it with `-F`, so the wrapping survives verbatim.

## Example

```text
Added the `license` Question

Added a `license` question offering the SPDX identifiers of ten
licenses, so that a generated project no longer ships with MIT
regardless of what its author intended. `template/LICENSE` now
includes the matching text from `licenses/`.

A generated project that runs `copier update` is asked the new
question, because its recorded answers do not hold one yet.

The documentation and the vendoring script were written using
Claude Code.

Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>
```

## Related

- [Git workflow](git-workflow.md) — who runs the commit, and what an instruction to write a message authorizes.
- [Versioning](versioning.md) — the changelog and the release tags.
- [Markdown style](markdown-style.md) — the same title-case and punctuation rules.
