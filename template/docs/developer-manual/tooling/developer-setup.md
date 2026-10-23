# Developer Setup

This article covers what to install before building or testing [[ product_name ]] locally.

## .NET SDK

Install the exact .NET SDK version pinned in [`global.json`](../../../global.json) from the [.NET downloads page](https://dotnet.microsoft.com/download). `global.json` sets `rollForward` to `disable`, so a mismatched version fails outright rather than silently substituting a different one.

Once the SDK is installed, restore the pinned local `dotnet` tools declared in [`.config/dotnet-tools.json`](../../../.config/dotnet-tools.json):

```shell
dotnet tool restore
```

That installs [ReportGenerator](https://github.com/danielpalme/ReportGenerator), used to turn raw coverage output into an HTML report (see [testing and code coverage](testing-and-code-coverage.md)).

## Related

- [Tooling](README.md) — what each installed tool does.
- [Dependency management](../conventions/dependency-management.md) — how these pinned versions are kept exact.
- [Testing and code coverage](testing-and-code-coverage.md) — running the tests once everything is installed.
