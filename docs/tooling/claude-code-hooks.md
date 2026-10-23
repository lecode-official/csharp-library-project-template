# Claude Code Hooks

This article covers the Claude Code hooks in the root's [`.claude/settings.json`](../../.claude/settings.json), which files reach them, and how they differ from the hooks the template body ships.

## What the Root's Hooks Do

Three `PostToolUse` hooks run after `Edit`, `Write` and `NotebookEdit`, and check the changed file:

- **dprint** formats it in place. It never fails the turn, because there is nothing for anyone to decide.
- **MarkdownLint** checks a `.md` file and reports what it finds. It runs without `--fix`, because dprint owns all formatting and no linter rewrites a file (see [tooling](README.md)). The assistant fixes the finding itself.
- **CSpell** checks it for unknown words.

A hook that finds a problem exits with the status code `2` and writes the tool's output to standard error, which is what makes the assistant read the finding and fix it rather than let it scroll past. Each hook is also guarded so that it does nothing when its tool is not installed in `node_modules`, so a fresh clone without `npm ci` stays quiet rather than failing confusingly.

Every hook reads the edited file's path from the JSON that Claude Code passes on standard input, with [`jq`](https://jqlang.org/). **Without `jq` installed, every hook silently does nothing**, because the path comes out empty and an empty path is skipped. Install it alongside Node.js (see [developer setup](developer-setup.md)).

The settings also allow the `Agent` tool, so delegating to a subagent needs no confirmation.

## Which Files Reach Them

Every hook ignores a file outside the repository, `"$CLAUDE_PROJECT_DIR"/*`, since an assistant also writes files elsewhere, such as scratch files or its own notes, which the repository's linters have no business checking. Inside the repository, every hook skips `node_modules/`, `template/` and `licenses/`, matching what the root's linter configurations exclude. That has a consequence worth knowing: **an assistant editing a body file gets no feedback at all.** No hook formats it, lints it or spell-checks it, so a mistake in the body is only ever found by rendering (see [testing](../conventions/testing.md)).

There is no `Stop` hook at the root, because the root has nothing to build.

## The Body's Hooks

[`template/.claude/settings.json`](../../template/.claude/settings.json) is the **generated project's** hook configuration, and a template file like any other. It runs the same three tools with the generated project's own configuration files at its root, also needs `jq`, ignores files outside the project, and skips SVGs and build output. Build output there is `"$CLAUDE_PROJECT_DIR"/build/*`, anchored to the project directory so that the documentation website's scripts in `docs/build/` are still formatted and checked. It also adds a `Stop` hook that builds the solution with `--configuration Release`, the only configuration that treats warnings as errors, so that an assistant cannot end a turn with an analyzer warning that would fail continuous integration. That hook names the solution through `[[ product_name ]]`, which is substituted like any other placeholder, and quotes it, because the product name may contain spaces.

A change to it changes the hooks of every project generated from now on. It is described from the generated project's side in its [Claude Code hooks](../../template/docs/developer-manual/tooling/claude-code-hooks.md) article, and verified in a render, where the hooks actually run.

When changing a hook on either side:

- Filter by path first and act second, so that an irrelevant file exits fast.
- Guard every tool invocation, so that a missing tool makes the hook a silent no-op.
- Keep the root's and the body's hooks alike where they do the same job, so that working on the template and working on a generated project feel the same.

## Project Instructions

Claude Code reads [`AGENTS.md`](../../AGENTS.md) as its project instructions from v2.1.277 on, and only while no `CLAUDE.md` exists in the working directory or above it. Do not add a `CLAUDE.md` next to it: the default setting would then ignore `AGENTS.md` entirely.

## Related

- [Tooling](README.md) — the tools these hooks run.
- [`AGENTS.md`](../../AGENTS.md) — the rules an assistant follows beyond what a hook can enforce.
- [Claude Code hooks](../../template/docs/developer-manual/tooling/claude-code-hooks.md) — the generated project's hooks.
