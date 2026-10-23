# Dependency Management

This article covers how dependencies — NuGet packages, the .NET SDK, and the local .NET tools — are pinned and locked in this repository.

## Exact Versions, Never Ranges

Every dependency is pinned to an exact version — never a floating range, a minimum-version range, or a wildcard. NuGet package versions are declared in one place, [`Directory.Packages.props`](../../../Directory.Packages.props) (Central Package Management), and look like this:

```xml
<PackageVersion Include="SauceControl.InheritDoc" Version="2.0.2" />
```

not `Version="2.*"` or `Version="[2.0.2,)"`. A project file references the package without a version, `<PackageReference Include="SauceControl.InheritDoc" PrivateAssets="all" />`, so two projects can never depend on different versions of the same package. A package that every project needs, such as an analyzer, is declared as a `GlobalPackageReference` in the same file instead, and no project file mentions it at all. The same rule applies outside NuGet:

- [`global.json`](../../../global.json) pins the exact .NET SDK version.

An upgrade is always a deliberate, visible change to a version string, never something that happens silently on the next restore.

## The Pinned SDK

[`global.json`](../../../global.json) pins the SDK to `[[ dotnet_sdk_version ]]` with `"rollForward": "disable"`, so a machine with a different patch level **fails outright** rather than silently substituting another toolchain. Even a newer patch does not satisfy it.

That is deliberate: it is what keeps the lock files below meaningful, since a different SDK can resolve a different dependency graph. Two settings soften the edges — `errorMessage` replaces the default SDK-not-found message with one that says where to get the right version, and `allowPrerelease: false` stops a preview SDK from ever being resolved.

Install the exact version from the [.NET downloads page](https://dotnet.microsoft.com/download/dotnet/10.0), or point `sdk.paths` at a repository-local SDK.

## Lock Files

Every project sets:

```xml
<RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
```

which makes `dotnet restore` generate and verify a `packages.lock.json` next to the project, recording the exact resolved version and content hash of every direct and transitive dependency. These files are committed.

With them in place, a restore fails loudly if the resolved graph would differ from what is locked — because a transitive dependency's range allows a newer release, for instance — instead of silently picking up a different set of packages than the last person who restored. `dotnet restore --locked-mode` turns that into a hard failure.

**When a package reference or a package version changes, run `dotnet restore` and commit the resulting `packages.lock.json` files alongside the change to the project file or `Directory.Packages.props`.** They move together.

## Vulnerability Audit

Every restore audits the dependencies for known vulnerabilities, and [`Directory.Build.props`](../../../Directory.Build.props) sets `NuGetAuditMode` to `all`, so the transitive dependencies are audited as well, not only the direct ones. A vulnerable package is reported as a warning on every restore. Upgrade the package, or the direct dependency that pulls it in, rather than suppressing the warning.

## Local .NET Tools

[`.config/dotnet-tools.json`](../../../.config/dotnet-tools.json) is a `dotnet` local tool manifest, restored with `dotnet tool restore`. It exists for tools invoked as part of the .NET build rather than through Node.js:

- **ReportGenerator**, which turns raw coverage data into a readable report (see [testing and code coverage](../tooling/testing-and-code-coverage.md)).

Each tool's version is pinned exactly, with `"rollForward": false`. Upgrading one is `dotnet tool update <tool name> --version <exact version>`, followed by committing the manifest change.

## Related

- [Developer setup](../tooling/developer-setup.md) — running these installs on a fresh machine.
- [Architecture](../architecture.md) — where the project files that set these properties live.
- [Versioning](versioning.md) — how the project's own version moves.
