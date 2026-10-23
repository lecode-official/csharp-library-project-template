# Testing

This article covers the conventions for the unit tests in [`tests/unit-tests`](../../../tests/unit-tests/). For the tooling that runs them and measures code coverage, see [testing and code coverage](../tooling/testing-and-code-coverage.md).

## Every New Feature Is Unit Tested

A change that implements a new feature is not done until it has unit tests covering it, in the same pull request. This applies to human and AI-assisted contributions alike (see [contributing](../contribution-guide.md)). A bug fix also adds a test that reproduces the bug and would fail without the fix. Documentation-only changes, formatting, and pure refactors that do not change behavior are exempt — but a refactor that changes behavior along the way is not.

Not every line needs to be covered for its own sake. A placeholder implementation with no reachable failure path yet — a `catch` block nothing can currently throw into — does not need a contrived test written just to touch it. Test the behavior that exists, not the branches a future change will eventually make reachable.

## One Test Class per Source Type

Each type with behavior worth verifying gets one test class, named `<TypeName>Tests`, in the mirroring namespace and folder. `[[ root_namespace ]].Greeter` is tested by `[[ root_namespace ]].UnitTests.GreeterTests` in `tests/unit-tests/GreeterTests.cs`, and a type in a namespace folder is mirrored into the same folder under `tests/unit-tests/`. This mirrors how the library itself is organized (see [architecture](../architecture.md)), so a source file's tests are always easy to find.

## Internal Types Are Tested Directly

The library grants the test assembly access to its internals through `InternalsVisibleTo`. An `internal` type with behavior of its own is instantiated and exercised directly in its own test class, exactly as a `public` type is, rather than only indirectly through whatever public surface happens to wrap it. Internal visibility is part of the design surface this project documents, so it deserves the same direct coverage.

## Naming Test Methods

A test method name has three parts, run together as a single PascalCase identifier with no separator: the member under test, the scenario, and the expected outcome — `GreetNoNameGreetsTheWorld`, `ConstructorBlankSalutationThrows`.

No member name in this code base contains an underscore, test methods included (see [C# style](csharp-style.md)). A test explorer or a failure message shows the full name on its own line regardless, so a separator is not needed to keep the three parts readable.

An asynchronous test method does not end in `Async`, unlike every other asynchronous method (see [C# style](csharp-style.md)). It is named after the member under test, the scenario, and the outcome like every other test, and only the test runner ever calls it, so the suffix would add nothing. [`tests/unit-tests/.globalconfig`](../../../tests/unit-tests/.globalconfig) turns the IDE1006 naming rule for asynchronous methods off for the test project (see [static code analysis](../tooling/static-code-analysis.md)).

## No `ConfigureAwait` in Tests

Test code never calls `ConfigureAwait`. xUnit's own analyzer reports `ConfigureAwait(false)` in a test method (xUnit1030), so the test project's `.globalconfig` turns the Roslynator rule RCS1090, which requires `ConfigureAwait(false)` in the library, around to report any `ConfigureAwait` call instead (see [static code analysis](../tooling/static-code-analysis.md)).

## Every Member Is Documented, Including Private Ones

A test class, and every member on it — test methods, test doubles, and the members of those test doubles — carries an XML documentation comment, with no exception for `private` or for test code. The build checks all of it: the compiler reports a missing comment on a `public` member, because `GenerateDocumentationFile` is enabled on the test project, and StyleCop Analyzers reports a missing comment on every other member, `private` ones included (see [static code analysis](../tooling/static-code-analysis.md)). See [comments and documentation comments](comments-and-documentation.md) for what the summary is expected to say.

## Structure

- **Test classes and test doubles are `sealed`**, like every other class here by default.
- **Members are grouped into `#region` blocks**, typically just `#region Public Methods` for the test methods, plus `#region Private Classes` where a test class defines a small fake or stub (see [C# style](csharp-style.md)).
- **A test body follows Arrange-Act-Assert, separated by a blank line between each part.** No comment marks the three parts — the blank lines are enough, and a comment restating "arrange" would only restate what the code already says.
- **Prefer a real collaborator over a mock** whenever the real thing is cheap to construct. Write a small hand-rolled fake — a private nested class implementing the interface — only for a dependency that cannot otherwise be observed.
- **A test that touches genuinely process-global state saves the original value and restores it in a `finally` block**, so that one test's use of shared state cannot leak into another test or into the test runner's own exit code.
- **Use `[Theory]` with `[InlineData]`** where the same assertion holds for several inputs, rather than copying a test method per input.

## What a Test Covers

A test covers a type's observable behavior, not its implementation. It asserts on what a caller can rely on, and does not mention the private members that happen to implement it, so a refactor that preserves the behavior preserves the tests.

## Redirecting Logging to the Test Output

This applies once the library grows something that logs, which it does not today. If a test hands the code under test a logger that writes to the console — the console provider of `Microsoft.Extensions.Logging`, for example, which an application built on the generic host registers by default — a test that runs far enough for that code to log something prints it straight to the console and clutters the test output, whether the test passed or not.

The fix is an `ILogger`/`ILoggerProvider` pair that writes to xUnit's `ITestOutputHelper` instead, plus an unsealed test base class that takes an `ITestOutputHelper` through its constructor and hands each test a logger already wired to it. xUnit surfaces `ITestOutputHelper` output only for a failing test, or when run verbosely, so logging becomes available for diagnosis without printing unconditionally.

Note that xUnit's fixture mechanisms (`IClassFixture<T>`, `ICollectionFixture<T>`) are not suited to this: both create one shared instance reused across multiple tests, while `ITestOutputHelper` is a fresh instance per test method, so a fixture built before it exists could never wrap the right one. Plain constructor injection into a base class, which xUnit re-instantiates for every test method, is the correct mechanism.

## Keep the Suite Green

When a test run reveals failures, fix them immediately. Do not label them pre-existing or unrelated and move on — the suite must stay green at all times.

## Related

- [C# style](csharp-style.md) — the conventions the tests also follow.
- [Comments and documentation comments](comments-and-documentation.md) — what a test's documentation comment says.
- [Testing and code coverage](../tooling/testing-and-code-coverage.md) — running the tests and generating a coverage report.
- [Architecture](../architecture.md) — where the test project sits in the repository.
- [Contributing](../contribution-guide.md) — the pull request requirement this article's first section states.
