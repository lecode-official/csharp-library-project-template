# Claude Code Hooks

This article covers the Claude Code hooks in [`.claude/settings.json`](../../../.claude/settings.json) and which files reach which hook.

## What the Hooks Do

`PostToolUse` hooks run after `Edit`, `Write`, and `NotebookEdit`, and format or lint the changed file with dprint, MarkdownLint, or CSpell — whichever applies to that file's type and location. A `Stop` hook builds the solution before a session ends, so that a change which does not compile, or which leaves an analyzer warning behind, cannot quietly end a turn.

A hook that finds a problem exits with the status code `2` and writes the tool's output to standard error. That combination is what makes the assistant read the finding and fix it, rather than the failure scrolling past unnoticed. The formatting hook is the exception: it rewrites the file in place and does not fail the turn, because there is nothing for anyone to decide.

## dprint Formats, MarkdownLint Only Reports

The MarkdownLint hook runs `markdownlint-cli2` without `--fix`. It reports a finding and leaves the file alone, and the assistant fixes it. Formatting is dprint's job alone (see [formatting](formatting-dprint.md)), and no linter reformats a file behind its back. Two tools rewriting the same file in turn would only fight over it.

## The Hooks Need `jq`

Claude Code hands a hook its input as JSON on standard input, and every `PostToolUse` hook reads the edited file's path out of it with [`jq`](https://jqlang.org/). **Without `jq` installed, every one of them silently does nothing.** The path comes out empty, and an empty path is one of the cases each hook skips. Install `jq` through the system's package manager (see [developer setup](developer-setup.md#jq-for-the-claude-code-hooks)).

## Which Files Reach Which Hook

Each hook filters by path before it does anything, so that an edit to a build artifact does not trip a tool that has no opinion about it. First of all, every hook ignores a file outside the project, `"$CLAUDE_PROJECT_DIR"/*`: an assistant also writes files elsewhere, such as scratch files or its own notes, and the project's linters have no business checking them, let alone failing the edit because of them. Inside the project:

- **dprint** sees everything except build output, `node_modules`, and SVGs — it is the only tool here that formats C#, XML, JSON, YAML and TOML as well as Markdown.
- **MarkdownLint** sees `.md` files only, again except build output and `node_modules`.
- **CSpell** sees everything except build output, `node_modules`, and SVGs.

Build output means `"$CLAUDE_PROJECT_DIR"/build/*`, the project's own `build/` directory at the repository root, into which every project's `bin` and `obj` are redirected (see [architecture](../architecture.md#build-output)), and into which the documentation website is built. The pattern is anchored to the project directory on purpose. A bare `*/build/*` would also match `docs/build/`, whose Python scripts are source code like any other, and are formatted and checked like any other.

Each `PostToolUse` hook also checks that its tool is installed, with a guard such as `[ -x node_modules/.bin/dprint ] || exit 0`, so that before the first `npm ci` a hook does nothing rather than fail every edit.

## The `Stop` Hook Builds the Solution

The `Stop` hook runs `dotnet build` against the solution, with `--configuration Release`. Only a Release build treats warnings as errors (see [static code analysis](static-code-analysis.md)), and Release is what [continuous integration](continuous-integration.md) builds. A Debug build would let a turn end with an analyzer warning that then fails the pull request. The Release build makes the assistant fix it before it stops.

It is guarded so that it does nothing when there is nothing to build, or nothing to build it with:

```shell
[ -f "source/[[ product_name ]].slnx" ] || exit 0; command -v dotnet >/dev/null 2>&1 || exit 0;
```

Without the first guard, a session that only touched documentation in a checkout whose solution has been renamed would end with a confusing build error rather than with a clean stop. The second one does the same for a machine without the .NET SDK.

A build is used rather than a separate type check because in C# they are the same thing — the compiler is the type checker, so there is no cheaper check to run instead.

## When Adding a New Hook

A new hook filters by path first and acts second, so that an irrelevant file exits fast. If it shells out to a tool that might not be installed, guard the invocation the way the existing hooks do: a missing tool should make the hook a silent no-op, never a confusing failure.

## Project Instructions

Claude Code reads [`AGENTS.md`](../../../AGENTS.md) as its project instructions from v2.1.277 on, and only while no `CLAUDE.md` exists in the working directory or above it. Do not add a `CLAUDE.md` next to it: the default setting would then ignore `AGENTS.md` entirely.

## Related

- [Tooling](README.md) — the formatting and linting tools these hooks run.
- [`AGENTS.md`](../../../AGENTS.md) — the rules an assistant follows beyond what a hook can enforce.
- [Architecture](../architecture.md) — why `build/` is excluded from every hook.
- [Developer setup](developer-setup.md) — installing `jq` and the tools the hooks run.
