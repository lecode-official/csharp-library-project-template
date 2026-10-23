# Dependency Management

This article covers how dependencies are pinned on both sides of the split: the tools this repository uses on its own files, and the dependencies the template body hands to every generated project.

## Exact Versions, Never Ranges

Every dependency is pinned to an exact version, at the root and in the body alike. Never a floating range, a minimum-version range, or a wildcard. An upgrade is always a deliberate, visible change to a version string, never something that happens silently on the next install.

## The Root's Own Dependencies

The root needs very little, and all of it is pinned:

- **The linters and the formatter** are `devDependencies` in the root [`package.json`](../../package.json), pinned exactly and locked in `package-lock.json`. Install them with `npm ci`, never `npm install`, so that a lock file that no longer matches fails instead of being silently rewritten.
- **`dprint`'s install script** is the one that is allowed to run, through the `allowScripts` map, keyed by exact name and version. A version bump means updating that key too, or the script silently stops being allowed.
- **The dprint plugins** in the root [`dprint.json`](../../dprint.json) are pinned to an exact release URL.
- **The verbatim license texts** are pinned to a tagged release of the SPDX license list, through `SPDX_LICENSE_LIST_VERSION` in [`scripts/refresh-licenses.py`](../../scripts/refresh-licenses.py). The choosealicense.com texts have no release tags, so they are pinned to a commit of the repository's `gh-pages` branch through `CHOOSE_A_LICENSE_COMMIT` instead. Review the diff of every refresh before keeping it (see [licensing](../project-template/licensing.md#where-the-texts-come-from)).
- **Copier itself** is not pinned for consumers, since it runs on their machines, but `_min_copier_version` in [`copier.yml`](../../copier.yml) declares the oldest release the template works with. Raise it in the same change that starts relying on a newer Copier feature.
- **The Copier the continuous integration renders with** is pinned to an exact version in [`.github/workflows/template.yml`](../../.github/workflows/template.yml), currently `copier==9.19.1`. Dependabot does not see a version in a `pip install` command, so raise it by hand, and render with the new version before keeping it.
- **The actions** in that workflow are pinned to the full commit SHA of a release, with the version in a comment next to it, because a tag can be moved and a commit SHA cannot.

## Dependabot at the Root

[`.github/dependabot.yml`](../../.github/dependabot.yml) checks two ecosystems at the root once a week, and groups each one's updates into a single pull request:

- **`github-actions`**, for the actions of the root's own workflow. Its pull request updates both the commit SHA and the version in the comment.
- **`npm`**, for the formatter and the linters in the root `package.json`.

It does not reach into `template/`, whose dependencies are raised deliberately and verified by rendering. A root npm pull request is therefore never complete on its own. The root and the body run the same tool versions (see below), so mirror every version it raises in `template/package.json` in the same change, update the `allowScripts` key of `dprint` in both files when its version changes, and render before merging.

The body ships a Dependabot configuration of its own, `template/.github/dependabot.yml`, which keeps a generated project's actions, NuGet packages, .NET SDK, npm and pip dependencies up to date once that project exists. It never runs in this repository, because Dependabot only reads the configuration at `.github/dependabot.yml`.

## The Body's Dependencies

Everything the body pins becomes a pin in every generated project, so the body follows the generated project's [dependency management](../../template/docs/developer-manual/conventions/dependency-management.md) rules unchanged: exact package versions declared once in `template/Directory.Packages.props`, `RestorePackagesWithLockFile` on every project, exact versions in `template/package.json`, `template/requirements.txt` and `template/.config/dotnet-tools.json`, and a Node.js version pinned in `template/.nvmrc`.

Two pins are not constants at all:

- **The .NET SDK version** in `template/global.json` is the answer to the `dotnet_sdk_version` question. Its default and its help text name the newest patches of the serviced feature bands, and are raised when a new SDK ships (see [questions](../project-template/questions.md#dotnet_sdk_version)).
- **The target framework** is the answer to `target_framework`, and a new choice is added when a new .NET release ships.

## No Lock Files in the Body

The body ships neither a `package-lock.json` nor any `packages.lock.json`. A generated project runs `npm install` and `dotnet restore` once, right after it is generated, and commits the lock files they write (see [rendering and updating](../project-template/rendering-and-updating.md#after-generating)). From then on it installs with `npm ci` and restores in locked mode, like any other project.

Generating the lock files during rendering is not an option, because running a command at render time needs a Copier task, and a task forces every consumer to render with `--trust`.

Shipping them in the body would work for a first render, but it breaks `copier update`. A lock file records the whole resolved dependency graph, including every dependency a consumer has added since. As soon as a project's graph differs from the template's, every template change to the lock file arrives as a large merge conflict in a file nobody edits by hand. Without a lock file in the body, a template update only changes version strings in `package.json` or a project file, and the consumer's own `npm install` or `dotnet restore` brings their lock file up to date.

The cost is that a generated project's first install resolves transitive dependencies on the day it runs, rather than to versions the template chose. The direct dependencies are still pinned exactly, and everything is locked from the first commit on.

## Keep Shared Tools in Step

The root and the body run the same tools on their Markdown, `dprint`, `markdownlint-cli2` and `cspell`, with the same dprint plugins for Markdown, JSON, YAML and TOML. `markdownlint-cli2` brings its own copy of the `markdownlint` library, so neither side declares that one directly. They also run them the same way, through the `run-s` command of `npm-run-all2`, which `npm run lint` uses on both sides. Their versions are the same on both sides, and they are raised together, in the same change.

The reason is that a root article and a body article are written to the same conventions, and a rule that behaves differently between two versions of a linter would let one side pass what the other rejects. Check both `package.json` files and both `dprint.json` files whenever you bump one of them.

## Upgrading a Body Dependency

1. Change the version in the template file.
2. Render a project (see [authoring](../project-template/authoring.md#verifying-a-change)).
3. In the render, run `npm install` and `dotnet restore`, which is what a consumer does first, then lint, build and test.
4. If the dependency also has a root counterpart, raise that in the same change.

An analyzer package (StyleCop Analyzers, Roslynator) needs more than a passing render. A new version usually brings new rules, so read its release notes, and decide for every new rule whether `template/.globalconfig` enables, configures, or turns it off, with a comment that says why. The body's own C# has to stay free of findings, because a Release build in every generated project fails on any of them.

The upgrade reaches existing generated projects through `copier update`, as an ordinary change to their version strings.

## Related

- [Questions](../project-template/questions.md) — the SDK version and the target framework.
- [Testing](testing.md) — the continuous integration that renders with the pinned Copier.
- [Licensing](../project-template/licensing.md) — the vendored license texts and where they are pinned.
- [Developer setup](../tooling/developer-setup.md) — installing the root's dependencies.
- [Dependency management](../../template/docs/developer-manual/conventions/dependency-management.md) — the generated project's full rule set.
