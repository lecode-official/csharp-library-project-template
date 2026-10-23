# Changelog

All notable changes to the C# library project template are documented here, newest release first. Each release corresponds to an annotated Git tag of the same name.

## Release v1.0.0

*Release date to be determined.*

- Added the tooling of the template repository itself: formatting with dprint, Markdown linting with MarkdownLint, spell checking with CSpell, the Visual Studio Code integration, and the Claude Code hooks.
- Added the conventions of the template repository, its `AGENTS.md`, and its community files.
- Added the Copier template: the core questions with their validators, and the split between the template repository and the template body in `template/`.
- Added the `license` question, with ten vendored license texts and the script that refreshes them.
- Added the documentation of the generated project: its read me, `AGENTS.md`, community files, changelog, and the developer and user manuals.
- Added the C# solution of the generated project: the library, the sample app, and the pinned .NET SDK.
- Added the NuGet packaging of the library: package metadata, inherited documentation comments, package validation, and a symbol package.
- Added the unit test project of the generated project, based on xUnit v3 and Microsoft.Testing.Platform, with code coverage.
- Added Central Package Management, lock files, and the NuGet vulnerability audit to the generated project.
- Added formatting with dprint, Markdown linting with MarkdownLint, and spell checking with CSpell to the generated project.
- Added strict static code analysis to the generated project, with the .NET analyzers, StyleCop Analyzers, Roslynator, and Nullable.Extended.
- Added the documentation website of the generated project, built with ProperDocs, including a generated API reference.
