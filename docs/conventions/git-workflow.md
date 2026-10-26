# Git Workflow

This article covers who runs which Git commands in this repository, and why. It applies to everyone, but it matters most for AI assistants, which can otherwise commit a change before anyone has looked at it.

## The Working Tree Belongs to the Author

An assistant edits files and stops there. It does not stage, commit, push, rebase, reset, tag or cherry-pick unless it was asked to do that exact thing.

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

## Merged Branches Are Deleted

A feature branch has done its job once its pull request is merged into `development` and its issue is closed, so it is deleted, on the repository host and locally. That keeps the branch list down to work in progress. GitHub offers to delete the branch right after the merge, and `gh pr merge --delete-branch` does it as part of the merge. Nothing is lost, because the merge commit keeps every commit of the branch in the history. `main` and `development` are never deleted (see [versioning](versioning.md#bringing-development-back-in-step)).

Deleting a branch changes the repository's state like any other command in this article, so an assistant only does it when it was asked to.

## Tags Are Releases

A tag is what makes a template change reach consumers, because `copier update` moves between tags (see [versioning](versioning.md)). Creating or pushing one is therefore a release, and only ever happens when it was asked for.

## Related

- [Commit messages](commit-messages.md) — what a message says once you are asked to write one.
- [Versioning](versioning.md) — the changelog and the tags.
- [Git workflow](../../template/docs/developer-manual/conventions/git-workflow.md) — the same rules, as the generated project states them.
