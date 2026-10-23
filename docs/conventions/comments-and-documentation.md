# Comments and Documentation

This article covers how comments and documentation are written on both sides of the split: in this repository's own files at the root, and in the files of the template body.

## Two Audiences

A comment or an article at the root explains the **template** to someone working on it. A comment or an article in the body explains the **generated project** to someone working on that project, who may never have heard of this template.

That decides what each side may talk about:

- **The body never explains the template.** A body file does not mention Copier, rendering, or why it is templated the way it is. It reads as though the generated project had been written by hand. The exceptions are the few things a generated project's developer genuinely needs to know about its origin, such as `.copier-answers.yml` and `copier update`, and the placeholder code that tells its reader to replace it.
- **The template's reasoning lives at the root.** Why a body file uses `| trim`, why a table has no placeholder in it, why a question is declared where it is: that goes into an article under [`docs/`](../README.md) or a comment in [`copier.yml`](../../copier.yml), never into the body.
- **Never hide it in the body either.** An `[% if false %]` block is the workaround this layout exists to remove (see [template structure](../project-template/template-structure.md)). A Jinja comment, `[# … #]`, is no better: it disappears on render, but the line it stood on stays behind as an empty line, and the explanation is invisible to anyone reading the documentation.

The same goes for links. A body file never links to anything outside `template/`, because a generated project has no `docs/`, `licenses/` or `copier.yml` of its own, so the link breaks in every project rendered from it. When a body comment refers to an article, it refers to the generated project's own article.

## C# Documentation Comments

The C# in the body follows these rules for its documentation comments:

- Every type and every member, including `private` ones and the test project's, has an XML documentation comment.
- The wording is fixed: `Represents a ...` for types, `Contains ...` for fields and constants, a third-person verb for methods, `Gets ...` or `Gets or sets ...` for properties.
- A `<returns>` element starts with "Returns". C# keywords are marked up with `<see langword="..."/>`, types and members with `<see cref="..."/>`, and other code with `<c>...</c>`, because a documentation comment is XML, not Markdown.
- `<inheritdoc/>` where a member implements or overrides one and has nothing to add.
- A `<summary>` explains why the member exists, not only what it does.

A documentation comment in the body is read by a generated project's developer and published in its API reference, so it describes the generated code in its own terms. A placeholder may appear in one, but it changes the line's rendered width (see [line length](line-length.md)).

## Comments in Configuration Files

Both sides carry heavily commented configuration: the JSONC files ([`dprint.json`](../../dprint.json), [`.cspell.json`](../../.cspell.json), `.vscode/*.json`), the YAML files ([`copier.yml`](../../copier.yml), [`.markdownlint.yml`](../../.markdownlint.yml), the body's workflows), `.editorconfig`, `.gitignore`, and the XML comments in the body's project files. The rules are the same on both sides:

- **A comment explains why a setting exists**, or what would go wrong without it. A setting whose purpose is obvious from its name needs no comment.
- **A comment sits on its own line above the setting it describes**, never at the end of that line.
- **A comment follows the plain-comment punctuation rule.** Sentences are separated by semicolons, and the last one takes no terminal punctuation.
- **A comment is filled to the 150-character limit**, and broken only where the next word would not fit (see [line length](line-length.md)).

A root comment refers to an article by its path, as in `(see docs/project-template/template-structure.md)`. A body comment refers to the generated project's article instead, either by its title, as in `(see Dependency Management)`, or by its path inside the generated project.

## Prose and Plain Comments

The punctuation rule is the same throughout the repository:

- **Prose** ends its sentences with periods and never joins two sentences with a semicolon. That covers Markdown, XML documentation comments, and the `help` strings and `validator` messages in [`copier.yml`](../../copier.yml), which are the only explanation a person rendering the template ever sees.
- **Plain comments** (`//`, `#`, `<!-- -->`) do the reverse. Sentences are separated by semicolons, and the last one takes no terminal punctuation.

Whatever the kind, a comment explains a non-obvious *why*: a hidden constraint, an ordering requirement, a workaround, a Copier behavior that would otherwise look like a mistake. A comment that only restates what the code says does not earn its place.

## Where an Article Goes

- **An article about the template** goes under the root's [`docs/`](../README.md), in the section it belongs to, and is listed in [`docs/README.md`](../README.md), in its section's `README.md`, and in the root [`README.md`](../../README.md).
- **An article for the generated project** goes under `template/docs/`, and is listed in the generated project's documentation index and its section index (see [authoring](../project-template/authoring.md#adding-a-file-to-the-body)).

## Related

- [Markdown style](markdown-style.md) — the rules for the articles themselves.
- [Line length](line-length.md) — how far a comment is filled.
