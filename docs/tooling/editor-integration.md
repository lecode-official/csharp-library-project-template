# Visual Studio Code Integration

This article covers the Visual Studio Code setup under the root's [`.vscode/`](../../.vscode/), and how it differs from the editor configuration the template body ships.

## Shared and Local Configuration

The root splits its workspace configuration the same way a generated project does, with the [Workspace Config Plus](https://marketplace.visualstudio.com/items?itemName=Swellaby.workspace-config-plus) extension. For `settings` and `tasks`, it merges two source files into the one the editor actually loads:

- `settings.shared.json` and `tasks.shared.json` are committed, and apply to everyone working on the template.
- `settings.local.json` and `tasks.local.json` are per-developer and ignored by Git.
- `settings.json` and `tasks.json` are **generated** from the two layers above, with the local layer winning.

The extension is effectively mandatory. Without it, no `settings.json` is generated, and every shared setting silently does nothing.

The rules are the generated project's rules:

- **Never edit a generated file.** It is overwritten on every change, and it is marked read-only through `files.readonlyInclude`.
- **Change a shared file only for something useful to everyone working on the template.** The shared files are marked read-only in the editor too, so changing one is a deliberate act, made in a reviewed change.
- **Everything personal goes in the matching local file.**

## Settings

[`settings.shared.json`](../../.vscode/settings.shared.json) is the shared layer. Most of it mirrors a generated project's settings:

- **A 150-character ruler**, matching the root's `lineWidth` (see [line length](../conventions/line-length.md)).
- **File associations** that map `.cspell.json`, `dprint.json`, `global.json`, `dotnet-tools.json` and `.vscode/*.json` to JSONC, so their comments are not reported as syntax errors.
- **Exclusions and file nesting**, which nest the configuration files under `.editorconfig`, `copier.yml`, `package.json` and `README.md`.
- **Branch protection** on `main`, and the same Git behavior a generated project has: the merge editor on conflicts, force-push allowed, rebase on sync.
- **CSpell and MarkdownLint** pointed at the root's own [`.cspell.json`](../../.cspell.json) and [`.markdownlint.yml`](../../.markdownlint.yml), not at the body's.
- **dprint as the default formatter**, with format-on-save on.

Because the editor uses the root's configuration everywhere, it reports nothing useful for a file under `template/`. CSpell and dprint skip the body by their configuration, and MarkdownLint judges a body article by the root's rules rather than the generated project's. Check body files in a render instead.

## Tasks

[`tasks.shared.json`](../../.vscode/tasks.shared.json) mirrors the root's npm scripts: Install Dependencies, Format, Lint Markdown, Lint Spelling, and the combined Lint, which is the default task of the `test` group. Every npm task depends on Install Dependencies, and the lint tasks carry problem matchers, so findings land in the Problems panel. There is no build or test task, because the root has nothing to build.

## The Body's Editor Configuration

The files under [`template/.vscode/`](../../template/.vscode/) are the **generated project's** editor configuration: its own shared settings, tasks, launch configurations and extension recommendations. Editing one is a body change like any other, and it is described in the generated project's [editor integration](../../template/docs/developer-manual/tooling/editor-integration.md) article.

If you open `template/` on its own in the editor, Workspace Config Plus generates a `settings.json`, `tasks.json` and `launch.json` next to the shared files there. Those are ignored by Git, like their counterparts at the root, so they never reach a render taken from a commit. Leave them alone.

## Extensions

[`extensions.json`](../../.vscode/extensions.json) recommends the extensions that back the settings above, plus Claude Code, a few Markdown conveniences, and `.gitignore` language support. Unlike the body's list, it does not recommend the C# extension, because the root has no C# to edit as a project.

## Related

- [Developer setup](developer-setup.md) — installing the editor and its extensions.
- [Formatting (dprint)](formatting-dprint.md), [MarkdownLint](linting-markdownlint.md), [CSpell](spell-checking-cspell.md) — the tools these settings configure.
- [Editor integration](../../template/docs/developer-manual/tooling/editor-integration.md) — the generated project's editor setup.
