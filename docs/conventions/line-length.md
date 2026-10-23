# Line Length

This article covers the 150-character line limit on both sides of the split, and what a placeholder does to a line's width.

## 150 Characters, Everywhere

No line exceeds 150 characters, at the root or in the body. The root's [`dprint.json`](../../dprint.json) sets `lineWidth` to 150 for the files it formats: the JSON, YAML and TOML at the root.

The limit applies just as much where no formatter enforces it. Nothing formats the shell commands in the Claude Code hooks, so keeping those within the limit is the author's job.

There are exactly two exceptions:

- **Markdown is exempt.** Prose is never hard-wrapped, at the root or in the body.
- **A line that genuinely cannot be broken**, such as a URL, a long string literal, or a hook command in `.claude/settings.json`.

## It Is Also a Lower Limit

A formatter reflows code, but never the inside of a comment or a string. So a comment or a split string literal is filled to the limit, and broken only where the next word would not fit. That applies to the comments in [`copier.yml`](../../copier.yml), and in the JSONC configuration files, exactly as it does to the generated project's code.

The reason is the same as in the generated project: when everyone wraps at a slightly different width, every later edit re-wraps the paragraph, and a one-word change shows up as a five-line diff.

## A Placeholder Changes the Width

A line in the body is measured twice: once as it is written in the template, and once after rendering, when every placeholder has been replaced by an answer of unknown length. The two widths differ, and only the second one is what the generated project sees.

- **In code**, a line that grows past the limit after rendering breaks the limit in the generated project. Leave room on a line that carries a placeholder, so that a reasonably long answer still fits.
- **In a comment or a documentation comment**, nothing reflows the line and nothing reports it. A placeholder makes the fill rule impossible to satisfy for every answer, so keep placeholders out of filled comment paragraphs where you can. Where you cannot, end the line that carries the placeholder early enough that a long answer still stays within the limit.
- **In Markdown**, the width does not matter, because Markdown is exempt.

The only way to see the rendered width is to render (see [authoring](../project-template/authoring.md#verifying-a-change)), ideally with a long product name, which is the answer that appears in the most places.

## Related

- [Formatting (dprint)](../tooling/formatting-dprint.md) — what the root's formatter formats.
- [Comments and documentation](comments-and-documentation.md) — what goes inside the comments being filled.
- [Markdown style](markdown-style.md) — the exempt case.
