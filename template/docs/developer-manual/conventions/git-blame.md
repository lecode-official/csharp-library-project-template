# Git Blame

This article covers [`.git-blame-ignore-revs`](../../../.git-blame-ignore-revs) and why the repository has one.

## The Problem It Solves

A repository-wide reformat touches almost every line without changing what any of them mean. Afterwards `git blame` attributes those lines to the reformat, and the person who last changed a line for a real reason disappears behind it.

Adopting dprint across an existing code base is exactly such a commit: it reformats every file in one go, and every line it touched now blames to it (see [formatting](../tooling/formatting-dprint.md)).

## How It Works

[`.git-blame-ignore-revs`](../../../.git-blame-ignore-revs) lists the commit identifiers that blame should skip, one per line, with `#` comments. When blame reaches a listed commit it walks past it to the previous change of that line.

It is opt-in per clone:

```shell
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

Without that setting, blame behaves as though the file were not there. GitHub applies it automatically in its own blame view. Do not assume every hosting platform does.

## What Belongs in It

Only commits that are genuinely mechanical and repository-wide: a reformat, a mass rename, a codemod that changed no behavior. Nothing else.

A commit that carries real changes must never be listed. Doing so hides its author permanently, which is the opposite of what the file is for. When a mostly-mechanical commit contains a few judgment calls — a lint fix sweep where some rewrites were reviewed by hand, for instance — leave it out.

## It Breaks When History Is Rewritten

The file stores commit identifiers, and a rebase gives every commit after the rewritten one a new identifier. An entry that pointed at the old one then silently matches nothing.

After any rebase that touches or precedes a listed commit, check the entries and update them in the commit that records them:

```shell
git merge-base --is-ancestor <recorded-sha> HEAD && echo valid || echo stale
```

## Related

- [Git workflow](git-workflow.md) — when a rebase may happen at all.
- [Formatting (dprint)](../tooling/formatting-dprint.md) — the tool behind the listed commit.
