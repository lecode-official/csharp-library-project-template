# Changelog

This article covers [`CHANGELOG.md`](../../../CHANGELOG.md): what it records, how a release is laid out in it, and how its entries are written.

## What It Records

`CHANGELOG.md` at the repository root lists every release, newest first. It is not generated from the Git history, so it is updated by hand, in the same change as the work it describes: whoever changes something adds the entry, under the version the change will ship in. A change that is left for later is a change the changelog eventually forgets.

Every release in it corresponds to an annotated Git tag of the same name (see [versioning](versioning.md#the-release-tags)).

## The Layout of a Release

Each release is a level-two heading naming the version, followed by a single italic paragraph with the release date, followed by a flat list of changes:

```markdown
## Release v0.3.0

*Released on August 12, 2026.*

- Added the `Greeter.GreetAll` method, which greets several names at once.
- Fixed `Greeter.Greet` throwing on an empty name instead of returning the plain greeting.
```

- **The heading** reads `Release vX.Y.Z`, with the same `v` prefix the release tag carries.
- **The date paragraph** reads `*Released on Month D, YYYY.*`, with the month spelled out.
- **The list** is flat, with one bullet per change. There is no opening paragraph and no grouping into subsections.

## An Unreleased Version

A version that has not shipped yet already has its heading and collects its entries, but its date paragraph reads exactly:

```markdown
*Release date to be determined.*
```

The period is part of it. Without it, MarkdownLint reads a paragraph that consists of nothing but emphasis as a heading in disguise and reports it. The last commit before the release replaces the paragraph with the release date, so that the date in the changelog and the date of the release never disagree.

## Writing the Entries

The entries follow the same prose rules as everything else here (see [Markdown style](markdown-style.md)):

- **Past tense**: "Added", "Fixed", "Raised", never "Add" or "Adds".
- **Periods rather than semicolons**, and every bullet ends with a period.
- **Backticks around file names, paths, identifiers, and code.**
- **Written for the reader of the release**, who wants to know what changed for them, not how the change was made. An entry that requires them to do something says so explicitly.

## The Changelog and the Tag Message

The message of a release tag repeats the release's list of changes, one bullet per change, so the changelog and the tag never disagree. The [tag message](commit-messages.md#tag-messages) rules cover how that list is wrapped, and [versioning](versioning.md#the-release-tags) covers how the tag is created.

## Related

- [Versioning](versioning.md) — the version number the headings name, and the release tags.
- [Commit messages](commit-messages.md) — the tag message that repeats a release's changes.
- [Markdown style](markdown-style.md) — the conventions the changelog is written to.
