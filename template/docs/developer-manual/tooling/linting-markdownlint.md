# Markdown Linting (MarkdownLint)

This article covers Markdown linting.

Markdown — including this documentation, [`README.md`](../../../README.md), and [`AGENTS.md`](../../../AGENTS.md) — is linted by [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2), configured in [`.markdownlint.yml`](../../../.markdownlint.yml).

## Configuration

The configuration keeps the default rules and changes two things:

- **Line length is off.** Prose is never hard-wrapped, so do not manually wrap a Markdown line (see [line length](../conventions/line-length.md) and [Markdown style](../conventions/markdown-style.md)).
- **Three inline-HTML elements are allowed**: `kbd`, for keyboard shortcuts, `div`, which the `README.md` uses to center-align its badge row, and `img`, which it uses to align the logo with its title. Everything else is still reported, because inline HTML in Markdown should stay the exception.

## The Pull Request Template

A pull request description is prose without a heading, and so is the [pull request template](../../../.github/pull_request_template.md) it starts from. [`.github/.markdownlint.yml`](../../../.github/.markdownlint.yml) extends the configuration at the root and turns `first-line-heading` off for that directory. Every other rule still applies there.

## Link Checking

The configuration also turns on `relative-links`, a rule that MarkdownLint does not have built in. It comes from the npm package [`markdownlint-rule-relative-links`](https://github.com/theoludwig/markdownlint-rule-relative-links), which [`.markdownlint-cli2.yaml`](../../../.markdownlint-cli2.yaml) loads, and it reports:

- **A relative link to a file that does not exist**, such as a link to an article that was renamed or moved, or to a missing image.
- **A link to a heading of another file that does not exist**, as in `article.md#section`, which breaks when the heading is renamed. A link to a heading of the same file is checked by the built-in rule `MD051`.

External links are not checked, so that the linting stays fast, deterministic, and independent of the network. Links written as HTML, such as the `<img>` in the title of the `README.md`, are not checked either. The build of the [documentation website](documentation-website.md) checks the links between its pages, too, but only under `docs/`, while the rule covers every Markdown file of the repository.

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
