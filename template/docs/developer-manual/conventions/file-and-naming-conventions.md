# File and Naming Conventions

This article covers how files and directories are named throughout the repository.

## Kebab-Case by Default

Files and directories are named in **kebab-case** — lowercase words separated by hyphens — for example `developer-manual`, `user-manual`, `getting-started.md`. This applies repository-wide: the [`docs/`](../README.md) tree, and every Markdown article.

## Well-Known Exceptions

Files with a conventional, tool- or ecosystem-mandated name keep that name instead of being renamed to kebab-case. This covers two kinds of file:

- **Files everyone recognizes by their standard name**: `README.md`, `AGENTS.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTORS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- **Files whose name is dictated by the tool that reads them**: `.editorconfig`, `.gitignore`, `.gitattributes`. Renaming these would simply stop the tool from finding them.

## Related

- [Architecture](../architecture.md) — where these directories and projects sit in the repository.
