# Developer Setup

This article covers what to install before building, testing, linting, or formatting [[ product_name ]] locally.

## Node.js and npm

Install [Node.js](https://nodejs.org), which bundles npm, at the version pinned in [`.nvmrc`](../../../.nvmrc). With [nvm](https://github.com/nvm-sh/nvm) that is one command in the repository root:

```shell
nvm use
```

Then install the exact locked dependency versions:

```shell
npm ci
```

Use `npm ci`, never `npm install`, for a fresh setup. `npm install` happily updates `package-lock.json`. `npm ci` fails instead, which is what makes a local run predict a continuous integration run (see [dependency management](../conventions/dependency-management.md)).

The one exception is a repository that has no `package-lock.json` yet, which is the case right after it was generated. `npm ci` refuses to run without one, so run `npm install` once to resolve the pinned dependencies and write the lock file, and commit it. Every install after that uses `npm ci`.

Install scripts are blocked by default, and the packages that genuinely need one are listed in the `allowScripts` map in [`package.json`](../../../package.json). If npm reports a package whose install script is not yet covered, do not reach for `npm approve-scripts`: it writes the approval into the shared, committed `package.json`, approving it for everyone rather than for you. Either add the entry deliberately as a reviewed change, or allow it for yourself only through an `allow-scripts` line in your user-level `~/.npmrc`.

Every tool is then available through `npx`, which resolves straight to the pinned version in `node_modules/.bin`:

```shell
npm run format
npm run lint
npm test
```

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
