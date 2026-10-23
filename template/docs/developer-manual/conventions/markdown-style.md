# Markdown Style

This article covers the conventions for Markdown files (this documentation, `README.md`, and `AGENTS.md`).

Prose in Markdown is never hard-wrapped.

## Headings Are Title Case

Every heading — at every level, in every Markdown file — uses **title case**, not sentence case. Write `## Running the App`, not `## Running the app`.

The rules:

- Capitalize the first and last word, and every major word in between (nouns, verbs, adjectives, adverbs, pronouns, and subordinating conjunctions).
- Keep minor words lowercase unless they are first or last: articles (`a`, `an`, `the`), coordinating conjunctions (`and`, `but`, `or`, `nor`, `for`, `so`, `yet`), and short prepositions (`as`, `at`, `by`, `for`, `from`, `in`, `into`, `of`, `off`, `on`, `per`, `to`, `up`, `via`, `vs`, `with`).
- In a hyphenated compound, apply the same rules to each part: `Build-Time Configuration`, `Server-to-Client Rendering`.

## Preserve Exact Casing of Names and Code

Title case never overrides the real casing of a name. Leave these exactly as they are written:

- Code spans stay verbatim, including surrounding backticks: ``## The `bootstrap` Pattern``.
- Brand and tool names keep their own casing, including intentionally lowercase ones: `dprint`, `esbuild`, `npm`.
- Acronyms and proper technology names stay as-is: `API`, `ESM`, `DTO`, `JSDoc`, `HTML`, `CSS`, `TypeScript`, `Angular`, `macOS`, `i18n`.

When a name is intrinsically lowercase, it stays lowercase even as the first word: `## dprint Owns Formatting`.

## Code Spans for Identifiers, Paths, and File Names

Wrap every identifier, file name, path, command, and code snippet in backticks, in prose everywhere — the documentation, `README.md`, `AGENTS.md`, and commit messages. Write `` `Greeter` ``, `` `source/[[ library_slug ]]/Greeter.cs` ``, `` `dotnet build` ``, not Greeter, source/[[ library_slug ]]/Greeter.cs, dotnet build. This keeps code visually distinct from surrounding prose and matches how links to source files are already written.

XML documentation comments are the one exception: they are XML, not Markdown, so a backtick stays literal there and `<see cref="..."/>` or `<c>...</c>` is used instead (see [comments and documentation comments](comments-and-documentation.md)).

## Punctuation

- **Prefer a period over a semicolon.** Where a semicolon joins two full sentences, split them into two sentences with a period instead. This applies to all prose — the documentation, `README.md`, and `AGENTS.md`. In-code comments are the one exception and follow their own rule (see [C# style](csharp-style.md)).
- **Use em and en dashes sparingly.** They fit a genuine aside or an abrupt break, not as a default connector. When a comma, a period, or parentheses reads just as well, use that instead.

## No Horizontal Rules

Never use horizontal rules (`---`) to separate sections. Headings already provide the structure. A `---` at the top of a file is only ever front matter, never a divider.

## Related

- The other conventions: [C# style](csharp-style.md) and [file and naming conventions](file-and-naming-conventions.md).
- [Commit messages](commit-messages.md) — the same title-case and punctuation rules, applied to the Git history.
