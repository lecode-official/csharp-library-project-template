# Installing the Tools

This article covers what to install before working on the template: what the root needs for its own linters, what rendering and verifying a change needs on top, and the optional tools. Installation instructions are kept general here. Each tool links to its official instructions, which cover every operating system and stay up to date.

## Git

The template is a Git repository, and Copier reads a template's versions from its Git tags, so [Git](https://git-scm.com/downloads) is needed for everything else. Clone the repository and work in its root:

```shell
git clone https://github.com/lecode-official/csharp-library-project-template.git
cd csharp-library-project-template
```

## Node.js and npm

The root's linters and formatter are npm packages, so working on the template's own files needs only [Node.js](https://nodejs.org/en/download), which bundles npm. The root [`package.json`](../../package.json) declares the supported versions in `engines`. Then, in the repository root:

```shell
npm ci
```

Use `npm ci`, never `npm install`, so that a `package-lock.json` that no longer matches `package.json` fails instead of being silently rewritten (see [dependency management](../conventions/dependency-management.md)). Every tool is then available through `npx`, which resolves straight to the pinned version in `node_modules/.bin`.

Install scripts are blocked by default, and the one package that needs one is listed in the `allowScripts` map. If npm reports another, do not reach for `npm approve-scripts`, which writes the approval into the shared `package.json` for everyone. Add the entry as a reviewed change, or allow it for yourself only in your user-level `~/.npmrc`.

The [Claude Code hooks](../tooling/claude-code-hooks.md) that run these tools read the edited file's path with [`jq`](https://jqlang.org/download/), so install it too, through the system's package manager. Without it, the hooks do not fail. They silently do nothing.

## Copier

Rendering the template needs [Copier](https://copier.readthedocs.io/en/stable/#installation), at least the version `_min_copier_version` in [`copier.yml`](../../copier.yml) names. Install it as an isolated command-line tool rather than into a project's Python environment, for example with `pipx install copier` or `uv tool install copier`. The template's continuous integration renders with the exact version pinned in [`.github/workflows/template.yml`](../../.github/workflows/template.yml), so a local render with that version matches it most closely.

## What a Render Needs

A rendered project is verified with its own toolchain, so checking a change to the body needs that toolchain too:

- **The [.NET SDK](https://dotnet.microsoft.com/download)**, at the exact version the render's `global.json` pins. That is the answer to the `dotnet_sdk_version` question, so a change that is rendered once per serviced SDK band needs the SDK of each of those renders installed. `global.json` disables roll-forward, so a mismatched SDK fails outright.
- **[Python](https://www.python.org/downloads/)**, for the render's documentation website, installed into a virtual environment inside the render, never into the system or user Python installation.
- **Python**, also, for [`scripts/refresh-licenses.py`](../../scripts/refresh-licenses.py), which uses only the standard library.

The render's own [installing the tools](../../template/docs/developer-manual/development-setup/installing-the-tools.md) article covers each of these in detail, from the generated project's point of view.

## The GitHub CLI

The [GitHub CLI](https://cli.github.com/), `gh`, is optional. It is only needed to run the scripts that work on GitHub directly, such as the ones in [setting up GitHub](setting-up-github.md), and it is a convenient way to create branches from issues and to open and merge pull requests (see [GitHub workflow](../conventions/github-workflow.md)). After installing it, sign in once:

```shell
gh auth login
```

## Visual Studio Code

Visual Studio Code is the recommended editor, though not required. [Setting up Visual Studio Code](setting-up-visual-studio-code.md) covers installing it and its extensions.

## Related

- [Setting up GitHub](setting-up-github.md) — the labels and the repository settings.
- [Setting up Visual Studio Code](setting-up-visual-studio-code.md) — the editor and its extensions.
- [Tooling](../tooling/README.md) — what each installed tool does.
- [Authoring](../project-template/authoring.md) — rendering and verifying a change once everything is installed.
- [Dependency management](../conventions/dependency-management.md) — how the pinned versions are kept exact.
