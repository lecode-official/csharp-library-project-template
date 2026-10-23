# Architecture

This article covers how the repository is laid out and how the .NET projects inside it are configured.

## Repository Layout

The repository is organized into a few top-level directories:

- [`source/`](../../source/) — the source code of [[ product_name ]] itself, and the sample app that demonstrates it.
- [`docs/`](../README.md) — this documentation.

Top-level files round out the repository. [`README.md`](../../README.md) is the project's front door, [`CHANGELOG.md`](../../CHANGELOG.md) records what changed in each version, [`CONTRIBUTORS.md`](../../CONTRIBUTORS.md) lists everyone who has contributed, and [`LICENSE`](../../LICENSE) is the full text of the license. [`CONTRIBUTING.md`](../../CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md) and [`SECURITY.md`](../../SECURITY.md) round out the community-facing files a repository host recognizes by name. [`global.json`](../../global.json) pins the exact .NET SDK version.

## Solution and Projects

[`source/[[ product_name ]].slnx`](../../source/) is the solution file, in the newer XML-based `.slnx` format rather than the classic `.sln` format. It sits in `source/` rather than at the repository root. It groups two projects:

- **`[[ library_slug ]]`** — the library itself.
- **`sample-app`** — a runnable sample application that references the library through a project reference and demonstrates how it is used.

Both target `[[ target_framework ]]`, and both enable `<Nullable>` and `<ImplicitUsings>`.

The library also sets `<GenerateDocumentationFile>`, so that the XML documentation comments in the source (see [C# style](conventions/csharp-style.md)) ship alongside the compiled assembly and reach a consumer's editor tooltips.

## Build Output

[`source/Directory.Build.props`](../../source/Directory.Build.props) redirects every project's `bin`/`obj` output out of its own folder and into the repository root's `build/<project folder name>/` instead — `build/[[ library_slug ]]/` and `build/sample-app/` — so that the source tree stays free of build output. It uses `$([System.IO.Path]::GetFileName($(MSBuildProjectDirectory)))` to read each project's own folder name at evaluation time, so the one file covers every project under `source/` without listing them individually.

The entire `build/` directory is generated and covered by [`.gitignore`](../../.gitignore) — nothing under it is ever committed.

## Versioning and Licensing

[`CHANGELOG.md`](../../CHANGELOG.md) is the human-readable history of what each version changed. It is not generated from Git history, so it is updated by hand.

The project is licensed under `[[ license ]]`, and [`LICENSE`](../../LICENSE) carries the full text of the license.

## Related

- [C# style](conventions/csharp-style.md) — the coding conventions for the source.
- [File and naming conventions](conventions/file-and-naming-conventions.md) — why the directories and the project files are named the way they are.
- [Tooling](tooling/README.md) — the tools that build and test the projects.
- [Contributing](contribution-guide.md) — how to propose and submit changes.
