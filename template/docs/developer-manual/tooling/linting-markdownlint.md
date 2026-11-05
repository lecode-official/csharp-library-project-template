# Markdown Linting (MarkdownLint)

This article covers Markdown linting.

Markdown — including this documentation, [`README.md`](../../../README.md), and [`AGENTS.md`](../../../AGENTS.md) — is linted by [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2), configured in [`.markdownlint.yml`](../../../.markdownlint.yml).

## Configuration

The configuration keeps the default rules and changes two things:

- **Line length is off.** Prose is never hard-wrapped, so do not manually wrap a Markdown line (see [line length](../conventions/line-length.md) and [Markdown style](../conventions/markdown-style.md)).
- **Three inline-HTML elements are allowed**: `kbd`, for keyboard shortcuts, `div`, which the `README.md` uses to center-align its badge row, and `img`, which it uses to align the logo with its title. Everything else is still reported, because inline HTML in Markdown should stay the exception.

## Running It

```shell
npm run lint:markdownlint
```

Under the hood that is:

```shell
npx markdownlint-cli2 "**/*.md" "!**/node_modules/**" "!**/build/**" "!**/.venv/**" "!**/coverage/**" "!**/coverage-report/**" "!**/TestResults/**"
```

`npx` resolves the exact version pinned in [`package.json`](../../../package.json) and locked in `package-lock.json`, the same version [continuous integration](continuous-integration.md) installs.

The exclusions matter: unlike dprint and CSpell, `markdownlint-cli2` does **not** ignore `node_modules` or build output by default, and it has no `--ignore` flag. Exclusions are expressed as negated globs instead — `!`-prefixed in the npm script, or `#`-prefixed when they are passed as bare arguments in a shell that would otherwise expand them. A run that suddenly takes minutes and reports thousands of findings is almost always a lost exclusion.

## Writing Docs That Pass

Keep to standard Markdown: one top-level heading per file, blank lines around headings, lists, and fenced code blocks, and a language on every code fence. Wrap element and tag names in backticks, so that `` `<summary>` `` is a code span rather than inline HTML the linter has to judge.

## Related

- [Markdown style](../conventions/markdown-style.md) — the stylistic conventions that go beyond linting.
- [Line length](../conventions/line-length.md) — why the line-length rule is off.
- [CSpell](spell-checking-cspell.md) — the other check that runs over these files.
- [Continuous integration](continuous-integration.md) — the pinned version used there.
