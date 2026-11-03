# Changelog

This article covers the template's own [`CHANGELOG.md`](../../CHANGELOG.md): what it records, how a release is laid out in it, and how its entries are written. It follows the generated project's [changelog](../../template/docs/developer-manual/conventions/changelog.md) conventions and adds what is different about a template.

## What It Records

[`CHANGELOG.md`](../../CHANGELOG.md) at the root lists every release of the template, newest first. It is updated by hand, in the same change as the work it describes: whoever changes the template adds the entry, under the version the change will ship in.

Every release in it corresponds to an annotated Git tag of the same name (see [versioning](versioning.md#the-version-is-a-tag)).

It is not the body's [`CHANGELOG.md`](../../template/CHANGELOG.md). That file is the generated project's own changelog, which starts with a single release and is only ever created by the template, never updated (see [the template's version is not the body's](versioning.md#the-templates-version-is-not-the-bodys)).

## The Layout of a Release

A release is laid out the same way the generated project's changelog lays it out:

```markdown
## Release v0.2.0

*Released on November 2, 2026.*

- Updated the serviced SDK bands named in the help of `dotnet_sdk_version`.
- Raised the pinned dprint plugins to their newest releases.
```

- **The heading** reads `Release vX.Y.Z`, with the same `v` prefix the tag carries.
- **The date paragraph** reads `*Released on Month D, YYYY.*`, with the month spelled out.
- **The list** is flat, with one bullet per change. There is no opening paragraph and no grouping into subsections.

## An Unreleased Version

A version that has not shipped yet already has its heading and collects its entries, but its date paragraph reads exactly:

```markdown
*Release date to be determined.*
```

The period is part of it. Without it, MarkdownLint reads a paragraph that consists of nothing but emphasis as a heading in disguise and reports it. The last commit before the release replaces the paragraph with the release date, so that the date in the changelog and the date of the tag never disagree.

## Writing the Entries

The entries follow the [Markdown style](markdown-style.md): past tense, periods rather than semicolons, and backticks around file names, paths, identifiers and code.

They are written for a consumer deciding whether to run `copier update`, so an entry says what changed in a generated project, and says explicitly when an existing project has to do something by hand. The usual case is a file the template only creates (see [rendering and updating](../project-template/rendering-and-updating.md#files-the-template-only-creates)): an update leaves it alone, so the entry tells the consumer what to copy into it.

A change that only touches the root is recorded too, since it is part of the release, even though a generated project never notices it.

## The Changelog and the Tag Message

The message of a release tag repeats the release's list of changes, so the changelog and the tag never disagree. The [tag message](commit-messages.md#tag-messages) rules cover how that list is wrapped, and [versioning](versioning.md#creating-the-tag) covers how the tag is created.

## Related

- [Versioning](versioning.md) — the version number the headings name, and the release tags.
- [Commit messages](commit-messages.md) — the tag message that repeats a release's changes.
- [Rendering and updating](../project-template/rendering-and-updating.md) — what a consumer does with a release.
- [Changelog](../../template/docs/developer-manual/conventions/changelog.md) — the generated project's own changelog conventions.
