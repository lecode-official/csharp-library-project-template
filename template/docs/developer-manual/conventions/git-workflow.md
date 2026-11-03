# Git Workflow

This article covers how the project uses Git: its branches and their names, keeping a branch up to date, tags, and who runs which Git commands, and why. It applies to everyone, but the last part matters most for AI assistants, which can otherwise commit a change before anyone has looked at it.

## The Branches

The repository has two long-lived branches and any number of short-lived ones:

- **`[[ default_branch ]]`** holds the released state of the project. Nothing is committed to it directly. It only ever receives a release, which merges `[[ integration_branch ]]` into it with a merge commit and is marked with a [tag](#tags).
- **`[[ integration_branch ]]`** collects the finished work between two releases. Every work branch starts from it and is merged back into it.
- **Work branches** each carry one feature or one bug fix. A work branch starts from the latest `[[ integration_branch ]]`, and it is merged back into it with a merge commit, never squashed and never rebased onto it, so that every commit of the branch stays in the history and the merge commit marks where the work came in.

A work branch lives only as long as its work: once it is merged, it is [deleted](#merged-branches-are-deleted).

## Branch Names

A work branch is named after the kind of change it carries, followed by a short description in lowercase words separated by hyphens:

- **`feature/`** for a new capability or any other change that is not a bug fix, as in `feature/configurable-greeting`.
- **`fix/`** for a bug fix, as in `fix/empty-name-greeting`.

The description names the change, not the person or the date, and it stays short, since it ends up in the subject of the merge commit.

## Keeping a Branch up to Date

A work branch that falls behind `[[ integration_branch ]]` is brought up to date by rebasing it onto the latest `[[ integration_branch ]]`, never by merging `[[ integration_branch ]]` into it:

```shell
git fetch origin
git rebase origin/[[ integration_branch ]]
git push --force-with-lease
```

The rebase replays the branch's own commits on top of the current state, so the branch reads as if it had been started today, and its history has no merge commits that change nothing of its own. The same goes for work that belongs into an earlier commit of the branch: it is moved into that commit with a rebase instead of being added as a separate fix commit.

A rebase rewrites the branch's history, which is why the push needs `--force-with-lease`, which refuses to overwrite the branch if someone else pushed to it in the meantime. Only a work branch is ever rebased. `[[ default_branch ]]` and `[[ integration_branch ]]` are shared, and their history is never rewritten.

Rewriting history moves every commit after the one that changed, which invalidates anything that recorded a commit identifier — [`.git-blame-ignore-revs`](git-blame.md) above all. After a rebase, check whether a recorded identifier still points at a commit on the branch, and correct it in the commit that records it.

## Merged Branches Are Deleted

A work branch has done its job once it is merged into `[[ integration_branch ]]` and its issue is closed, so it is deleted, on the repository host and locally. That keeps the branch list down to work in progress. GitHub offers to delete the branch right after the merge, and `gh pr merge --delete-branch` does it as part of the merge. Nothing is lost, because the merge commit keeps every commit of the branch in the history. `[[ default_branch ]]` and `[[ integration_branch ]]` are never deleted.

## Bringing the Integration Branch Back in Step

A release merges `[[ integration_branch ]]` into `[[ default_branch ]]` with a merge commit, so afterwards `[[ default_branch ]]` is one commit ahead of `[[ integration_branch ]]`: the release merge itself. `[[ integration_branch ]]` has no commits of its own at that point, so it is fast-forwarded to `[[ default_branch ]]`, which moves the branch without creating a commit or rewriting any history:

```shell
git switch [[ integration_branch ]]
git merge --ff-only [[ default_branch ]]
git push origin [[ integration_branch ]]
```

Do it right after the release pull request is merged, before the next work branch is created, so that every work branch starts from a `[[ integration_branch ]]` that contains the release. Deleting and re-creating `[[ integration_branch ]]` reaches the same state, but closes every open pull request into it. Merging `[[ default_branch ]]` into it adds a merge commit that changes nothing. If `--ff-only` refuses, something was merged into `[[ integration_branch ]]` after the release pull request was opened, and `[[ default_branch ]]` is merged into `[[ integration_branch ]]` through a pull request instead.

## Tags

A tag is a name for one commit. Unlike a branch, it never moves, so it marks a state of the repository for good. Git has two kinds: a lightweight tag is nothing but the name, and an annotated tag is an object of its own, with an author, a date, and a message.

This project uses tags for one thing only, releases:

- **Every release has exactly one tag**, and every tag is a release. A tag is named exactly like the version it releases, prefixed with `v`, as in `v1.2.0`, and it points at the merge commit that brought the release into `[[ default_branch ]]`.
- **Tags are always annotated.** Lightweight tags are not used, because the tag message is part of the release record. It repeats the release's entry in the [changelog](changelog.md) and follows the [tag message](commit-messages.md#tag-messages) rules.
- **Tags are pushed explicitly.** Pushing a branch does not carry its tags along, so a tag is pushed by name.
- **A pushed tag is immutable.** A tag that turns out to be wrong is deleted and recreated only while it is still local. Once it is pushed, other clones have it, so a mistake is corrected by releasing a new version instead.

How the release tag is created, and the GitHub Release that goes with it, is part of the release itself (see [the release tags](versioning.md#the-release-tags)).

## The Working Tree Belongs to the Author

An assistant edits files and stops there. It does not stage, commit, push, tag, rebase, reset, or cherry-pick unless it was asked to do that exact thing. The same goes for creating, fast-forwarding, or deleting a branch.

The reason is review. Reading a diff in the working tree is how the person responsible for the change decides whether it is right. A change that is already committed has skipped that step, and a change that is already pushed cannot be reconsidered quietly.

## Ask for the Thing You Want

Each instruction authorizes exactly itself:

- **"Write a commit message"** means write it and stop. The message is reviewed first, and then either the user commits it or asks for the commit.
- **"Commit this"** authorizes the commit, not a push.
- **"Rebase these changes into that commit"** authorizes that rebase, not the next one.

An instruction to do one of these once does not carry over to later work in the same session.

## Staging Is the Review Mechanism

The staging area is not a step on the way to a commit here, it is how a reviewer tracks what they have already read. Staging or unstaging on someone's behalf destroys that record, which is why `git add` and `git restore --staged` are on the same footing as `git commit`.

## Related

- [Commit messages](commit-messages.md) — what a message should say once you are asked to write one.
- [Git blame](git-blame.md) — the revisions that blame skips.
- [Versioning](versioning.md) — the version bump that happens in the branch, before the pull request, and the release tags.
- [Changelog](changelog.md) — the release's entry, which the tag message repeats.
- [Contribution guide](../contribution-guide.md) — the process a change goes through.
