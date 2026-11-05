# Git Workflow

This article covers how this repository uses Git: its branches and their names, keeping a branch up to date, tags, and who runs which Git commands, and why. It follows the generated project's [Git workflow](../../template/docs/developer-manual/conventions/git-workflow.md) and adds what is different about a template. It applies to everyone, but the last part matters most for AI assistants, which can otherwise commit a change before anyone has looked at it.

## The Branches

The repository has two long-lived branches and any number of short-lived ones:

- **`main`** holds the released state of the template. Nothing is committed to it directly. It only ever receives a release, which merges `development` into it with a merge commit and is marked with a [tag](#tags).
- **`development`** collects the finished work between two releases. Every work branch starts from it and is merged back into it.
- **Work branches** each carry one feature, one bug fix, or the preparation of one release. A work branch starts from the latest `development`, and it is merged back into it with a merge commit, never squashed and never rebased onto it, so that every commit of the branch stays in the history and the merge commit marks where the work came in.

A work branch lives only as long as its work: once it is merged, it is [deleted](#merged-branches-are-deleted).

## Branch Names

A work branch is named after the kind of change it carries, followed by a short description in lowercase words separated by hyphens:

- **`feature/`** for a new capability or any other change that is not a bug fix, as in `feature/changelog-article`.
- **`fix/`** for a bug fix, as in `fix/readme-logo-alignment`.
- **`release/`** for the preparation of a release, followed by the version instead of a description, as in `release/v1.1.0` (see [GitHub workflow](github-workflow.md#releases)).

The description names the change, not the person or the date, and it stays short, since it ends up in the subject of the merge commit.

## Keeping a Branch up to Date

A work branch that falls behind `development` is brought up to date by rebasing it onto the latest `development`, never by merging `development` into it:

```shell
git fetch origin
git rebase origin/development
git push --force-with-lease
```

The rebase replays the branch's own commits on top of the current state, so the branch reads as if it had been started today, and its history has no merge commits that change nothing of its own. The same goes for work that belongs into an earlier commit of the branch: it is moved into that commit with a rebase instead of being added as a separate fix commit.

A rebase rewrites the branch's history, which is why the push needs `--force-with-lease`, which refuses to overwrite the branch if someone else pushed to it in the meantime. Only a work branch is ever rebased. `main` and `development` are shared, and their history is never rewritten.

## Merged Branches Are Deleted

A work branch has done its job once it is merged into `development` and its issue is closed, so it is deleted, on the repository host and locally. That keeps the branch list down to work in progress. GitHub offers to delete the branch right after the merge, and `gh pr merge --delete-branch` does it as part of the merge. Nothing is lost, because the merge commit keeps every commit of the branch in the history. `main` and `development` are never deleted.

## Bringing `development` Back in Step

A release merges `development` into `main` with a merge commit, so afterwards `main` is one commit ahead of `development`: the release merge itself. `development` has no commits of its own at that point, so it is fast-forwarded to `main`, which moves the branch without creating a commit or rewriting any history:

```shell
git switch development
git merge --ff-only main
git push origin development
```

Do it right after the release pull request is merged, before the next work branch is created, so that every work branch starts from a `development` that contains the release. Deleting and re-creating `development` reaches the same state, but closes every open pull request into it. Merging `main` into it adds a merge commit that changes nothing. If `--ff-only` refuses, something was merged into `development` after the release pull request was opened, and `main` is merged into `development` through a pull request instead.

## Tags

A tag is a name for one commit. Unlike a branch, it never moves, so it marks a state of the repository for good. Git has two kinds: a lightweight tag is nothing but the name, and an annotated tag is an object of its own, with an author, a date, and a message.

This repository uses tags for one thing only, releases, and they matter more here than in the generated project: `copier update` moves a generated project between tags, so a template change does not reach any consumer until it is tagged.

- **Every release has exactly one tag**, and every tag is a release. A tag is named exactly like the version it releases, prefixed with `v`, as in `v1.1.0`, and it points at the merge commit that brought the release into `main`.
- **Tags are always annotated.** Lightweight tags are not used, because the tag message is part of the release record. It repeats the release's entry in the [changelog](changelog-entries.md) and follows the [tag message](commit-messages.md#tag-messages) rules.
- **Tags are pushed explicitly.** Pushing a branch does not carry its tags along, so a tag is pushed by name.
- **A pushed tag is immutable.** A tag that turns out to be wrong is deleted and recreated only while it is still local. Once it is pushed, generated projects may already record it in their answers file, so a mistake is corrected by releasing a new version instead.

How the release tag is created, and the GitHub Release that goes with it, is part of the release itself (see [creating the tag](versioning.md#creating-the-tag)).

## The Working Tree Belongs to the Author

An assistant edits files and stops there. It does not stage, commit, push, tag, rebase, reset, or cherry-pick unless it was asked to do that exact thing. The same goes for creating, fast-forwarding, or deleting a branch.

The reason is review. Reading a diff in the working tree is how the person responsible for the change decides whether it is right. A change that is already committed has skipped that step, and a change that is already pushed cannot be reconsidered quietly. In a template that matters twice over, because a pushed and tagged change reaches every project that runs `copier update`.

## Ask for the Thing You Want

Each instruction authorizes exactly itself:

- **"Write a commit message"** means write it and stop. The message is reviewed first, and then either the user commits it or asks for the commit.
- **"Commit this"** authorizes the commit, not a push, and not a tag.
- **"Rebase these changes into that commit"** authorizes that rebase, not the next one.

An instruction to do one of these once does not carry over to later work in the same session.

## Staging Is the Review Mechanism

The staging area is not a step on the way to a commit here. It is how a reviewer tracks what they have already read. Changing what is staged on someone's behalf, in either direction, destroys that record, which is why `git add` and `git restore --staged` are on the same footing as `git commit`.

That includes the indirect ways of staging something. `git mv` and `git rm` update the index as well as the working tree, so moving or deleting a file is done with plain `mv` and `rm`, and the reviewer stages the result.

## Rendering Needs No Commit

Verifying a change means rendering the template (see [authoring](../project-template/authoring.md#verifying-a-change)), and that never requires committing first. When the template is a local Git repository with uncommitted changes, Copier warns that it is dirty and renders the working tree as it is, including those changes.

Render into a directory outside the repository, such as `/tmp/render-test`, so that none of the repository's own linters picks it up. A render is never committed.

## Related

- [Commit messages](commit-messages.md) — what a message says once you are asked to write one.
- [GitHub workflow](github-workflow.md) — the issues, labels, milestones, and pull requests around a branch, and the GitHub Release around a tag.
- [Versioning](versioning.md) — the version number and creating the release tag.
- [Changelog](changelog-entries.md) — the release's entry, which the tag message repeats.
- [Git workflow](../../template/docs/developer-manual/conventions/git-workflow.md) — the same rules, as the generated project states them.
