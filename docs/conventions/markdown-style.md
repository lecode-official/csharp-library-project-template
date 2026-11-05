# Markdown Style

This article covers the conventions for Markdown in this repository: the articles under [`docs/`](../README.md), [`README.md`](../../README.md), [`AGENTS.md`](../../AGENTS.md) and [`CHANGELOG.md`](../../CHANGELOG.md) at the root, and every Markdown file in the template body. Linting itself is handled by [MarkdownLint](../tooling/linting-markdownlint.md). This is about the conventions on top.

## The Same Rules on Both Sides

The root's Markdown follows the same conventions as the generated project's [Markdown style](../../template/docs/developer-manual/conventions/markdown-style.md), and the body's Markdown follows them because it becomes that project's documentation. In short:

- **Headings are title case**, at every level, in every file. Capitalize the first and last word and every major word. Keep articles, coordinating conjunctions and short prepositions lowercase unless they are first or last. Apply the same to each part of a hyphenated compound: `Two-Level Layout`.
- **Title case never overrides a name's real casing.** Code spans stay verbatim, tool names keep their own casing even as the first word (`## dprint Owns Formatting`), and acronyms stay as they are.
- **Identifiers, file names, paths, commands and code go in backticks**, in prose everywhere: `copier.yml`, `template/LICENSE`, `copier copy`.
- **Prose uses periods, not semicolons**, and em and en dashes sparingly.
- **No horizontal rules.** Headings provide the structure.
- **No comments.** A Markdown file is meant to read well without a renderer, and an HTML comment is clutter in the source and invisible once rendered. An explanation belongs in the prose, or in the article about the thing it explains. Inline HTML in general is limited to the few elements the linter allows.
- **Prose is never hard-wrapped.** Markdown is exempt from the [line length](line-length.md) limit on both sides.

One thing to watch: a heading that ends in `C#` reads to MarkdownLint as a closed ATX heading, which it reports, and which its `--fix` mode would "repair" into `C #`. Word such a heading so that it does not end in the `#`.

## Placeholders in Body Markdown

A Markdown file in the body is a template, and a placeholder in it is substituted before the generated project's linters ever see it. That makes a few constructs unsafe:

- **Never put a placeholder inside a table.** dprint pads every cell to align a table's pipes, and it does so at the template's widths. Substitution then changes those widths, so the rendered table is misaligned and the generated project's own MarkdownLint reports `MD060`, in a file nobody touched. Use prose, a list, or a fenced code block instead, none of which is aligned. Tables at the root are fine, since they are never rendered.
- **Never put a placeholder that may contain spaces in a link target.** `[[ product_name ]]` may contain spaces, and a raw space ends a Markdown link target. Link to the containing directory instead, and name the file in the link text, as in ``[`source/[[ product_name ]].slnx`](source/)``.
- **A placeholder in a heading is fine** when the answer is a name, such as `# [[ product_name ]] Documentation`, because a name keeps its own casing under title case anyway.
- **A placeholder in a code span is fine**, and is the usual way a body article shows a generated path or command.
- **Never write a placeholder directly inside the brackets of a link or image label.** In `[[[ maintainer_name ]]]`, the template engine reads the first two brackets as the opening delimiter and the third one as the start of a list, so the answer renders as a Python list, `['Jane Doe']`. Build the label inside the expression instead, as in `[[ '[' ~ maintainer_name ~ ']' ]]([[ maintainer_url ]])`. The same goes for any other `[[[` in the body, including a regular expression in a script.

The rendered Markdown is linted with the generated project's configuration, not this repository's, so check it in a render (see [authoring](../project-template/authoring.md#verifying-a-change)).

## Where Root Articles Differ

The root's articles are about the template, so they talk about placeholders constantly. They write them in code spans, `` `[[ product_name ]]` ``, so that they read as literal text. Root articles also link into the body freely, with relative paths such as `../../template/docs/README.md`. The reverse is never allowed (see [comments and documentation](comments-and-documentation.md#two-audiences)).

Each root article is small and covers a single topic, opens with a one-sentence "This article covers ..." line, and ends with a `## Related` section that links to its neighbors. That is the same shape the generated project's articles have.

## Related

- [MarkdownLint](../tooling/linting-markdownlint.md) — the linter, and the two configurations it runs with.
- [Comments and documentation](comments-and-documentation.md) — which side an article belongs on, and where it is listed.
- [Line length](line-length.md) — the exempt case.
- [Authoring](../project-template/authoring.md) — the table problem in context.
- [Markdown style](../../template/docs/developer-manual/conventions/markdown-style.md) — the generated project's full rule set.
