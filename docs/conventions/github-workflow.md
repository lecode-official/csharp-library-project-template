# GitHub Workflow

This article covers what GitHub adds on top of the [Git workflow](git-workflow.md) in this repository: issues, their titles, labels, milestones, pull requests, and releases. It follows the generated project's [GitHub workflow](../../template/docs/developer-manual/conventions/github-workflow.md), and the two are the same except for the examples and what this article adds about a template. The Git workflow says how a change travels from a work branch into a release. This article says how that journey is planned, tracked, and recorded on GitHub.

## Issues

Every change starts with an issue, and every issue describes one change: one feature or one bug fix, the same scope as the [work branch](git-workflow.md#the-branches) that will carry it. A change that turns out to be two changes becomes two issues.

An issue says what is wrong or missing and why it matters, before it says how to fix it. A bug report adds what was done, what was expected, and what happened instead, so that anyone can reproduce it. Details that the work needs, such as decisions already made or the files involved, go into a "Details" section below the description, so that the issue is enough to start the work from. An issue also says which side of the [split](../project-template/template-structure.md) it changes, since a change to the template body reaches every generated project, and a change at the root does not.

The work branch is created from its issue, which links the two on GitHub:

```shell
gh issue develop 42 --base development --name feature/changelog-article --checkout
```

## Titles

Issue and pull request titles are title case, like headings, commit subjects, and tag messages (see [Markdown style](markdown-style.md)). Names and code keep their own casing.

- **An issue title** is an imperative that says what is to be done, as in `Add an Article on the Changelog`.
- **A pull request title** says what was done, in the past tense, like the subject of a [commit message](commit-messages.md), as in `Added an Article on the Changelog`.

## Labels

Labels sort issues and pull requests into four groups, each named by its prefix:

- **`Type:`** says what kind of change it is. Every issue and every pull request has at least one, and one for each kind of change it makes, so an issue that updates the documentation, implements a feature, and changes a GitHub Actions workflow has three.
- **`Priority:`** says how urgent it is. Every issue has one, unless its priority has not been decided yet, and never more than one.
- **`Status:`** says where it stands, when that is more than open or closed: blocked, waiting for information, or not going to be done at all. The `Status:` labels mostly exclude each other, so an issue has one or none, and more than one only for a good reason.
- **`Dependabot:`** says which ecosystem a [Dependabot pull request](#dependabot-pull-requests) updates. Dependabot sets it itself, and nobody else uses it.

A pull request carries the same `Type:` labels as the issue it resolves.

| Label                               | Color     | Meaning                                                                 |
| ----------------------------------- | --------- | ----------------------------------------------------------------------- |
| `Type: Bug`                         | `#B60205` | Concerns the fixing of a bug.                                           |
| `Type: CI/CD`                       | `#6800E7` | Concerns the continuous integration and deployment (CI/CD) pipeline.    |
| `Type: Content`                     | `#A7DA8B` | Concerns the addition or updating of content, for example on a website. |
| `Type: Design`                      | `#E99695` | Concerns visual design.                                                 |
| `Type: Documentation`               | `#3545AF` | Concerns the updating or adding of content to the documentation.        |
| `Type: Idea or Request`             | `#1D76DB` | Concerns an idea or the request for adding a new feature.               |
| `Type: Implementation`              | `#006B75` | Concerns the implementation of a new feature.                           |
| `Type: Testing & Linting`           | `#FF7518` | Concerns unit tests, integration tests, linting, or formatting.         |
| `Priority: Critical`                | `#B60205` | Has a critical priority.                                                |
| `Priority: High`                    | `#E99695` | Has a high priority.                                                    |
| `Priority: Medium`                  | `#1D76DB` | Has a medium priority.                                                  |
| `Priority: Low`                     | `#0E8A16` | Has a low priority.                                                     |
| `Status: Abandoned`                 | `#B60205` | Was abandoned and no longer needs to be addressed.                      |
| `Status: Blocked`                   | `#D93F0B` | Is blocked until other issues or pull requests are completed.           |
| `Status: Can't Reproduce`           | `#750DB3` | Tries to address a bug, which cannot be reproduced.                     |
| `Status: Confirmed`                 | `#0E8A16` | Concerns a bug, which was confirmed to be reproducible.                 |
| `Status: Duplicate`                 | `#FEB6A8` | Is a duplicate of another issue or pull request.                        |
| `Status: Needs Information`         | `#FBCA04` | Needs more information to proceed.                                      |
| `Status: Won't Do/Fix`              | `#5319E7` | Concerns a feature request or bug that will not be addressed.           |
| `Dependabot: GitHub Actions Update` | `#0366D6` | Was opened by Dependabot and updates the GitHub Actions actions.        |
| `Dependabot: npm Update`            | `#0366D6` | Was opened by Dependabot and updates the npm packages.                  |

On GitHub, each label's description is its meaning, prefixed with "The issue or pull request", as in "The issue or pull request concerns the fixing of a bug." The `Dependabot:` labels only ever apply to a pull request, so theirs are prefixed with "The pull request" instead. This repository has a `Dependabot:` label for each ecosystem of its own Dependabot configuration, and the generated project one for each of its own. The labels are created with the script in [setting up GitHub](../development-setup/setting-up-github.md#labels), which is changed together with this table.

Only a maintainer can set labels, milestones, and assignees. A contributor who opens an issue or a pull request from a fork leaves them to the maintainers.

## Milestones

Every release is tracked with a milestone, which shows how much of it is done:

- **The title** is `Milestone v<major>.<minor>.<patch>`, after the version it releases, as in `Milestone v1.1.0`.
- **The description** is a short summary of every change planned for the release.
- **Every issue that goes into the release is assigned to it**, together with its pull request. That includes the bug fixes found along the way and the release's own issue.

The milestone is created when the release is planned, before its first issue, and it is closed once the release is published.

## Pull Requests

Every pull request resolves one issue, and it goes from the work branch into `development`. Its title follows the [title rules](#titles), it carries the issue's `Type:` labels and milestone, and its description says what changed and why, in prose, followed by the disclosure of any AI involvement (see [commit messages](commit-messages.md)) and the line `Resolves #42.` that names the issue.

A pull request is merged with a merge commit, never squashed or rebased (see [the branches](git-workflow.md#the-branches)), and with a message written by hand. GitHub's default merge message does not follow the [commit message](commit-messages.md) rules, so the message is written like any other commit message, including the AI disclosure, and passed explicitly. Its subject names the branch, as in `` Merged `feature/changelog-article` ``, and its body names the pull request and the issue it resolves, as in `Merged pull request #49, which resolves #42.`:

```shell
gh pr merge 49 --merge --subject 'Merged `feature/changelog-article`' --body-file <message-file>
```

GitHub only closes an issue through `Resolves #42.` when the pull request goes into the default branch, `main`. A pull request into `development` leaves the issue open, so the issue is closed by hand right after the merge, and the work branch is [deleted](git-workflow.md#merged-branches-are-deleted).

## Dependabot Pull Requests

Dependabot opens a pull request whenever a newer version of a dependency is released (see [dependency management](dependency-management.md)). Such a pull request has no issue, so it carries the `Dependabot:` label of its ecosystem instead of a `Type:` label, and it is assigned to the milestone of the next release like every other pull request.

Before it is merged, it is reviewed like any other change:

- **What changed.** Read the release notes of every dependency it raises, and note what the new versions change for the project, above all anything that breaks or that brings new findings.
- **What has to change with it.** Check whether the documentation or anything else has to change in the same pull request. [Dependency management](dependency-management.md) lists what Dependabot cannot do on its own, such as raising the body's linter versions together with the root's and rendering the template. Such a change is pushed to the pull request's branch.
- **The checks.** Continuous integration has to pass, like for every other pull request.

It is then merged with a merge commit and a message written by hand, like every other pull request. Its body names the pull request alone, as in `Merged pull request #40.`, since there is no issue to resolve.

## Releases

A release has an issue of its own, titled `Release vX.Y.Z`, and a pull request of the same title, the one pull request title that is not in the past tense, that merges `development` into `main`. Its merge message names the release, as in ``Merged `development` for Release v1.1.0``. Since that pull request goes into the default branch, its `Resolves` line closes the release issue. The release issue also lists the order in which the release's other issues are implemented, when one builds on another.

Once the release pull request is merged, the release is marked with a [tag](git-workflow.md#tags) on the merge commit, and a GitHub Release is created from that tag. The GitHub Release is titled like the tag's release, `Release vX.Y.Z`, and its notes are the tag message, which repeats the release's entry in the [changelog](changelog-entries.md). How the tag and the GitHub Release are created is covered in [creating the tag](versioning.md#creating-the-tag). The tag is what `copier update` moves a generated project to, so the release is not available to any consumer before it exists.

## Related

- [Git workflow](git-workflow.md) — the branches, their names, and the tags this article builds on.
- [Commit messages](commit-messages.md) — the rules for the merge message and the AI disclosure.
- [Versioning](versioning.md) — creating the release tag and the GitHub Release.
- [Changelog](changelog-entries.md) — the release's entry, which the GitHub Release repeats.
- [GitHub workflow](../../template/docs/developer-manual/conventions/github-workflow.md) — the same rules, as the generated project states them.
