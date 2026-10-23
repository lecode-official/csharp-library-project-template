# C# Style

This article covers the conventions for the C# code in [`source/`](../../../source/). It is about style and structure on top of the language itself — for the repository layout the code lives in, see [architecture](../architecture.md).

## File Layout

Every file declares a file-scoped namespace (`namespace [[ root_namespace ]];`), not a namespace block. Beyond the usings that `ImplicitUsings` already brings in, additional `using` directives are wrapped in a `#region Using Directives` block at the top of the file, above the namespace declaration. Without such directives, the namespace declaration is the first line.

Every type groups its members into `#region` blocks, regardless of file size — even a type with a single constructor and a single property uses regions. There is no size threshold below which regions are skipped.

Regions appear in this order: constructors, then constants, then fields, then properties, then methods, then interface implementations. Within the constants/fields/properties/methods categories, group first by kind (for example static methods before instance methods) and, within a kind, order by access modifier: `private` before `internal` before `protected` before `public` — so `#region Private Fields` precedes `#region Public Fields` when both exist. Typical region names are `#region Constructors`, `#region Private Fields`, `#region Public Constants` (for `const` members, kept separate from `#region Public Fields`), `#region Public Properties`, `#region Public Static Methods`, `#region Public Methods`, and `#region Protected Methods`. A region for the members that implement a specific interface, inside the *implementing* type, is named `#region <InterfaceName> Implementation` with **no** access modifier in the name (it is always `#region IHost Implementation`, never `#region Public IHost Implementation`), because an implementing member's accessibility is dictated by the interface, not chosen per member.

Inside an interface declaration itself, access modifiers are meaningful and follow the same rules as a class: an abstract member (one without a body) is implicitly, and must be declared, `public`. A member with a default implementation, however, may instead be declared `protected` or `private`, letting a default `public` method delegate a piece of its behavior to a `protected` method that implementers can override without replacing the whole implementation, or to a `private` helper that only other default implementations in the interface can call. Because the modifier carries real information here, interface regions are named the same way class regions are — `#region Public Methods`, `#region Protected Methods` — instead of dropping the modifier:

```csharp
public interface ITest
{
    #region Public Properties

    public string Name { get; }

    #endregion

    #region Public Methods

    public void Run() => this.OnRunning();

    #endregion

    #region Protected Methods

    protected void OnRunning() { }

    #endregion
}
```

## Documentation Comments

