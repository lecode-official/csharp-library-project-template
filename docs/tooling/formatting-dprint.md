# Code Formatting (dprint)

This article covers code formatting, which is owned entirely by [dprint](https://dprint.dev), on both sides of the split.

## The Root's Configuration

The root's [`dprint.json`](../../dprint.json) formats the template's own files: Markdown, JSON, YAML and TOML. It has no C# or XML plugin, because the root has no such files.

It excludes three things:

- **`template/`**, because the files in it are Jinja templates rather than valid documents of their own type. Formatting them here would mangle them, or fail on them outright.
- **`licenses/`**, because the vendored license texts are verbatim copies of upstream documents.
- **The lock files**, whose formatting belongs to the tool that writes them.

## Running It

```shell
npm run format            # the root's files, in place
npx dprint check "**/*"   # check only, which is what npm run lint does
```

`npx` resolves the version pinned in the root's `package.json` out of `node_modules/.bin`. Visual Studio Code runs dprint on save (see [editor integration](editor-integration.md)), and the Claude Code hooks run it after every edit (see [Claude Code hooks](claude-code-hooks.md)).

## dprint Owns Formatting, Linters Must Not

On both sides, the linters are configured never to enforce a rule that dprint already decides, and a disabled lint rule carries a comment saying which dprint setting owns that decision. When adding a lint rule, never enable one that conflicts with dprint.

## Trailing-Comma JSONC Files

Several JSON files are authored as JSONC, with `//` comments and trailing commas, and each one is listed in `json.jsonTrailingCommaFiles`. That list **replaces** the plugin's defaults rather than extending them, so adding a JSONC file means listing it and keeping every existing entry.

The two configurations list different files, because the two sides have different files: the root lists its own `.cspell.json`, `dprint.json` and `.vscode/*.json`, and the body lists the generated project's, including its own `.cspell.json` and the launch configurations. A file read by a strict JSON parser, such as `.claude/settings.json`, is deliberately absent from both.

## Related

- [Line length](../conventions/line-length.md) — the 150-character limit, and what a placeholder does to it.
