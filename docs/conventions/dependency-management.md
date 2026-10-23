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

## Related

- [Licensing](../project-template/licensing.md) — the vendored license texts and where they are pinned.
- [Developer setup](../tooling/developer-setup.md) — installing the root's dependencies.
