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

The template's own version lives at the root: in the tag, in the root [`CHANGELOG.md`](../../CHANGELOG.md), and in the `version` field of the root [`package.json`](../../package.json). All three carry the same number, and `package-lock.json` repeats the one in `package.json`. They are raised together, in the branch, before the pull request. A bump that is left for after the merge is a bump that eventually does not happen.

## Creating the Tag

The tag points at the merge commit that brought the release into `main`, so it is created after the release pull request is merged. The [`Release`](../../.github/workflows/release.yml) workflow does that by itself: when a pull request into `main` is merged, it reads the newest release from the [changelog](changelog-entries.md), creates the annotated tag on the merge commit, pushes it, and creates the GitHub Release from it. Before it creates anything, it checks that the tag does not exist yet, that the release's date paragraph is set, and that the version in the root `package.json` and `package-lock.json` is the release's.

The workflow writes both texts with [`.github/scripts/prepare-release.py`](../../.github/scripts/prepare-release.py):

- **The tag message** follows the [tag message](commit-messages.md#tag-messages) rules: the subject `Release vX.Y.Z (Month D, YYYY)`, with the date from the changelog, and the release's bullets, wrapped at 72 characters without breaking a code span.
- **The release notes** are the same bullets exactly as the changelog has them, unwrapped, since GitHub wraps them itself. The GitHub Release is titled `Release vX.Y.Z`.

The tag is created by `github-actions[bot]` and is not signed. A tag pushed with the workflow's token starts no other workflow, so everything a release does happens in that one workflow. The `Linters` workflow runs the same script as a dry run on every pull request, so a changelog it cannot read fails long before the release (see [testing](testing.md#continuous-integration)). To see the tag message the next release will get, run it locally:

```shell
python3 .github/scripts/prepare-release.py --dry-run
```

When the workflow fails, the tag and the GitHub Release are created by hand instead, from the same texts. The script writes them into a directory, and the tag is pushed explicitly, since pushing a branch does not carry its tags along:

```shell
python3 .github/scripts/prepare-release.py --output-directory /tmp/release
git tag -a v0.2.0 <merge-commit> -F /tmp/release/tag-message.txt
git push origin v0.2.0
gh release create v0.2.0 --verify-tag --title "Release v0.2.0" --notes-file /tmp/release/release-notes.md
```

The GitHub Release is always created from the existing tag. Typing a new tag name into GitHub's release form makes GitHub create the tag itself, and a tag GitHub creates is always lightweight, so the release would lose its tag message. `--verify-tag` makes the GitHub CLI fail instead.

A tag that turns out to be wrong is deleted with `git tag -d` and recreated, but only while it is still local. Once it is pushed, generated projects may already record it in their answers file, so it is treated as immutable. Release a new version instead.

After the release pull request is merged, `development` is fast-forwarded to `main` (see [bringing `development` back in step](git-workflow.md#bringing-development-back-in-step)). Creating and pushing a tag by hand, and the fast-forward, only ever happen when they were asked for (see [Git workflow](git-workflow.md#the-working-tree-belongs-to-the-author)).

## Related

- [Rendering and updating](../project-template/rendering-and-updating.md) — what a consumer does with a released version.
- [Changelog](changelog-entries.md) — the release's entry, which the tag message repeats.
- [GitHub workflow](github-workflow.md) — the release issue, the release pull request, and the milestone.
- [Commit messages](commit-messages.md) — the tag message rules.
- [Git workflow](git-workflow.md) — what a tag is, bringing `development` back in step after a release, and who creates the tag.
- [Versioning](../../template/docs/developer-manual/conventions/versioning.md) — the generated project's own versioning rules.
