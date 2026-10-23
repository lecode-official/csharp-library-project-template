# Commit Messages

This article covers how commit messages are written in this repository. It applies to everyone, human and AI assistant alike.

## The 50/72 Rule

Commit messages follow the conventional 50/72 rule:

- The subject line is at most 50 characters.
- A single blank line separates the subject from the body.
- Every body line is wrapped at most 72 characters — unlike the documentation, which is never manually wrapped (see [Markdown style](markdown-style.md)).

The subject is a complete summary on its own. The body is optional — a small, self-explanatory change may be subject-only.

There is no type or scope prefix. Commit messages here are not [Conventional Commits](https://www.conventionalcommits.org): a subject reads `Added the Concurrency Limit`, never `feat(queue): add concurrency limit`.

## Title-Cased Subject

The subject line is written in Title Case, capitalizing the principal words. Preserve the natural casing of code identifiers and brand names, exactly as [Markdown headings](markdown-style.md) do. Do not end the subject with a period.

## Past Tense

Both the subject and the body are written in the past tense, describing what the change did — not what it does or should do. Write "Added the Greeter Class", "Pinned the .NET SDK", or "Fixed the Salutation Guard", never "Add", "Pin", or "Fixes".

## Code Spans

Wrap file names, paths, identifiers, and code in backticks, exactly as Markdown prose does (see [Markdown style](markdown-style.md#code-spans-for-identifiers-paths-and-file-names)). This applies to the subject line and the body alike: `global.json`, `docs/README.md`, `Greet()`.

This holds even though most Git tools render commit messages as plain text: the backticks still mark the boundary between prose and literal code for a human reader.

## Body Structure

When a body is present, it explains what changed and why — the diff already shows what changed, so the *why* is what earns its place. It is written as either:

- Prose paragraphs, or
- Bulleted or numbered lists.

Multiple paragraphs and lists may be intermixed freely — for example, an opening paragraph followed by a list, followed by another paragraph. Keep every line within the 72-character wrap. Whichever form the body takes, it follows the same punctuation rule as the rest of the documentation: periods, not semicolons (see [Markdown style](markdown-style.md)).

## Disclosing AI Involvement

Every commit message states whether AI was involved in producing it and, if it was, what exactly the AI did. The commit history is where that involvement is tracked. A commit written entirely by hand carries no such note. A commit where AI was involved:

- Says in the body what the AI actually did — wrote the documentation, generated a design asset, tracked down a bug, and so on. The trailer alone does not say this, and it is the part a reader of the history actually needs.
- Carries one co-author trailer per AI model involved, at the very end of the message, after a blank line. The trailer names the AI tool's own no-reply address, which links the commit to the tool's account on the repository host, and the exact model and version that did the work:

  ```text
  Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>
  ```

The trailer names the specific model and version, `Claude Opus 5.5 Medium`, never just the product, `Claude`. A product name covers many models of very different capabilities over the years, so only the model and its version tell a reader of the history what actually produced a change. Add a further detail, such as the size of the context window, only when the model name and version alone do not tell two models apart — when the same model is offered with two different context windows, for example. A model that always comes with the same context window needs no such detail.

Claude is only one example. Other AI tools have trailers of their own, and the same rule applies to them, with the model and version in the name:

```text
Co-Authored-By: <model and version> <175728472+Copilot@users.noreply.github.com>
Co-Authored-By: aider (<model and version>) <noreply@aider.chat>
```

The first is the address of GitHub Copilot, the second the form aider writes on its own. For any other tool, use the no-reply address it documents, or the one it writes into its own commits. When several models were involved, list one trailer per model, one per line.

## Tag Messages

Release tags carry a message too, and it follows every rule above — the 50/72 wrap, Title Case, past tense, and backticks around file names, paths, identifiers, and code. The differences are these:

- **The subject is the release, not a change.** It reads `Release vX.Y.Z (Month D, YYYY)`, with the month spelled out and no terminal period, for example `Release v0.4.0 (August 12, 2026)`.
- **The body is the release's list of changes.** It is the same list the release has in [`CHANGELOG.md`](../../../CHANGELOG.md), one bullet per change, so the two never disagree. There is no opening paragraph.
- **No co-author trailer.** A tag records a release, not authorship of the work, and every change in it is already attributed by the commits it tags.
- **Never break a code span across a wrapped line.** Reword the bullet instead, so that the whole code span stays on one line.

Write the message into a file and pass it with `-F`, so the wrapping survives verbatim:

```text
Release v0.4.0 (August 12, 2026)

- Raised the pinned .NET SDK to `10.0.401`, because the `10.0.3xx`
  feature band stopped receiving servicing updates.
```


## Example

```text
Added a Guard Against a Blank Salutation

Added a guard to `Greeter`'s constructor that rejects a salutation
consisting only of white-space characters, so that the failure is
reported where the mistake was made rather than showing up as a
greeting that starts with blanks.

- Added a `[Theory]` covering the empty and the blank string.
- Documented the new `ArgumentException` on the constructor.

The test was written using Claude Code.

Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>
```

## Related

- [Git workflow](git-workflow.md) — who runs the commit, and what an instruction to write a message does and does not authorize.
- [Markdown style](markdown-style.md) — the same title-case and punctuation rules used for headings and prose.
