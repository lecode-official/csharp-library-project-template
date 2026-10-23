# Line Length

This article covers the 150-character line limit: where it is enforced, where it does not apply, and why it is also a *lower* limit for everything a formatter cannot rewrap.

## 150 Characters, in Every Language

No line of code exceeds 150 characters. The limit lives in [`dprint.json`](../../../dprint.json) as `lineWidth`, and dprint applies it to every language it formats — C#, XML (including `.csproj`, `.props`, and `.slnx`), JSON, YAML, and TOML. The limit applies just as much to the languages dprint does not format, where nothing enforces it automatically.

This is a hard limit, not a target. There are exactly two exceptions:

- **Markdown is exempt.** dprint's `textWrap` is `never` and MarkdownLint's line-length rule is off, so prose is never hard-wrapped — see [Markdown style](markdown-style.md) and [MarkdownLint](../tooling/linting-markdownlint.md). Do not manually wrap a Markdown line, whatever its length.
- **A line that genuinely cannot be broken.** A URL, a base64 blob, a long single string literal, a command in a task definition. Configuration files collect most of these, which is why they are the usual place to find an overlong line. dprint itself sometimes cannot break a line to fit, as the comment in `dprint.json` says. Leave those alone rather than mangling them. An unbreakable line is an exception, never a license to stop caring about the rest.

## It Is Also a Lower Limit

dprint reflows code, but it never reflows the inside of a comment or a string. Those are the author's job, and the rule is symmetrical:

**A comment, an XML documentation comment, or a string literal split over several lines is filled to the limit. Break only when the next word would not fit.**

So a documentation comment line that stops at column 100 while the next word would have fit at column 120 is wrong, and so is a string constant whose pieces are split short of the limit. This matters because the alternative is invisible drift: every author wraps at a slightly different width, and every later edit re-wraps the paragraph differently, so a one-word change shows up as a five-line diff.

The same applies to the `//` comments, to the `<!-- -->` comments in the MSBuild files, to the comments in the JSONC configuration files and in `.globalconfig`, and to the `#` comments and docstrings of the Python scripts.

## Two Things That Are Never Reflowed

- **Preformatted lines.** An indented block inside a comment — a usage example, a command, a sample payload — keeps its own line breaks. Indentation is the signal.
- **List items and tag paragraphs.** A `-` item in a comment, and each `<param>`/`<returns>`/`<exception>` tag of an XML documentation comment, starts its own paragraph and is filled independently. A continuation line of a list item is indented under the item's text.

## Splitting a String Literal

When a string is split across lines, each piece is a literal of its own joined with `+`, and **the space between two words stays at the end of the preceding piece**:

```csharp
private const string Description = "Composes a greeting for the given name. The salutation the greeter was constructed with is used for every " +
    "greeting it produces.";
```

Never `" ...for every"` plus `" greeting..."`: a leading space on the continuation reads as an indentation mistake, and the two forms mixed in one file make it impossible to see at a glance where the space actually is. Continuation pieces are indented one level from the line that opens the statement.

## Related

- [Formatting (dprint)](../tooling/formatting-dprint.md) — the formatter that owns everything else about layout.
- [Comments and documentation comments](comments-and-documentation.md) — what goes inside those blocks.
- [Markdown style](markdown-style.md) — the exempt case.
- [C# style](csharp-style.md) — the rest of the conventions the formatter does not own.
