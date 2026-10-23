# Git Workflow

This article covers who runs which Git commands, and why. It applies to everyone, but it matters most for AI assistants, which can otherwise commit a change before anyone has looked at it.

## The Working Tree Belongs to the Author

An assistant edits files and stops there. It does not stage, commit, push, tag, rebase, reset, or cherry-pick unless it was asked to do that exact thing.

The reason is review. Reading a diff in the working tree is how the person responsible for the change decides whether it is right. A change that is already committed has skipped that step, and a change that is already pushed cannot be reconsidered quietly.

## Ask for the Thing You Want

Each instruction authorizes exactly itself:

- **"Write a commit message"** means write it and stop. The message is reviewed first, and then either the user commits it or asks for the commit.
- **"Commit this"** authorizes the commit, not a push.
- **"Rebase these changes into that commit"** authorizes that rebase, not the next one.

An instruction to do one of these once does not carry over to later work in the same session.

## Staging Is the Review Mechanism

The staging area is not a step on the way to a commit here, it is how a reviewer tracks what they have already read. Staging or unstaging on someone's behalf destroys that record, which is why `git add` and `git restore --staged` are on the same footing as `git commit`.

## When a Rebase Was Asked For

Rewriting history moves every commit after the one that changed, which invalidates anything that recorded a commit identifier — [`.git-blame-ignore-revs`](git-blame.md) above all. After a rebase, check whether a recorded identifier still points at a commit on the branch, and correct it in the commit that records it.

## Related

- [Commit messages](commit-messages.md) — what a message should say once you are asked to write one.
- [Git blame](git-blame.md) — the revisions that blame skips.
- [Versioning](versioning.md) — the version bump that happens in the branch, before the pull request.
- [Contribution guide](../contribution-guide.md) — the process a change goes through.
