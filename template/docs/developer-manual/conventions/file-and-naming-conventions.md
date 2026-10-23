# File and Naming Conventions

This article covers how files and directories are named throughout the repository.

## Kebab-Case by Default

Files and directories are named in **kebab-case** — lowercase words separated by hyphens — for example `sample-app`, `unit-tests`, `developer-manual`, `formatting-dprint.md`. This applies repository-wide: the project directories under [`source/`](../../../source/), the [`docs/`](../README.md) tree, and every Markdown article.

## Well-Known Exceptions

Files with a conventional, tool- or ecosystem-mandated name keep that name instead of being renamed to kebab-case. This covers two kinds of file:

- **Files everyone recognizes by their standard name**: `README.md`, `AGENTS.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTORS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- **Files whose name is dictated by the tool that reads them**: `.editorconfig`, `.gitignore`, `.gitattributes`, `dprint.json`, `.cspell.json`, `.markdownlint.yml`, `.globalconfig`, `global.json`, `Directory.Build.props`, `Directory.Packages.props`, `packages.lock.json`. Renaming these would simply stop the tool from finding them.

## PascalCase Inside a C# Project

Inside a C# project's own source tree, directories and files switch to **PascalCase** — the library's `Greeter` type lives in `source/[[ library_slug ]]/Greeter.cs`, and a type in a namespace folder would live in, say, `source/[[ library_slug ]]/Formatting/GreetingFormatter.cs`. This follows the standard .NET convention of naming a file after the single type it contains, and grouping related types into a PascalCase namespace folder.

The project's own top-level folder still follows the repository's kebab-case rule. The switch to PascalCase only happens once you are inside the project, looking at its namespaces and types.

## Project and Solution Files Are Named After the Product

The `.csproj` and `.slnx` files are named after the product, **spaces included**, rather than after either convention:

- The solution — `source/[[ product_name ]].slnx`
- The library — `source/[[ library_slug ]]/[[ product_name ]].csproj`
- The sample app — `source/sample-app/[[ product_name ]] Sample App.csproj`
- The unit tests — `tests/unit-tests/[[ product_name ]] Unit Tests.csproj`

So a project file's base name deliberately does **not** match its directory name. The directory says where the project sits in the repository. The file says what the product is called.

## Namespaces and Assembly Names

- The **root namespace** is PascalCase with no spaces and no dots beyond the ones it deliberately nests with: `[[ root_namespace ]]` for the library, `[[ root_namespace ]].SampleApp` and `[[ root_namespace ]].UnitTests` for the other two.
- The **assembly name** is the project file's base name, so it keeps the spaces: `[[ product_name ]] Unit Tests`. This is the name `InternalsVisibleTo` references, which is why that attribute names the assembly rather than the package.
- The **package id** is PascalCase with no spaces: `[[ package_id ]]`. NuGet ids cannot contain spaces.

## One Type per File

A C# file declares one top-level type, and is named after it. A type that only supports another one gets a file of its own, or becomes a nested type of the type it supports. See [C# style](csharp-style.md).

## Test Files

Test files live in `tests/unit-tests/`, mirroring the namespace and folder of the type they test, and are named `<TypeName>Tests.cs`. See [testing](testing.md).

## Related

- [Architecture](../architecture.md) — where these directories and projects sit in the repository.
- [C# style](csharp-style.md) — the naming rules that apply once you are inside a C# file.
- [Testing](testing.md) — the test project's own mirroring rule.
