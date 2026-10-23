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

## The Body's Dependencies

Everything the body pins becomes a pin in every generated project, so the body follows the generated project's [dependency management](../../template/docs/developer-manual/conventions/dependency-management.md) rules unchanged: exact package versions declared once in `template/Directory.Packages.props`, `RestorePackagesWithLockFile` on every project, and exact versions in `template/.config/dotnet-tools.json`.

Two pins are not constants at all:

- **The .NET SDK version** in `template/global.json` is the answer to the `dotnet_sdk_version` question. Its default and its help text name the newest patches of the serviced feature bands, and are raised when a new SDK ships (see [questions](../project-template/questions.md#dotnet_sdk_version)).
- **The target framework** is the answer to `target_framework`, and a new choice is added when a new .NET release ships.

## No Lock Files in the Body

The body ships no `packages.lock.json`. A generated project runs `dotnet restore` once, right after it is generated, and commits the lock files it writes (see [rendering and updating](../project-template/rendering-and-updating.md#after-generating)). From then on it restores in locked mode, like any other project.

Generating the lock files during rendering is not an option, because running a command at render time needs a Copier task, and a task forces every consumer to render with `--trust`.

Shipping them in the body would work for a first render, but it breaks `copier update`. A lock file records the whole resolved dependency graph, including every dependency a consumer has added since. As soon as a project's graph differs from the template's, every template change to the lock file arrives as a large merge conflict in a file nobody edits by hand. Without a lock file in the body, a template update only changes version strings in a project file, and the consumer's own `dotnet restore` brings their lock files up to date.

The cost is that a generated project's first install resolves transitive dependencies on the day it runs, rather than to versions the template chose. The direct dependencies are still pinned exactly, and everything is locked from the first commit on.

## Upgrading a Body Dependency

1. Change the version in the template file.
2. Render a project (see [authoring](../project-template/authoring.md#verifying-a-change)).
3. In the render, run `dotnet restore`, which is what a consumer does first, then build and test.
4. If the dependency also has a root counterpart, raise that in the same change.

The upgrade reaches existing generated projects through `copier update`, as an ordinary change to their version strings.

## Related

- [Questions](../project-template/questions.md) — the SDK version and the target framework.
- [Licensing](../project-template/licensing.md) — the vendored license texts and where they are pinned.
- [Developer setup](../tooling/developer-setup.md) — installing the root's dependencies.
- [Dependency management](../../template/docs/developer-manual/conventions/dependency-management.md) — the generated project's full rule set.
