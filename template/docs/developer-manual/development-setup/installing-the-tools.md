# Installing the Tools

This article covers what to install before building, testing, linting, or formatting [[ product_name ]] locally. Installation instructions are kept general here. Each tool links to its official instructions, which cover every operating system and stay up to date.

Not every section is needed for every task: Python is only needed to build the documentation website locally, `jq` only to let the Claude Code hooks run, and the GitHub CLI only to run the scripts that work on GitHub directly.

## Git

Install [Git](https://git-scm.com/downloads), then clone the repository and work in its root:

```shell
git clone [[ repository_url ]]
cd [[ product_slug ]]
```

## Node.js and npm

Install [Node.js](https://nodejs.org/en/download), which bundles npm, at the version pinned in [`.nvmrc`](../../../.nvmrc). With [nvm](https://github.com/nvm-sh/nvm) that is one command in the repository root:

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

That installs [ReportGenerator](https://github.com/danielpalme/ReportGenerator), used to turn raw coverage output into an HTML report (see [testing and code coverage](../tooling/testing-and-code-coverage.md)), and the XML-documentation-to-Markdown generator the [documentation website](../tooling/documentation-website.md) uses.

Then restore the solution's NuGet packages, at the versions locked in each project's `packages.lock.json`:

```shell
dotnet restore "source/[[ product_name ]].slnx"
```

## Python and the Documentation Website

The [documentation website](../tooling/documentation-website.md) is built with [ProperDocs](https://properdocs.org/), themed with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). Install [Python](https://www.python.org/downloads/), then create a virtual environment and install the pinned dependencies into it — never into the global or user Python installation:

```shell
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --requirement requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead of the `source` line. `.venv` is already excluded in [`.gitignore`](../../../.gitignore), so it is never committed.

Without a virtual environment, `pip` either installs the packages globally, where they are invisible to everyone else on the machine and collide with every other project's Python dependencies, or refuses outright with an externally-managed-environment error on a distribution that locks down the system interpreter.

Activate the environment in every new shell before running the documentation commands, and `deactivate` when done.

## jq for the Claude Code Hooks

The [Claude Code hooks](../tooling/claude-code-hooks.md) read the path of the edited file with [`jq`](https://jqlang.org/download/), so install it through the system's package manager, for example `brew install jq` on macOS or `sudo apt install jq` on Debian and Ubuntu. Without it, the hooks do not fail. They silently do nothing.

## The GitHub CLI

The [GitHub CLI](https://cli.github.com/), `gh`, is optional. It is only needed to run the scripts that work on GitHub directly, such as the ones in [setting up GitHub](setting-up-github.md), and it is a convenient way to create branches from issues and to open and merge pull requests (see [GitHub workflow](../conventions/github-workflow.md)). After installing it, sign in once:

```shell
gh auth login
```

## Visual Studio Code

Visual Studio Code is the recommended editor, though not required. [Setting up Visual Studio Code](setting-up-visual-studio-code.md) covers installing it and its extensions.

## Related

- [Setting up GitHub](setting-up-github.md) — the labels, the repository settings, and GitHub Pages.
- [Setting up Visual Studio Code](setting-up-visual-studio-code.md) — the editor and its extensions.
- [Tooling](../tooling/README.md) — what each installed tool does.
- [Dependency management](../conventions/dependency-management.md) — how these pinned versions are kept exact.
- [Continuous integration](../tooling/continuous-integration.md) — the versions to match locally.
- [Testing and code coverage](../tooling/testing-and-code-coverage.md) — running the tests once everything is installed.
- [Documentation website](../tooling/documentation-website.md) — building the site locally.
- [Claude Code hooks](../tooling/claude-code-hooks.md) — what `jq` is needed for.
