# Visual Studio Code Integration

This article covers the Visual Studio Code setup under [`.vscode/`](../../../.vscode/).

## Shared and Local Configuration

The workspace configuration is split with the [Workspace Config Plus](https://marketplace.visualstudio.com/items?itemName=Swellaby.workspace-config-plus) extension (`Swellaby.workspace-config-plus`, recommended in [`extensions.json`](../../../.vscode/extensions.json)). For `settings`, `tasks`, and `launch`, the extension reads two source files and merges them into the file Visual Studio Code actually loads:

- `settings.shared.json`, `tasks.shared.json`, `launch.shared.json` — checked into Git, apply to every developer.
- `settings.local.json`, `tasks.local.json`, `launch.local.json` — per-developer, ignored by Git (see [`.gitignore`](../../../.gitignore)).
- `settings.json`, `tasks.json`, `launch.json` — **generated** by the extension from the two layers above.

The local layer wins over the shared layer, so each developer can override or extend the shared configuration without touching it.

The extension is effectively mandatory. Without it installed, no `settings.json` is generated at all, and every shared setting silently does nothing — the editor simply behaves as though the repository had no configuration.

### Rules

- **Never edit a generated file.** `settings.json`, `tasks.json`, and `launch.json` are produced by the extension and overwritten on every change, so any manual edit is lost. They are also Git-ignored, and `settings.shared.json` additionally marks them read-only through `files.readonlyInclude`, so the editor refuses the edit rather than letting it be silently discarded.
- **Change a `*.shared.json` file only for things useful to every developer.** A shared change is committed and affects the whole team, so it has to be genuinely common: a project-wide setting, a build or debug configuration, a lint integration.
- **Everything personal goes in the matching `*.local.json` file.** Icon themes, personal editor tweaks, local-only tasks — those belong in the local layer, never in the shared one.

## Settings

[`settings.shared.json`](../../../.vscode/settings.shared.json) is the shared layer. What it does, and why:

- **A 150-character editor ruler**, matching dprint's `lineWidth` (see [line length](../conventions/line-length.md)), so the limit is visible while typing rather than discovered by the formatter.
- **File associations**, mapping `.cspell.json`, `dprint.json`, `global.json`, `dotnet-tools.json`, and `.vscode/*.json` to JSONC, so that the comments in them are highlighted as comments rather than reported as syntax errors, and `.globalconfig` files to INI, so that the analyzer configuration is highlighted at all.
- **Explorer, watcher, and search exclusions**, hiding the `build/` directory and operating system clutter, so that the redirected `bin` and `obj` output never shows up in a search result.
- **File nesting**, collapsing the configuration files under `.editorconfig` and `package.json`, and the generated editor files under their shared counterparts.
- **Branch protection** on `[[ default_branch ]]` and `[[ integration_branch ]]`, which stops a commit through the editor's own Git UI — not through the terminal (see [Git workflow](../conventions/git-workflow.md)).
- **Git behavior**: always open the merge editor on a conflict, allow force-push (this project amends regularly), fetch all branches and prune on pull, and push tags and rebase rather than merge when syncing.
- **CSpell**, importing [`.cspell.json`](../../../.cspell.json) and raising the diagnostic level from information to error, so a spelling mistake looks like the problem it is. `ignorePaths` and `useGitignore` are reset, because the extension's defaults would otherwise override the imported configuration.
- **MarkdownLint**, pointed at [`.markdownlint.yml`](../../../.markdownlint.yml).
- **The solution path**, pointed at `source/[[ product_name ]].slnx`, so that the C# extension does not have to guess. Without it, the solution's non-standard location — in `source/`, not the repository root — and its cross-directory reference to the test project under `tests/` can lead the extension to miss part of the solution and report a file as belonging to no project.
- **dprint as the default formatter**, with format-on-save on and format-on-type off.

## Tasks

[`tasks.shared.json`](../../../.vscode/tasks.shared.json) mirrors the npm and `dotnet` commands as tasks: Install Dependencies, Format, Check Formatting, Lint Markdown, Lint Spelling, the combined Lint, Build, Test, and Run Sample App. The npm-backed tasks depend on Install Dependencies, so none of them can run against a stale or missing `node_modules`.

Lint is the default task of the `test` group and Build the default of the `build` group, so "Run Test Task" and "Run Build Task" do the obvious thing.

Every linter task carries a problem matcher, so findings land in the Problems panel instead of only in the terminal. The .NET tasks use the built-in `$msCompile` matcher. MarkdownLint and CSpell have no built-in matcher, so the tasks define custom patterns inline — and the aggregate Lint task repeats both, because a task only reports through the matchers it declares itself.

## Launch Configuration

[`launch.shared.json`](../../../.vscode/launch.shared.json) holds the debug configurations everyone shares. It ships with one, Debug Sample App, which runs the Build task first and then launches the sample app under the `coreclr` debugger, from its output under `build/sample-app/` (see [architecture](../architecture.md#build-output)), with `source/sample-app` as the working directory and the integrated terminal as its console. A personal debug configuration goes into `launch.local.json` instead.

## Extensions

[`extensions.json`](../../../.vscode/extensions.json) recommends the extensions that back all of the above, plus a few editing conveniences and `.gitignore` language support.

Which engine an extension uses matters, because it decides whether the editor and the command line can disagree:

- **MarkdownLint and CSpell bundle their engines.** They read the same configuration files, so the rules stay consistent, but their engine version can differ slightly from the pinned one that [continuous integration](continuous-integration.md) runs.
- **dprint does not bundle an engine.** It runs a `dprint` executable, together with the plugins declared in [`dprint.json`](../../../dprint.json). This project pins `dprint` as a devDependency, so once `npm install` has run, the project-local executable is what the extension finds, which is what keeps the editor in step with continuous integration. Before that, it falls back to a globally installed `dprint`, and the version is then whatever that happens to be.

## Related

- [Tooling](README.md) — the tools these settings configure.
- [Formatting (dprint)](formatting-dprint.md), [MarkdownLint](linting-markdownlint.md), [CSpell](spell-checking-cspell.md) — the individual tools.
- [Continuous integration](continuous-integration.md) — the pinned versions these extensions approximate.
- [Developer setup](developer-setup.md) — installing all of this on a fresh machine.
