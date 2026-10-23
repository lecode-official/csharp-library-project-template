# Dependency Management

This article covers how dependencies — NuGet packages, but also the linters and the code formatter from [tooling](../tooling/README.md) — are pinned and locked in this repository.

## Exact Versions, Never Ranges

Every dependency is pinned to an exact version — never a floating range, a minimum-version range, or a wildcard. NuGet package versions are declared in one place, [`Directory.Packages.props`](../../../Directory.Packages.props) (Central Package Management), and look like this:

```xml
<PackageVersion Include="SauceControl.InheritDoc" Version="2.0.2" />
```

not `Version="2.*"` or `Version="[2.0.2,)"`. A project file references the package without a version, `<PackageReference Include="SauceControl.InheritDoc" PrivateAssets="all" />`, so two projects can never depend on different versions of the same package. A package that every project needs, such as an analyzer, is declared as a `GlobalPackageReference` in the same file instead, and no project file mentions it at all. The same rule applies outside NuGet:

- The dprint plugins in [`dprint.json`](../../../dprint.json) are pinned to an exact release URL.
- `dprint`, `cspell`, its `@cspell/dict-*` dictionary packages, `markdownlint-cli2`, and `npm-run-all2` are pinned exactly in [`package.json`](../../../package.json).
- The Python packages that build the documentation website are pinned exactly in [`requirements.txt`](../../../requirements.txt).
- [`global.json`](../../../global.json) pins the exact .NET SDK version.

The analyzer packages are no exception (see [static code analysis](../tooling/static-code-analysis.md)). Because a new analyzer version usually brings new rules, and a Release build fails on every new finding, upgrading one is a change of its own that fixes or configures whatever the new version reports.

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

Every restore audits the dependencies for known vulnerabilities, and [`Directory.Build.props`](../../../Directory.Build.props) sets `NuGetAuditMode` to `all`, so the transitive dependencies are audited as well, not only the direct ones. A vulnerable package is a warning, which a Release build turns into an error. Upgrade the package, or the direct dependency that pulls it in, rather than suppressing the warning.

## Local .NET Tools

[`.config/dotnet-tools.json`](../../../.config/dotnet-tools.json) is a `dotnet` local tool manifest, restored with `dotnet tool restore`. It exists for tools invoked as part of the .NET build rather than through Node.js or Python:

- **ReportGenerator**, which turns raw coverage data into a readable report (see [testing and code coverage](../tooling/testing-and-code-coverage.md)).
- **xmldoc2md**, which generates the API reference section of the documentation website (see [documentation website](../tooling/documentation-website.md)).

Each tool's version is pinned exactly, with `"rollForward": false`. Upgrading one is `dotnet tool update <tool name> --version <exact version>`, followed by committing the manifest change.

## Node.js Dependencies

The linters and the code formatter are npm packages, declared as `devDependencies` in [`package.json`](../../../package.json) and locked in `package-lock.json`, together with `npm-run-all2`, whose `run-s` runs the linters one after the other for `npm run lint` (see [tooling](../tooling/README.md)). The Node.js version itself is pinned in [`.nvmrc`](../../../.nvmrc). `nvm use` selects it, and the continuous integration workflows read the same file, so the two cannot drift.

Restore them with `npm ci`, never `npm install` — `npm ci` fails instead of silently updating the lock file when it would no longer match `package.json`, which is the same guarantee `--locked-mode` gives the NuGet restore. The only exception is the very first install, before any `package-lock.json` exists: `npm install` writes it, and it is committed straight away. The same goes for the `packages.lock.json` files, which the first `dotnet restore` writes.

Install scripts are blocked by default. The one package that genuinely needs one, `dprint`, is listed explicitly in the `allowScripts` map, keyed by exact name and version. A version bump means updating that key too, or the script silently stops being allowed.

## Python Dependencies

[`requirements.txt`](../../../requirements.txt) pins the exact versions of ProperDocs, its theme and its plugins. Unlike the NuGet and npm dependencies, there is **no lock file** recording transitive versions — only the direct dependencies are pinned.

Install it inside a virtual environment, never against the system or user Python installation (see [developer setup](../tooling/developer-setup.md)). Without one, `pip` either installs the packages globally, where they are invisible to every other project, or refuses outright with an externally-managed-environment error.

## Related

- [Developer setup](../tooling/developer-setup.md) — running these installs on a fresh machine.
- [Architecture](../architecture.md) — where the project files that set these properties live.
- [Versioning](versioning.md) — how the project's own version moves.