Every member has an XML documentation comment — public and internal ones because `GenerateDocumentationFile` is enabled in the project files, so those ship in the compiled output and reach a consumer's editor tooltips, but `private` members are documented exactly the same way, for the same reason every other convention on this page exists: someone reading the source, not just the compiled output, needs it. A `<summary>` explains not just what a member does, but why it exists and how it relates to the rest of the design — the reasoning belongs next to the code, not only in a commit message. Parameters and return values are documented with `<param>` and `<returns>`. When a member implements an interface member or overrides a base member and has nothing to add beyond what is already documented there, use `<inheritdoc/>` instead of repeating the text. The C# compiler never expands `<inheritdoc/>` into real text in the generated XML documentation file — it is left in verbatim — so the library's `.csproj` references [SauceControl.InheritDoc](https://github.com/saucecontrol/InheritDoc), which rewrites every `<inheritdoc/>` with the real, inherited text as a build step. Without it, a consumer's editor tooltip would show nothing for these members.

Prose inside documentation comments follows the same punctuation rule as the rest of the documentation: periods, not semicolons (see [Markdown style](markdown-style.md)).

A `<returns>` element always starts with "Returns", for example `<returns>Returns the exit code produced by the executed command.</returns>`.

C# keywords mentioned in documentation-comment prose — `null`, `true`, `false`, `default`, `sealed`, `internal`, and so on — are marked up with `<see langword="..."/>` rather than written as plain text or in a code span, for example `<see langword="null"/>` or `<see langword="sealed"/>`.

A documentation comment is XML, not Markdown, so backticks stay literal instead of rendering as a code span (see [code spans](markdown-style.md#code-spans-for-identifiers-paths-and-file-names) for the general rule). Reference a type or member with `<see cref="..."/>` (for example `<see cref="Greeter"/>`) so that it becomes a clickable link in IDE tooltips, and wrap anything else that is code — a file name, a literal value, a short snippet — in `<c>...</c>`.

## Plain Comments

A plain `//` comment inside a method body is not prose — it explains a non-obvious *why* (a hidden constraint, an ordering requirement, a workaround) that the code next to it does not already make clear. It follows the opposite punctuation rule from documentation comments and the rest of the documentation: sentences are separated by semicolons, and the last one takes no terminal punctuation.

```csharp
// The fallback is only registered if the consumer did not register one of their own, so that the type stays usable out of the box while still
// letting a caller replace the behavior entirely simply by registering their own implementation
```

Do not write a comment that only restates what the code already says. If removing it would not confuse a future reader, it should not be there.

## Members and Types

The rules that hold for every member, before the C#-specific ones below:

- **Every member declares its scope explicitly.** Write `private`, `protected`, `internal`, or `public`, even where it is the language default.
- **Every method declares its return type explicitly**, including `void`.
- **Keep explicit type annotations even where the type could be inferred.** An annotation is documentation, and it is the part a reader gets for free — so prefer `string[] arguments = [...]` over `var arguments = [...]`.
- **Model an absent value explicitly.** A nullable type means `null` is a real, handled case, not an oversight.
- **Type arguments are never broken across lines**, in any context — an implements or extends clause, an annotation, a constructor call, a method call.
- **A file declares exactly one top-level type.** A type that only supports another one still gets a file of its own, or becomes a nested type of the type it supports.

And the C#-specific ones:

- **Classes are `sealed` by default.** A type is only left unsealed when it is deliberately designed as a base class for extension. Where a type needs to reuse behavior from a sealed framework type it cannot inherit from (for example, a concrete host or builder from `Microsoft.Extensions.Hosting`), it wraps that type and forwards to it (composition) instead.
- **Prefer expression-bodied members** (`=>`) for members whose implementation is a single expression, including constructors, property getters, and simple methods.
- **Access instance members through `this.`** explicitly, even in a constructor or method where the name would resolve unambiguously without it.
- **Async methods are suffixed `Async`** and return `Task` or `Task<T>`. They accept a `CancellationToken` (typically the last parameter) whenever the work they do can meaningfully be canceled.
- **Prefer factory methods over public constructors** when a type has invariants to establish or work to do beyond simple field assignment. An `internal` constructor paired with a `public static` creation method (or a dedicated builder type) keeps construction explicit and controllable.
- **Interfaces are prefixed with `I`** (`IDisposable`), following the standard .NET convention.
- **Interface members declare their access modifier explicitly** (`public string Name { get; }`), even where it is `public`, the default for an interface member, matching the explicit style used elsewhere in this codebase (`this.`, `sealed`). A member with a default implementation may also be `protected` or `private` (see [file layout](#file-layout)).
- **Private fields are `camelCase`** with no leading underscore and no `_` prefix.

## Idioms the Analyzers Enforce

A few smaller idioms are checked by the analyzers configured in [`.globalconfig`](../../../.globalconfig) (see [static code analysis](../tooling/static-code-analysis.md)):

- **Every `await` in the library uses `ConfigureAwait(false)`** (`RCS1090`), because a library does not know the synchronization context of the code that calls it. The sample app and the test project turn the rule around in their own `.globalconfig`, so there a `ConfigureAwait` call is reported instead: an application owns its synchronization context, and xUnit reports `ConfigureAwait(false)` in a test method itself (`xUnit1030`).
- **Null checks use pattern matching**, `value is null` and `value is not null`, never `==` or `!=` (`RCS1248`).
- **An empty string is written as `string.Empty`**, never `""` (`RCS1078`).
- **Argument lists, array initializers, and collection initializers have no trailing comma** (`RCS1260`).
- **Arguments are validated with throw helpers** such as `ArgumentNullException.ThrowIfNull` and its siblings, not with an `if` statement that throws (`RCS1255`).
- **Primary constructors are not used**, because their parameters cannot carry XML documentation comments of their own. The code-style option behind `IDE0290` is turned off, so the analyzers never suggest one.

## Nullability and Implicit Usings

Every project enables `<Nullable>enable</Nullable>` and `<ImplicitUsings>enable</ImplicitUsings>` (see [architecture](../architecture.md)). Write code that is genuinely null-safe rather than silencing the analyzer with `!`. A nullable parameter or return type should mean that `null` is a real, handled case.

Where the null-forgiving operator `!` is genuinely needed, because the compiler cannot see a guarantee that the code relies on, it carries a justification comment: a plain comment that starts with `// !`, followed by a space, and says why the value cannot be `null`. It goes on the line above the statement, or, for a declaration, between the documentation comment and the declaration — above the documentation comment, StyleCop reports it (`SA1514`). A `!` without one fails the build (see [static code analysis](../tooling/static-code-analysis.md)).

```csharp
/// <summary>
/// Gets the name of the greeter.
/// </summary>
// ! Every caller sets the name through the object initializer, which the required modifier cannot express here
public string Name { get; init; } = null!;
```

## Formatting

C# **is** formatted by [dprint](../tooling/formatting-dprint.md), through the Roslyn plugin configured in [`dprint.json`](../../../dprint.json). The plugin drives whitespace, newlines, and indentation only — it has no equivalent of the `csharp_style_*` or `dotnet_*` analyzer preferences. `.csproj` and `.slnx` files are formatted too, as XML, through an explicit association in the same configuration.

Indentation and basic whitespace also come from [`.editorconfig`](../../../.editorconfig) (4 spaces and no tabs, in `.csproj` and `.slnx` files too, LF line endings, and the 150-character maximum line length), which most editors, including Visual Studio Code, apply automatically.

## Enforcement

Most of the rules on this page are checked on every build by the analyzers configured in [`.globalconfig`](../../../.globalconfig): explicit types, explicit access modifiers, `this.` qualification, file-scoped namespaces, expression bodies, braces, one type per file, the documentation comments, and many more (see [static code analysis](../tooling/static-code-analysis.md)). A Release build fails on any finding. The member order is checked in part: constructors before fields, constants before other fields, static before instance members, and private before internal before protected before public. What no analyzer can check — the order of properties and methods, the names of the `#region` blocks, sealing by default, the wording of a summary — remains a review-time convention.

## Related

- [Comments and documentation comments](comments-and-documentation.md) — the required wording for every documentation comment.
- [Architecture](../architecture.md) — where these files live in the repository.
- [File and naming conventions](file-and-naming-conventions.md) — what the files and directories around them are called.
- [Line length](line-length.md) — the 150-character limit, which is also a lower limit for comments.
- [Markdown style](markdown-style.md) — the punctuation rule for prose versus plain comments governs both.
- [Formatting (dprint)](../tooling/formatting-dprint.md) — the formatter and its Roslyn plugin.
- [Static code analysis](../tooling/static-code-analysis.md) — the analyzers that enforce most of these rules.
- [Testing](testing.md) — how these rules apply to the test project.
