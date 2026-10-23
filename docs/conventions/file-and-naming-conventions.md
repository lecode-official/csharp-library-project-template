# File and Naming Conventions

This article covers how files and directories are named at the root of this repository and in the template body.

## Kebab-Case by Default

Files and directories at the root are named in **kebab-case**: `docs/project-template/`, `rendering-and-updating.md`, `scripts/refresh-licenses.py`. A Python script is named that way too, because it is run by its path and never imported as a module.

Every section of the documentation is a directory under [`docs/`](../README.md) with a `README.md` that indexes it.

## Well-Known Exceptions

Files with a conventional or tool-mandated name keep that name:

- **Files everyone recognizes by their standard name**: `README.md`, `AGENTS.md`, `CHANGELOG.md`, `LICENSE`.
- **Files whose name and place are dictated by the tool that reads them**: `copier.yml`, which Copier only ever looks for at the clone root, as well as `dprint.json`, `.cspell.json`, `.markdownlint.yml`, `.editorconfig`, `.gitignore` and `package.json`.
- **The vendored license texts**, which are named after their SPDX identifier exactly, as in `MIT.txt` and `LGPL-3.0-or-later.txt`. `template/LICENSE` builds the path from the answer with `"licenses/" ~ license ~ ".txt"`, so the file name *is* the identifier, casing included (see [licensing](../project-template/licensing.md)).

## The Body Uses the Generated Project's Names

A path under `template/` is the path the file will have in the generated project, so the body follows the generated project's [file and naming conventions](../../template/docs/developer-manual/conventions/file-and-naming-conventions.md): kebab-case by default, PascalCase inside a C# project's own source tree, one type per file, and project and solution files named after the product.

No file in the body carries a `.jinja` suffix. `_templates_suffix` is empty, so every file is a template under its real name (see [authoring](../project-template/authoring.md#no-jinja-extension)).

## Placeholders in Paths

Copier renders path names too, and which answer goes into a path is decided by what the path is for:

- **A directory takes a slug**, never the product name: `template/source/[[ library_slug ]]/`. A slug is lowercase and dash-separated by the question's contract, so the directory follows the kebab-case rule once rendered.
- **A project or solution file takes the product name**, spaces included: `template/source/[[ product_name ]].slnx`, `template/source/[[ library_slug ]]/[[ product_name ]].csproj`, `template/tests/unit-tests/[[ product_name ]] Unit Tests.csproj`. The directory says where the project sits, and the file says what the product is called.
- **Anything else takes no placeholder.** A file named after an answer is a file every consumer has to find under a different name, and every shell command that names it needs quoting.

`[` and `]` are character-class syntax in a glob, so a shell pattern that spells out a placeholder path literally matches nothing. Quote such paths, or match the directory with a `*`.

One file in the body has a name and place Copier depends on: [`template/.copier-answers.yml`](../../template/.copier-answers.yml) has to be there, or a generated project cannot be updated (see [template structure](../project-template/template-structure.md#what-copier-requires-of-this-layout)).

## Related

- [Template structure](../project-template/template-structure.md) — what lives at the root and what lives in the body.
- [Questions](../project-template/questions.md) — the slugs and names that end up in paths.
- [C# style](csharp-style.md) — the naming rules inside a C# file.
- [File and naming conventions](../../template/docs/developer-manual/conventions/file-and-naming-conventions.md) — the generated project's full rule set.
