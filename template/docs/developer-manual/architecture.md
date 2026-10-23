# Architecture

This article covers how the repository is laid out and how the .NET projects inside it are configured.

## Repository Layout

The repository is organized into a few top-level directories:

- [`source/`](../../source/) — the source code of [[ product_name ]] itself, and the sample app that demonstrates it.
- [`tests/`](../../tests/) — the unit tests.
- [`docs/`](../README.md) — this documentation, including the [documentation website](tooling/documentation-website.md)'s build scripts (`docs/build/`), wired in via [`properdocs.yml`](../../properdocs.yml).

Top-level files round out the repository. [`README.md`](../../README.md) is the project's front door, [`CHANGELOG.md`](../../CHANGELOG.md) records what changed in each version, [`CONTRIBUTORS.md`](../../CONTRIBUTORS.md) lists everyone who has contributed, and [`LICENSE`](../../LICENSE) is the full text of the license. [`CONTRIBUTING.md`](../../CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md) and [`SECURITY.md`](../../SECURITY.md) round out the community-facing files a repository host recognizes by name. [`global.json`](../../global.json) pins the exact .NET SDK version, and [`.config/dotnet-tools.json`](../../.config/dotnet-tools.json) is the local tool manifest — both follow the same exact-version-only rule as everything else (see [dependency management](conventions/dependency-management.md)). The configuration of the code formatter, the linters, and the static code analysis lives at the repository root too, where each tool discovers it on its own (see [tooling](tooling/README.md)).

## Solution and Projects

[`source/[[ product_name ]].slnx`](../../source/) is the solution file, in the newer XML-based `.slnx` format rather than the classic `.sln` format. It sits in `source/` rather than at the repository root, and reaches back out with a relative path to pull in the test project. It groups three projects:

- **`[[ library_slug ]]`** — the library itself, packed and published as the `[[ package_id ]]` NuGet package.
- **`sample-app`** — a runnable sample application that references the library through a project reference and demonstrates how it is used.
- **`unit-tests`** — the xUnit test project, living under [`tests/`](../../tests/) rather than `source/` (see [testing and code coverage](tooling/testing-and-code-coverage.md)).

All three target `[[ target_framework ]]`, and all three enable `<Nullable>` and `<ImplicitUsings>`.

All three also set `<GenerateDocumentationFile>`, each for its own reason:

- **The library**, so that the XML documentation comments in the source (see [C# style](conventions/csharp-style.md)) ship alongside the compiled assembly and reach a consumer's editor tooltips — and so that the [documentation website](tooling/documentation-website.md) can generate its API reference from them.
- **The test project**, so that a missing documentation comment on a test class or method fails the build.
- **The sample app**, which is not documented for a consumer, because the analyzers need the documentation file all the same. Without it, the code-style rule IDE0005 cannot run in the build and StyleCop Analyzers turns its documentation rules off (SA0001), and both report that as an error (see [static code analysis](tooling/static-code-analysis.md)).

The library also grants the test project access to its `internal` members through `InternalsVisibleTo`, so internal types can be unit tested directly (see [testing](conventions/testing.md)). Both the sample app and the test project set `<IsPackable>false</IsPackable>` — neither is published.

## The Sample App Is Not Only a Sample

The sample app earns its place twice. It demonstrates the library, and it is also what the [documentation website](tooling/documentation-website.md) builds in order to generate the API reference: a class library's own build output does not include its NuGet dependencies, and the documentation generator needs every dependency of the library assembly loadable by reflection. Building the sample app transitively builds the library and copies the assembly, its XML documentation file, and the full dependency closure into one output folder.

Deleting the sample app therefore breaks the API reference. If it ever goes, the generator has to be pointed at something else that produces a complete output folder.

## Shared Build Settings

[`Directory.Build.props`](../../Directory.Build.props) at the repository root holds the build settings every project shares: the static code analysis settings, warnings as errors in Release builds, deterministic builds on the continuous integration runner (see [versioning](conventions/versioning.md#the-package-and-its-symbols)), and the dependency audit (see [static code analysis](tooling/static-code-analysis.md)). MSBuild only imports the `Directory.Build.props` closest to a project, so the two files below import the root one explicitly before adding their own settings.

[`Directory.Packages.props`](../../Directory.Packages.props) turns on Central Package Management: it declares the version of every NuGet package, and the project files reference packages without a version (see [dependency management](conventions/dependency-management.md)).

## Build Output

Two `Directory.Build.props` files redirect every project's `bin`/`obj` output out of its own folder and into the repository root's `build/<project folder name>/` instead — `build/[[ library_slug ]]/`, `build/sample-app/` and `build/unit-tests/` — so that the source tree stays free of build output:

- [`source/Directory.Build.props`](../../source/Directory.Build.props) covers every project under `source/`, using `$([System.IO.Path]::GetFileName($(MSBuildProjectDirectory)))` to read each project's own folder name at evaluation time, so the one file covers them all without listing them individually.
- [`tests/unit-tests/Directory.Build.props`](../../tests/unit-tests/Directory.Build.props) covers the test project alone, so it hard-codes `build/unit-tests/` — there is only the one project under `tests/`, so the folder-name lookup would be needless indirection.

The documentation website builds into `build/documentation-website/` alongside them, via `site_dir` in [`properdocs.yml`](../../properdocs.yml). The entire `build/` directory is generated and covered by [`.gitignore`](../../.gitignore) — nothing under it is ever committed.

## Versioning and Licensing

The NuGet package version is the `<Version>` property of the library's project file. [`CHANGELOG.md`](../../CHANGELOG.md) is the human-readable history of what each version changed. It is not generated from Git history, so it is updated by hand (see [versioning](conventions/versioning.md)).

The project is licensed under `[[ license ]]`. The library's project file declares it as `<PackageLicenseExpression>`, which is the SPDX identifier NuGet expects, and [`LICENSE`](../../LICENSE) carries the full text of the same license.

## Related

- [C# style](conventions/csharp-style.md) — the coding conventions for the source.
- [File and naming conventions](conventions/file-and-naming-conventions.md) — why the directories and the project files are named the way they are.
- [Tooling](tooling/README.md) — the linters, the code formatter, and the editor setup.
- [Testing and code coverage](tooling/testing-and-code-coverage.md) — running the unit tests.
- [Contributing](contribution-guide.md) — how to propose and submit changes.
