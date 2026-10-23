# C# Style

This article covers how the C# files added to the template body are styled. The root of this repository holds no C# at all: every `.cs`, `.csproj` and `.slnx` file lives under [`template/source/`](../../template/source/) or [`template/tests/`](../../template/tests/), and becomes the generated project's code.

## The Generated Project's Rules Apply Unchanged

A C# file in the body follows the generated project's [C# style](../../template/docs/developer-manual/conventions/csharp-style.md) exactly, with no exception for being a template:

- A file-scoped namespace, with additional `using` directives in a `#region Using Directives` block above it.
- `#region` blocks on every type, whatever its size, in the documented order: constructors, constants, fields, properties, methods, then interface implementations.
- An XML documentation comment on every member, including `private` ones (see [comments and documentation](comments-and-documentation.md)).
- Explicit access modifiers, explicit return types, and explicit type annotations instead of `var`.
- `sealed` classes by default, explicit `this.` on member access, expression-bodied members where the implementation is a single expression, and `camelCase` private fields without an underscore.
- Nullable reference types honored rather than silenced with `!`.

The reason is that the body's C# is the only C# a generated project starts with. `Greeter.cs`, in the library's directory under [`template/source/`](../../template/source/), says so in its own summary: it is there to be replaced, and its shape is the pattern to follow. A file in the body that departs from the conventions is therefore not a local blemish. It is the example every generated project copies.

## Placeholders in C# Code

Only a few answers are safe inside C# code, because a placeholder is substituted textually and the result has to compile for every answer a consumer might give:

- **`[[ root_namespace ]]` is the one placeholder that becomes an identifier.** It appears in namespace declarations and `using` directives, and the sample app's and the unit tests' namespaces derive from it as `[[ root_namespace ]].SampleApp` and `[[ root_namespace ]].UnitTests`. Its `help` string asks for PascalCase without spaces, which is what makes it a valid identifier.
- **`[[ product_name ]]` never becomes an identifier.** It may contain spaces and dots. It is fine inside a string literal, as the sample app's `Greet("[[ product_name ]]")` shows, and in project and assembly names, which are allowed to contain spaces.
- **Anything else stays out of code.** If a C# file seems to need another answer, it usually belongs in the project file instead, where the answers already feed `AssemblyTitle`, `Product`, `PackageId` and the rest (see [questions](../project-template/questions.md)).

A placeholder inside a documentation comment changes that line's rendered width, which the [line length](line-length.md) article deals with.

## Ship Placeholders, Not Features

The C# in the body exists so that a freshly generated project builds, tests, packs and documents itself on day one. It is deliberately minimal: the library is a single placeholder class, the sample app calls it, and the test project tests it.

Anything added to it has to be something every generated library wants, because every consumer either keeps it or deletes it. A type that only some libraries need is a type most consumers delete by hand after every render, and a type they keep is one the template now has to maintain for them through `copier update`.

## Nothing Compiles a Body File in Place

A C# file in the body is not valid C# until it is rendered: `namespace [[ root_namespace ]];` does not parse. The root's [dprint configuration](../tooling/formatting-dprint.md) excludes `template/` for that reason, and the root's [Claude Code hooks](../tooling/claude-code-hooks.md) skip it too. Your editor's C# extension will report diagnostics against these files that mean nothing.

So compiling happens in a render:

1. Render a project, as described in [authoring](../project-template/authoring.md#verifying-a-change).
2. Run `dotnet build` in the rendered project.
3. Port any fix back into the template file by hand.

## Related

- [C# style](../../template/docs/developer-manual/conventions/csharp-style.md) — the full rule set of the generated project.
- [Comments and documentation](comments-and-documentation.md) — the documentation-comment wording and placement rules.
- [Line length](line-length.md) — what a placeholder does to a line's width.
- [File and naming conventions](file-and-naming-conventions.md) — placeholders in the file names around the code.
- [Testing](testing.md) — the test that goes with every type in the body.
