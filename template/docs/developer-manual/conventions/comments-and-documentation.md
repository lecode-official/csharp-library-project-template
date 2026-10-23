# Comments and Documentation Comments

This article covers the documentation-comment requirement and its fixed wording patterns, and the separate rule that plain comments follow.

## Every Member Gets a Documentation Comment

Every type and every member has an XML documentation comment — **including `private` ones**. Public and internal members need it because `GenerateDocumentationFile` is enabled, so those comments ship alongside the compiled assembly and reach a consumer's editor tooltips. Private members are documented for the same reason every other convention here exists: someone reading the source, not just consuming the package, needs it.

The wording is consistent, so that a reader can predict the first three words of any comment:

- Classes, interfaces, structs, records: `Represents a ...`
- Fields and constants: `Contains ...`
- Boolean fields, constants, and properties: `Contains a value that determines whether ...`
- Methods: a third-person verb — `Opens ...`, `Creates ...`, `Updates ...`
- Property getters: `Gets ...`
- Property setters, and get-set pairs: `Gets or sets ...`
- Enumerations: `Represents an enumeration for the different kinds of ...`

A `<summary>` explains not just what a member does, but **why it exists and how it relates to the rest of the design**. The reasoning belongs next to the code, not only in a commit message.

## The Tags

- `<param>` and `<returns>` document parameters and return values. A `<returns>` element always starts with "Returns", as in `<returns>Returns the exit code the command produced.</returns>`.
- `<exception>` documents every exception the member throws deliberately.
- `<inheritdoc/>` is used where a member implements an interface member or overrides a base member and has nothing to add. The compiler never expands it into the generated XML documentation file — it is left in verbatim — which is why the library references `SauceControl.InheritDoc` to rewrite it with the real inherited text at build time. Without that, both a consumer's tooltip and the generated API reference show nothing for those members (see [documentation website](../tooling/documentation-website.md)).

## Markup Inside a Documentation Comment

A documentation comment is XML, not Markdown, so backticks stay literal instead of rendering as a code span:

- `<see cref="..."/>` references a type or member, so that it becomes a clickable link in an editor tooltip and in the generated API reference.
- `<see langword="..."/>` marks up a C# keyword mentioned in prose — `null`, `true`, `false`, `default`, `sealed`, `internal`, and so on — rather than writing it as plain text.
- `<c>...</c>` wraps anything else that is code: a file name, a literal value, a short snippet.

## Placement and Formatting

- Only on types and their members. Never inside a method body — no documentation comment on a local variable or a local function.
- Always leave one empty line before the comment, outside it.
- No blank lines inside the comment.

## Punctuation

Documentation comments are prose, and follow the [prose punctuation](markdown-style.md) rule: separate sentences with a period, never a semicolon, and end each sentence with a period.

Plain `//` comments do the reverse. Sentences are separated by a semicolon, and the last one takes no terminal punctuation at all:

```csharp
// The fallback is only registered if the consumer did not register one of their own, so that the type stays usable out of the box while still
// letting a caller replace the behavior entirely by registering their own implementation
```

A single-sentence comment simply takes no terminal punctuation. A plain comment sits on its own line above the code it describes, never at the end of that line.

## Explain Why, Not What

A plain comment inside a method body is not prose — it explains a non-obvious *why*: a hidden constraint, an ordering requirement, a workaround. The comments that earn their place document exactly that, and they should be preserved rather than tidied away.

Do not write a comment that only restates what the code already says. If removing it would not confuse a future reader, it should not be there.

## The Test Project Is Not Exempt

Every test class and every test method carries a documentation comment too, and `GenerateDocumentationFile` is enabled on the test project so that a missing one on a `public` member fails the build — which reaches every test, since xUnit requires them to be public.

A test method's name already states its scenario and expected outcome in short form, so its `<summary>` does not repeat that. It explains **why the scenario matters and what the assertion is protecting against**, for the benefit of someone who has not memorized the naming convention. See [testing](testing.md).

## Related

- [C# style](csharp-style.md) — the surrounding style rules, including where regions go.
- [Line length](line-length.md) — how far a comment is filled before it is broken.
- [Markdown style](markdown-style.md) — the prose punctuation rule these comments share.
- [Testing](testing.md) — the test project's own documentation requirement.
- [Documentation website](../tooling/documentation-website.md) — how these comments become the published API reference.
