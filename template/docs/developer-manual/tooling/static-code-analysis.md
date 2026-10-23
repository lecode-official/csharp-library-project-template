# Static Code Analysis

This article covers the Roslyn analyzers that check the C# code on every build, where their configuration lives, and how to deal with a finding.

## The Analyzers

Four sets of analyzers run in every project — the library, the sample app, and the unit tests:

- **The .NET SDK's own analyzers.** `<AnalysisLevel>latest-all</AnalysisLevel>` turns on every code quality rule (`CA*`) as a warning. It does not touch the code-style rules (`IDE*`), so `<AnalysisModeStyle>All</AnalysisModeStyle>` raises those to warnings as well, and `<EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>` runs them in the build, not only in the editor.
- **[StyleCop Analyzers](https://github.com/DotNetAnalyzers/StyleCopAnalyzers)** (`SA*`), which checks layout, ordering, naming, readability, and documentation comments.
- **[Roslynator](https://josefpihrt.github.io/docs/roslynator/)**, split into two packages: `Roslynator.Analyzers` (`RCS1*`), which simplifies and modernizes code, and `Roslynator.Formatting.Analyzers` (`RCS0*`), which checks where lines break and where blank lines go. All formatting rules are off by default, so each one that is used is enabled explicitly.
- **[Nullable.Extended](https://github.com/tom-englert/Nullable.Extended)** (`NX*`), which reports every use of the null-forgiving operator `!` that has no justification comment (see [C# style](../conventions/csharp-style.md#nullability-and-implicit-usings)).

The library also sets `<IsAotCompatible>true</IsAotCompatible>`, which adds the trim, AOT, and single-file analyzers (`IL2*`, `IL3*`). Code that a consumer could not trim or compile ahead of time is reported in the library, instead of in the consumer's application.

The analyzer packages are declared once, as `GlobalPackageReference` items in [`Directory.Packages.props`](../../../Directory.Packages.props), which adds them to every project as build-time-only dependencies, so they never become a dependency of the published package. They are pinned like every other dependency (see [dependency management](../conventions/dependency-management.md)). StyleCop Analyzers has only ever published modern C# support in prerelease versions, so it is the one dependency pinned to a `-beta` version.

The build settings themselves live in [`Directory.Build.props`](../../../Directory.Build.props) at the repository root, which every project imports. Besides the analysis settings above, it treats warnings as errors in Release builds, turns on the compiler's `strict` mode, and audits the transitive dependencies for known vulnerabilities as well (`NuGetAuditMode`). A Debug build shows the findings without stopping, and a Release build fails on any of them.

## Where the Configuration Lives

The severity of every rule, and every option an analyzer reads, lives in [`.globalconfig`](../../../.globalconfig) at the repository root. Every setting in it carries a comment that says what the rule enforces and, where the setting turns a rule off, why.

A `.globalconfig` is a *global analyzer configuration file*, not an EditorConfig file. It shares the EditorConfig syntax, but only the C# compiler reads it, which is why editors do not recognize it on their own:

- **The compiler finds it on its own.** It looks for a file named `.globalconfig` in the directory of every source file and in all of its parent directories, so the one file at the root covers every project, without any reference from a project file.
- **It applies to a whole project, not to a file glob.** It has no sections. A `[*.cs]` header is not an error, but everything below it is silently ignored.
- **It holds analyzer settings only.** Indentation, line endings, and the character set stay in [`.editorconfig`](../../../.editorconfig), which editors read. A key set in both files takes its value from `.editorconfig`, so the two never repeat a setting.

Two projects need settings of their own. Each has a `.globalconfig` in its own directory with `global_level = 101`, which outranks the root file's `global_level = 100`. Without different levels, two files setting the same key would cancel each other out, and the key would fall back to its default.

- **[`tests/unit-tests/.globalconfig`](../../../tests/unit-tests/.globalconfig)** reverses the Roslynator rule `RCS1090`, so that it reports `ConfigureAwait` calls instead of asking for them, because xUnit's own analyzer (`xUnit1030`) forbids `ConfigureAwait(false)` in test methods. It also exempts asynchronous test methods from the `Async` suffix, because a test method's name follows the [testing](../conventions/testing.md) naming scheme.
- **[`source/sample-app/.globalconfig`](../../../source/sample-app/.globalconfig)** reverses `RCS1090` as well, because an application owns its synchronization context.

## The Rule Set Follows the Conventions

The configuration encodes the [conventions](../conventions/README.md), so a rule is never turned off just because it is inconvenient. A rule is turned off when it contradicts a documented convention:

- **`#region` blocks.** `SA1124` would forbid them.
- **Member order.** StyleCop checks that constructors come before fields, constants before other fields, static members before instance members, and, within each group, private members before internal, protected, and public ones, which is the reverse of its default order (`stylecop.ordering.accessibilityOrder`, checked by `SA1202`). Properties and methods are left unordered, because an interface implementation region may put a property after the methods.
- **Braces.** A body that fits on a single line has no braces, and a body that spans several lines must have them. `SA1503` and `csharp_prefer_braces` are turned off, and `RCS1001` to `RCS1004` enforce the rule both ways. An empty block may stay on one line, as in `protected void OnRunning() { }`.
- **Explicit types.** `IDE0008` reports `var`, and `RCS1250` asks for a target-typed `new()` instead.
- **`this.` qualification.** `SA1101` enforces it in the build. The `dotnet_style_qualification_*` options keep the editor from suggesting the opposite.
- **Primary constructors.** They are not used, because their parameters cannot carry XML documentation comments of their own.
- **Private members are documented.** StyleCop checks private members and private fields too, not just the public surface.

## One Problem, One Warning

The analyzer sets overlap, and with every rule enabled, many problems would be reported two or three times — a missing access modifier, for example, by `IDE0040`, `SA1400`, and `RCS1018` alike. When two rules report the same thing, the built-in rule is kept and the other one is turned off. The built-in rules come with the SDK and with code fixes in every editor. `.globalconfig` names each turned-off twin next to the rule that replaces it.

The one exception is `ConfigureAwait`: `RCS1090` is kept and `CA2007` is turned off, because only `RCS1090` can be reversed for the projects that must not call `ConfigureAwait` at all.

## The Analyzers Check, dprint Formats

Formatting stays with [dprint](formatting-dprint.md). `IDE0055`, which reports formatting that deviates from the formatting options, is turned off for that reason. The Roslynator formatting rules do not contradict dprint: dprint's Roslyn plugin decides whitespace and indentation, but it never moves a line break or adds a blank line, which is all those rules check. Where an analyzer and dprint disagree, the analyzer rule is wrong and is turned off, never the formatter.

## Dealing with a Finding

- **Fix the code.** Most findings come with a code fix in the editor, behind the light bulb.
- **Suppress a single finding** only when the rule is right in general and wrong in this one place. Use `[SuppressMessage]` with a `Justification`, or a `#pragma warning disable`/`restore` pair around the smallest possible span, with a comment that explains why.
- **Change `.globalconfig`** when the rule is wrong for the whole project, and give the setting a comment that says why. A project-specific exception goes into that project's own `.globalconfig` instead.

## Related

- [C# style](../conventions/csharp-style.md) — the conventions the rules encode.
- [Testing](../conventions/testing.md) — the test naming scheme behind the test project's exceptions.
- [Dependency management](../conventions/dependency-management.md) — how the analyzer packages are pinned.
- [Architecture](../architecture.md) — the `Directory.Build.props` and `Directory.Packages.props` files.
- [Formatting (dprint)](formatting-dprint.md) — the formatter the analyzers leave formatting to.
