# GitHub Workflow

This article covers what GitHub adds on top of the [Git workflow](git-workflow.md): issues, their titles, labels, milestones, pull requests, and releases. The Git workflow says how a change travels from a work branch into a release. This article says how that journey is planned, tracked, and recorded on GitHub.

## Issues

Every change starts with an issue, and every issue describes one change: one feature or one bug fix, the same scope as the [work branch](git-workflow.md#the-branches) that will carry it. A change that turns out to be two changes becomes two issues.

An issue says what is wrong or missing and why it matters, before it says how to fix it. A bug report adds what was done, what was expected, and what happened instead, so that anyone can reproduce it. Details that the work needs, such as decisions already made or the files involved, go into a "Details" section below the description, so that the issue is enough to start the work from.

A new issue on GitHub starts from one of the issue forms in [`.github/ISSUE_TEMPLATE/`](../../../.github/ISSUE_TEMPLATE/), which ask for these sections. The bug report asks for what was done, what was expected, and what happened instead, and the feature request for the description alone; both offer the "Details" section. They preset the `Type: Bug` or the `Type: Idea or Request` [label](#labels), and leave every other label, the milestone, and the assignee to whoever maintains the project. A blank issue stays available for an issue that fits neither form, such as the [release issue](#releases), and it is written in the same format. A security vulnerability is never reported in an issue, and the issue forms point to the [security policy](../../../SECURITY.md) for it.

The work branch is created from its issue, which links the two on GitHub:

```shell
gh issue develop 12 --base [[ integration_branch ]] --name feature/configurable-greeting --checkout
```

## Titles

Issue and pull request titles are title case, like headings, commit subjects, and tag messages (see [Markdown style](markdown-style.md#headings-are-title-case)). Names and code keep their own casing.

- **An issue title** is an imperative that says what is to be done, as in `Make the Greeting Configurable`.
- **A pull request title** says what was done, in the past tense, like the subject of a [commit message](commit-messages.md), as in `Made the Greeting Configurable`.

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
| `Type: Release`                     | `#F9D0C4` | Concerns the preparation of a release.                                  |
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
| `Dependabot: NuGet Update`          | `#0366D6` | Was opened by Dependabot and updates the NuGet packages.                |
| `Dependabot: .NET SDK Update`       | `#0366D6` | Was opened by Dependabot and updates the .NET SDK.                      |
| `Dependabot: npm Update`            | `#0366D6` | Was opened by Dependabot and updates the npm packages.                  |
| `Dependabot: pip Update`            | `#0366D6` | Was opened by Dependabot and updates the Python packages.               |

On GitHub, each label's description is its meaning, prefixed with "The issue or pull request", as in "The issue or pull request concerns the fixing of a bug." The `Dependabot:` labels only ever apply to a pull request, so theirs are prefixed with "The pull request" instead. The labels are created with the script in [setting up GitHub](../development-setup/setting-up-github.md#labels), which is changed together with this table.

Only a maintainer can set labels, milestones, and assignees. A contributor who opens an issue or a pull request from a fork leaves them to the maintainers.

## Milestones

Every release is tracked with a milestone, which shows how much of it is done:

- **The title** is `Milestone v<major>.<minor>.<patch>`, after the version it releases, as in `Milestone v1.2.0`.
- **The description** is a short summary of every change planned for the release.
- **Every issue that goes into the release is assigned to it**, together with its pull request. That includes the bug fixes found along the way and the release's own issue.

The milestone is created when the release is [planned](#planning-a-release), before the work on its first issue begins, and it is closed once the release is published.

## Pull Requests

Every pull request resolves one issue, and it goes from the work branch into `[[ integration_branch ]]`. Its title follows the [title rules](#titles), it carries the issue's `Type:` labels and milestone, and its description says what changed and why, in prose, followed by the disclosure of any AI involvement (see [commit messages](commit-messages.md)) and the line `Resolves #12.` that names the issue. A new pull request on GitHub starts from the [pull request template](../../../.github/pull_request_template.md), which holds these three parts as text to replace.

The only pull request into `[[ default_branch ]]` is the [release pull request](#releases) from `[[ integration_branch ]]`. The `Check Source Branch` check of the `Pull Requests` workflow fails any other pull request into `[[ default_branch ]]`, and once the branches are [protected](../development-setup/setting-up-github.md#branch-protection), such a pull request cannot be merged until its base branch is changed to `[[ integration_branch ]]`.

A pull request is merged with a merge commit, never squashed or rebased (see [the branches](git-workflow.md#the-branches)), and with a message written by hand. GitHub's default merge message does not follow the [commit message](commit-messages.md) rules, so the message is written like any other commit message, including the AI disclosure, and passed explicitly. Its subject names the branch, as in `` Merged `feature/configurable-greeting` ``, and its body names the pull request and the issue it resolves, as in `Merged pull request #13, which resolves #12.`:

```shell
gh pr merge 13 --merge --subject 'Merged `feature/configurable-greeting`' --body-file <message-file>
```

GitHub only closes an issue through `Resolves #12.` when the pull request goes into the default branch, `[[ default_branch ]]`. A pull request into `[[ integration_branch ]]` leaves the issue open, so the issue is closed by hand right after the merge, and the work branch is [deleted](git-workflow.md#merged-branches-are-deleted).

## Dependabot Pull Requests

Dependabot opens a pull request whenever a newer version of a dependency is released (see [dependency management](dependency-management.md)). Such a pull request has no issue, so it carries the `Dependabot:` label of its ecosystem instead of a `Type:` label, and it is assigned to the milestone of the next release like every other pull request. Dependabot opens it against `[[ integration_branch ]]`, like every other pull request, because its configuration sets `target-branch`.

A security update is the exception. Dependabot applies its configuration only to version updates, so it opens a security update against the default branch, `[[ default_branch ]]`, and without a label. As soon as it is opened, the [`Dependabot Security Updates`](../../../.github/workflows/dependabot-security-updates.yml) workflow points it at `[[ integration_branch ]]` and gives it the label of its ecosystem (see [continuous integration](../tooling/continuous-integration.md#dependabot-security-updates-workflow)). Dependabot computed the update against `[[ default_branch ]]`, which `[[ integration_branch ]]` always contains, so the diff stays the same.

The workflow runs as it is on `[[ default_branch ]]`, so it only takes effect once it has reached `[[ default_branch ]]`. Should it not have run, or have failed for an ecosystem that has no label, point the pull request at `[[ integration_branch ]]` and label it by hand:

```shell
gh pr edit 14 --base [[ integration_branch ]] --add-label "Dependabot: npm Update"
```

Until it is pointed at `[[ integration_branch ]]`, its `Check Source Branch` check fails, which is what keeps it out of `[[ default_branch ]]` on a protected repository. A pull request that is merged into `[[ default_branch ]]` by mistake is brought back into `[[ integration_branch ]]` by merging `[[ default_branch ]]` into `[[ integration_branch ]]` through a pull request, never by rewriting either branch.

Before it is merged, it is reviewed like any other change:

- **What changed.** Read the release notes of every dependency it raises, and note what the new versions change for the project, above all anything that breaks or that brings new findings.
- **What has to change with it.** Check whether the documentation or anything else has to change in the same pull request. [Dependency management](dependency-management.md) lists what Dependabot cannot do on its own, such as updating the `allowScripts` key of `dprint`. Such a change is pushed to the pull request's branch.
- **The checks.** Continuous integration has to pass, like for every other pull request.

It is then merged with a merge commit and a message written by hand, like every other pull request. Its body names the pull request alone, as in `Merged pull request #14.`, since there is no issue to resolve.

## Planning a Release

A release is planned at its start, not at its end. Before the work on its first issue begins, its [milestone](#milestones) is created, together with its issues and its [release issue](#releases), so that the plan the release issue keeps is there for every issue that follows.

The release issue lists the order in which the release's other issues are implemented, under the heading `## Order`. The order is a numbered list, and each item names one issue or several:

```markdown
## Order

1. #13.
2. #14, #15, #16, and #17.
3. #18.
```

- **The items are worked through from top to bottom.** An item is only started once every issue of the item above it is closed, so an issue that another one builds on goes into an earlier item.
- **The issues of one item can be worked on at the same time**, by different people. They are listed in their suggested order.
- **A short note may say why an issue comes where it does**, as in `#18 (adds to the workflow of #17)`. It explains the order, but the items alone decide it.
- **An issue added to the milestone later**, such as a bug found along the way, is added to the order too.

The next issue to work on is found by reading the order from top to bottom and from left to right. It is the first issue that is open and assigned to nobody else, within the first item that still has open issues. An issue that is assigned to someone else is their work, so it is skipped. When every open issue of that item is assigned, there is no next issue until one of them is closed. The release issue itself comes last, once every other issue of the milestone is closed.

## Releases

A release is prepared and merged in a fixed order:

1. **The release issue.** A release has an issue of its own, titled `Release vX.Y.Z`, labeled `Type: Release`, and assigned to the release's milestone. It is created when the release is [planned](#planning-a-release), at the start of the release, and it lists the order in which the release's other issues are implemented.
2. **The release branch.** Once every other issue of the milestone is closed, a work branch named `release/vX.Y.Z` is created from `[[ integration_branch ]]` and linked to the release issue. Its commit finishes the release:
   - It replaces the date paragraph of the release in the [changelog](changelog-entries.md#an-unreleased-version) with the release date, and tidies up the release's entries. They are written one change at a time, so just before the release, entries that describe the same work are merged, and the entries a consumer has to act on come first.
   - It checks that the version is the same everywhere it has to be (see [versioning](versioning.md#everything-that-has-to-move-together)).
3. **The pull request into `[[ integration_branch ]]`.** The release branch is merged into `[[ integration_branch ]]` like any other work branch, through a pull request titled `Prepared Release vX.Y.Z` with the line `Resolves #12.` that names the release issue. It goes into `[[ integration_branch ]]`, so it links the release issue without closing it.
4. **The release pull request.** A pull request titled `Release vX.Y.Z`, the one pull request title that is not in the past tense, merges `[[ integration_branch ]]` into `[[ default_branch ]]`. It carries `Type: Release` and the same `Resolves` line, and since it goes into the default branch, merging it closes the release issue. Its merge message names the release, as in ``Merged `[[ integration_branch ]]` for Release v1.2.0``.
5. **After the merge.** The merge commit is marked with the release's [tag](git-workflow.md#tags), a GitHub Release is created from that tag, `[[ integration_branch ]]` is [brought back in step](git-workflow.md#bringing-the-integration-branch-back-in-step) with `[[ default_branch ]]`, and the milestone is closed.

The GitHub Release is titled like the tag's release, `Release vX.Y.Z`, and its notes are the tag message, which repeats the release's entry in the changelog. How the tag and the GitHub Release are created is covered in [the release tags](versioning.md#the-release-tags).

## Related

- [Git workflow](git-workflow.md) — the branches, their names, and the tags this article builds on.
- [Commit messages](commit-messages.md) — the rules for the merge message and the AI disclosure.
- [Versioning](versioning.md) — creating the release tag and the GitHub Release.
- [Changelog](changelog-entries.md) — the release's entry, which the GitHub Release repeats.
- [Contribution guide](../contribution-guide.md) — the process a change goes through.
