# Versioning

This article covers the template's own version number: what it measures, when it is raised, and how a release is tagged. The [changelog](changelog-entries.md) that records each release has an article of its own.

## The Version Is a Tag

`copier update` moves a generated project from the template version recorded in its `.copier-answers.yml` to a newer one, and Copier only knows a version by its Git tag. So a template change is not available to any consumer until it is released, and a release is an annotated tag named after the version, prefixed with `v`: `v0.1.0`, `v0.2.0`, and so on (see [rendering and updating](../project-template/rendering-and-updating.md#updating-a-project)). The [Git workflow](git-workflow.md#tags) explains what a tag is and the rules every tag follows.

A release is not complete until its tag exists and is pushed.

## Semantic Versioning, Against the Generated Project

The template follows [Semantic Versioning](https://semver.org), measured against what a consumer of the template depends on: the questions they answer, and the project those answers produce.

- **Major** — a consumer's existing project or recorded answers stop working cleanly: a renamed or removed question, an answer that now means something different, or a restructured layout that `copier update` cannot reconcile without conflicts nobody caused.
- **Minor** — something new that takes nothing away: a new question with a sensible default, a new file in the body, a new choice for an existing question.
- **Patch** — a fix, or a change a generated project does not notice: a wording fix in a body article, a corrected comment, anything that only touches the root.

When a change is several of these, the highest one wins. Updating a project is always a merge, so err on the side of the higher number when in doubt.

## The Template's Version Is Not the Body's

The body carries version numbers of its own: `<Version>` in the library's project file, `version` in `template/package.json`, and the first release in `template/CHANGELOG.md`. Those are the **generated project's** starting version, not the template's. A template release never touches them. They only change when the template decides that new projects should start at a different version, which is a body change like any other.

The template's own version lives at the root: in the tag, in the root [`CHANGELOG.md`](../../CHANGELOG.md), and in the `version` field of the root [`package.json`](../../package.json). All three carry the same number, and they are raised together, in the branch, before the pull request. A bump that is left for after the merge is a bump that eventually does not happen.

## Creating the Tag

The tag points at the merge commit that brought the release into `main`, so it is created after the release pull request is merged. The tag message repeats the release's [changelog](changelog-entries.md) entry and follows the [tag message](commit-messages.md#tag-messages) rules. Write it into a file and pass it with `-F`, then push the tag explicitly, since pushing a branch does not carry its tags along:

```shell
git tag -a v0.2.0 <commit> -F <message-file>
git push origin v0.2.0
```

The GitHub Release is created after the tag is pushed, from that existing tag. Typing a new tag name into GitHub's release form makes GitHub create the tag itself, and a tag GitHub creates is always lightweight, so the release would lose its tag message. Pick the pushed tag in the form instead, or create the release from it with the GitHub CLI, which also takes the release notes from the tag message:

```shell
gh release create v0.2.0 --verify-tag --notes-from-tag --title "Release v0.2.0"
```

A tag that turns out to be wrong is deleted with `git tag -d` and recreated, but only while it is still local. Once it is pushed, generated projects may already record it in their answers file, so it is treated as immutable. Release a new version instead.

After the release pull request is merged, `development` is fast-forwarded to `main` (see [bringing `development` back in step](git-workflow.md#bringing-development-back-in-step)). Creating and pushing a tag, and the fast-forward, only ever happen when they were asked for (see [Git workflow](git-workflow.md#the-working-tree-belongs-to-the-author)).

## Related

- [Rendering and updating](../project-template/rendering-and-updating.md) — what a consumer does with a released version.
- [Changelog](changelog-entries.md) — the release's entry, which the tag message repeats.
- [GitHub workflow](github-workflow.md) — the release issue, the release pull request, and the milestone.
- [Commit messages](commit-messages.md) — the tag message rules.
- [Git workflow](git-workflow.md) — what a tag is, bringing `development` back in step after a release, and who creates the tag.
- [Versioning](../../template/docs/developer-manual/conventions/versioning.md) — the generated project's own versioning rules.
