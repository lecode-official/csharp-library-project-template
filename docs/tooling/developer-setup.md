# Developer Setup

This article covers what to install before working on the template: what the root needs for its own linters, and what rendering and verifying a change needs on top.

## Node.js and npm

The root's linters and formatter are npm packages, so working on the template's own files needs only [Node.js](https://nodejs.org), which bundles npm. The root [`package.json`](../../package.json) declares the supported versions in `engines`. Then, in the repository root:

```shell
npm ci
```

Use `npm ci`, never `npm install`, so that a `package-lock.json` that no longer matches `package.json` fails instead of being silently rewritten (see [dependency management](../conventions/dependency-management.md)). Every tool is then available through `npx`, which resolves straight to the pinned version in `node_modules/.bin`.

Install scripts are blocked by default, and the one package that needs one is listed in the `allowScripts` map. If npm reports another, do not reach for `npm approve-scripts`, which writes the approval into the shared `package.json` for everyone. Add the entry as a reviewed change, or allow it for yourself only in your user-level `~/.npmrc`.

The [Claude Code hooks](claude-code-hooks.md) that run these tools read the edited file's path with [`jq`](https://jqlang.org/), so install it too, through the system's package manager. Without it, the hooks do not fail. They silently do nothing.

## Copier

Rendering the template needs [Copier](https://copier.readthedocs.io/en/stable/#installation), at least the version `_min_copier_version` in [`copier.yml`](../../copier.yml) names. Install it as an isolated command-line tool rather than into a project's Python environment, for example with `pipx install copier` or `uv tool install copier`.

## Python

[`scripts/refresh-licenses.py`](../../scripts/refresh-licenses.py) needs Python, and only its standard library.

## Visual Studio Code

Visual Studio Code is recommended, though not required. On first opening the repository it offers to install the extensions recommended in [`.vscode/extensions.json`](../../.vscode/extensions.json). Install all of them, and above all Workspace Config Plus, without which none of the shared editor configuration takes effect (see [editor integration](editor-integration.md)).

## Related

- [Editor integration](editor-integration.md) — the shared and local editor configuration.
- [Tooling](README.md) — what each installed tool does.
- [Authoring](../project-template/authoring.md) — rendering and verifying a change once everything is installed.
- [Dependency management](../conventions/dependency-management.md) — how the pinned versions are kept exact.
