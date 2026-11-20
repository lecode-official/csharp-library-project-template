# Markdown Linting (MarkdownLint)

This article covers Markdown linting, at the root and in the template body.

## The Root's Configuration

The template's own Markdown, meaning the articles under [`docs/`](../README.md), [`README.md`](../../README.md), [`AGENTS.md`](../../AGENTS.md) and [`CHANGELOG.md`](../../CHANGELOG.md), is linted by [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2), configured in the root's [`.markdownlint.yml`](../../.markdownlint.yml). It keeps the default rules and changes two things:

- **Line length is off.** Prose is never hard-wrapped (see [line length](../conventions/line-length.md)).
- **Two inline-HTML elements are allowed**, `kbd` and `div`. Everything else is still reported.

## Running It

```shell
npm run lint:markdownlint
```

Under the hood that is:

```shell
npx markdownlint-cli2 "**/*.md" "!**/node_modules/**" "!template/**" "!licenses/**" "!**/.venv/**"
```

`markdownlint-cli2` has no `--ignore` flag and does not skip `node_modules` on its own, so every exclusion is a negated glob. `template/**` is excluded because the body's Markdown is checked by the body's own configuration, in a render. `.venv/` is excluded because a local Python virtual environment, for example one for the documentation website of a render, carries the Markdown files of every package installed into it. A run that suddenly takes minutes and reports thousands of findings has almost always lost an exclusion.

## The Body's Configuration

[`template/.markdownlint.yml`](../../template/.markdownlint.yml) is the generated project's configuration, and it is what checks the body's Markdown once rendered. The two configurations are separate on purpose: the root's governs articles that talk *about* placeholders, and the body's governs articles that *contain* them, which only become valid Markdown once the placeholders are gone.

The sharpest difference between the two is the table rule. A placeholder inside a Markdown table in the body produces a table that the generated project reports with `MD060`, so never put one there (see [Markdown style](../conventions/markdown-style.md#placeholders-in-body-markdown)).

## Link Checking

Both configurations also turn on `relative-links`, a rule that MarkdownLint does not have built in. It comes from the npm package [`markdownlint-rule-relative-links`](https://github.com/theoludwig/markdownlint-rule-relative-links), which [`.markdownlint-cli2.yaml`](../../.markdownlint-cli2.yaml) and its copy in the body load, and it reports:

- **A relative link to a file that does not exist**, such as a link to an article that was renamed or moved, or to a missing image.
- **A link to a heading of another file that does not exist**, as in `article.md#section`, which breaks when the heading is renamed. A link to a heading of the same file is checked by the built-in rule `MD051`.

External links are not checked, so that the linting stays fast, deterministic, and independent of the network. Links written as HTML, such as the `<img>` in the title of the generated read me, are not checked either. The rule checks a link against the files that exist, so the body's links are only checked in a render, where the placeholders in their paths are filled in.

## Writing Docs That Pass

Keep to standard Markdown: one top-level heading per file, blank lines around headings, lists and fenced code blocks, and a language on every code fence. Do not end a heading with `C#`, which MarkdownLint reads as a closed ATX heading and "fixes" into `C #`.

## Related

- [Markdown style](../conventions/markdown-style.md) — the conventions that go beyond linting.
- [CSpell](spell-checking-cspell.md) — the other check that runs over these files.
- [Markdown linting (MarkdownLint)](../../template/docs/developer-manual/tooling/linting-markdownlint.md) — the generated project's linter setup.
