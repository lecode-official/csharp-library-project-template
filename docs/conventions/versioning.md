# Versioning

This article covers the template's own version number: what it measures, when it is raised, and how a release is recorded.

## The Version Is a Tag

`copier update` moves a generated project from the template version recorded in its `.copier-answers.yml` to a newer one, and Copier only knows a version by its Git tag. So a template change is not available to any consumer until it is released, and a release is an annotated tag named after the version, prefixed with `v`: `v0.1.0`, `v0.2.0`, and so on (see [rendering and updating](../project-template/rendering-and-updating.md#updating-a-project)).

Lightweight tags are not used, because the tag message is part of the release record. A release is not complete until its tag exists and is pushed.

## Semantic Versioning, Against the Generated Project

The template follows [Semantic Versioning](https://semver.org), measured against what a consumer of the template depends on: the questions they answer, and the project those answers produce.

- **Major** — a consumer's existing project or recorded answers stop working cleanly: a renamed or removed question, an answer that now means something different, or a restructured layout that `copier update` cannot reconcile without conflicts nobody caused.
- **Minor** — something new that takes nothing away: a new question with a sensible default, a new file in the body, a new choice for an existing question.
- **Patch** — a fix, or a change a generated project does not notice: a wording fix in a body article, a corrected comment, anything that only touches the root.

When a change is several of these, the highest one wins. Updating a project is always a merge, so err on the side of the higher number when in doubt.

## The Template's Version Is Not the Body's

The body carries version numbers of its own: `<Version>` in the library's project file and the first release in `template/CHANGELOG.md`. Those are the **generated project's** starting version, not the template's. A template release never touches them. They only change when the template decides that new projects should start at a different version, which is a body change like any other.

The template's own version lives at the root: in the tag, in the root [`CHANGELOG.md`](../../CHANGELOG.md), and in the `version` field of the root [`package.json`](../../package.json). All three carry the same number, and they are raised together, in the branch, before the pull request. A bump that is left for after the merge is a bump that eventually does not happen.

## The Changelog

[`CHANGELOG.md`](../../CHANGELOG.md) at the root lists every release of the template, newest first, in the same format the generated project's changelog uses:

```markdown
## Release v0.2.0

*Released on November 2, 2026.*

- Updated the serviced SDK bands named in the help of `dotnet_sdk_version`.
- Raised the pinned dprint plugins to their newest releases.
```

An unreleased version's date paragraph reads `*Release date to be determined.*` until it ships. The entries are written for a consumer deciding whether to run `copier update`: past tense, periods rather than semicolons, backticks around file names, paths, identifiers and code, and an explicit note on anything that changes a generated project.

## Creating the Tag

The tag message repeats the release's changelog entry and follows the [tag message](commit-messages.md#tag-messages) rules. Write it into a file and pass it with `-F`, then push the tag explicitly, since pushing a branch does not carry its tags along:

```shell
git tag -a v0.2.0 <commit> -F <message-file>
git push origin v0.2.0
```

A tag that turns out to be wrong is deleted with `git tag -d` and recreated, but only while it is still local. Once it is pushed, generated projects may already record it in their answers file, so it is treated as immutable. Release a new version instead.

Creating and pushing a tag only ever happens when it was asked for (see [Git workflow](git-workflow.md#tags-are-releases)).

## Related

- [Rendering and updating](../project-template/rendering-and-updating.md) — what a consumer does with a released version.
- [Commit messages](commit-messages.md) — the tag message rules.
- [Git workflow](git-workflow.md) — who creates the tag.
- [Versioning](../../template/docs/developer-manual/conventions/versioning.md) — the generated project's own versioning rules.
