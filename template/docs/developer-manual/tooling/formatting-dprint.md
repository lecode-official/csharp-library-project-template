# Code Formatting (dprint)

This article covers code formatting, which is owned entirely by [dprint](https://dprint.dev).

Configuration lives in [`dprint.json`](../../../dprint.json). dprint formats C# through the Roslyn plugin, XML — including `.csproj` and `.slnx`, which are explicitly associated with the markup plugin because their extensions are not recognized by default — and Markdown, JSON, YAML and TOML.

The Roslyn plugin only drives whitespace, newlines, and indentation. It has no equivalent of the `csharp_style_*` or `dotnet_*` analyzer preferences. Those, and most of the structural conventions in [C# style](../conventions/csharp-style.md), are checked by the analyzers instead (see [static code analysis](static-code-analysis.md)), which report a problem but never reformat anything. A plugin for a file type the repository has no use for can be removed, together with its configuration section.

## Running It

```shell
npm run format            # the whole repository, in place
```

To check formatting without modifying anything, which is what [continuous integration](continuous-integration.md) does:

```shell
npx dprint check "**/*"
```

dprint is pinned in [`package.json`](../../../package.json) and locked in `package-lock.json` like the other tools (see [dependency management](../conventions/dependency-management.md)), so `npx` resolves the pinned version out of `node_modules/.bin` rather than downloading one.

## dprint Owns Formatting — Linters Must Not

Because dprint is the single source of truth for formatting, the linters are configured to disable any rule that would reformat code. Every such disabled rule carries a comment in its configuration saying which dprint setting owns that decision instead. When adding a lint rule, never enable one that conflicts with dprint.

## Some JSON Files Are Trailing-Comma JSONC

Several JSON files in this repository are authored as JSONC, with `//` comments and trailing commas, including files whose extension has to stay `.json` for the tool that reads them — [`.cspell.json`](../../../.cspell.json) and `dprint.json` itself. Each one is listed explicitly in `json.jsonTrailingCommaFiles` in [`dprint.json`](../../../dprint.json).

[`global.json`](../../../global.json) is the one file in between. It carries `//` comments, but it is not listed in `jsonTrailingCommaFiles`, so dprint writes it without trailing commas. The same goes for [`.config/dotnet-tools.json`](../../../.config/dotnet-tools.json).

Since `jsonTrailingCommaFiles` **replaces** the plugin's defaults rather than extending them, adding a new JSONC-style file means listing it there and keeping every existing entry in place. A file that is not listed has its trailing commas removed, which breaks nothing — but a file that *is* listed and is read by a strict JSON parser does break, which is why a web app manifest is deliberately absent from the list.

## Related

- [Line length](../conventions/line-length.md) — the 150-character limit dprint enforces, and where it is also a lower limit.
- [C# style](../conventions/csharp-style.md) — what the Roslyn plugin does and does not decide.
- [Continuous integration](continuous-integration.md) — the check-mode invocation.
- [Tooling](README.md) — the full tool set.
