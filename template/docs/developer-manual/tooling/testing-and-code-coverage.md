# Testing and Code Coverage

This article covers how to run the unit tests in [`tests/unit-tests`](../../../tests/unit-tests/) and how code coverage is measured. For the conventions the tests themselves follow, see [testing](../conventions/testing.md).

## The Test Project

[`[[ product_name ]] Unit Tests.csproj`](../../../tests/unit-tests/) is an [xUnit.net](https://xunit.net) v3 project that references the library through a project reference. Like the other projects it targets `[[ target_framework ]]` with `<Nullable>` and `<ImplicitUsings>` enabled, and sets `<RestorePackagesWithLockFile>`.

Three properties stand out:

- `<IsPackable>false</IsPackable>`, because the tests are never published.
- `<OutputType>Exe</OutputType>` together with `<UseMicrosoftTestingPlatformRunner>true</UseMicrosoftTestingPlatformRunner>`. An xUnit v3 test project is an executable of its own, which runs its tests on [Microsoft.Testing.Platform](https://learn.microsoft.com/dotnet/core/testing/microsoft-testing-platform-intro) rather than on the legacy VSTest runner. That is why it needs neither `Microsoft.NET.Test.Sdk` nor `xunit.runner.visualstudio`.
- `<GenerateDocumentationFile>true</GenerateDocumentationFile>`, which all three projects set, each for its own reason (see [architecture](../architecture.md#solution-and-projects)). Here it makes a missing documentation comment on a test class or test method fail the build. xUnit requires both to be `public`, so that check actually reaches them (see [testing](../conventions/testing.md) for what a test's documentation comment is expected to say).

It also declares a global `using` for `Xunit`, so test files carry no `using Xunit;` of their own.

## Running the Tests

[`global.json`](../../../global.json) switches `dotnet test` to Microsoft.Testing.Platform (`"test": { "runner": "Microsoft.Testing.Platform" }`). The .NET 10 SDK no longer runs a Microsoft.Testing.Platform project through VSTest, and in this mode `dotnet test` takes the solution or the project through `--solution` or `--project` instead of a positional argument.

```shell
dotnet test --solution "source/[[ product_name ]].slnx"
```

runs every test in the solution. To run only the test project:

```shell
dotnet test --project "tests/unit-tests/[[ product_name ]] Unit Tests.csproj"
```

## Measuring Code Coverage

Coverage is collected with [coverlet](https://github.com/coverlet-coverage/coverlet)'s extension for Microsoft.Testing.Platform, `coverlet.MTP`, which the test project references and `--coverlet` turns on:

```shell
dotnet test --solution "source/[[ product_name ]].slnx" --coverlet --coverlet-output-format cobertura --results-directory ./coverage
```

This writes a Cobertura-format report per test project into `./coverage`, named `coverage.cobertura.<timestamp>.xml`. Only the library is measured, not the test project itself. That raw XML is not meant to be read directly — turn it into an HTML report with [ReportGenerator](https://github.com/danielpalme/ReportGenerator), a pinned local `dotnet` tool declared in [`.config/dotnet-tools.json`](../../../.config/dotnet-tools.json):

```shell
dotnet tool restore
dotnet tool run reportgenerator -reports:"coverage/**/coverage.cobertura*.xml" -targetdir:coverage-report -reporttypes:Html
```

Open `coverage-report/index.html` to browse coverage by assembly, class, and line. Neither `coverage/` nor `coverage-report/` is committed — both are covered by [`.gitignore`](../../../.gitignore) — so it is safe to regenerate them at any time.

## No Minimum Coverage

There is no enforced minimum coverage percentage that fails the build. The expectation is stated as a rule instead of a number: a new feature arrives with tests, and a bug fix arrives with a test that would have caught it (see [testing](../conventions/testing.md)).

## Related

- [Testing](../conventions/testing.md) — the conventions the tests themselves follow.
- [Architecture](../architecture.md) — where the test project sits in the repository.
