# Versioning

This article covers the version number: what it means here, when it is raised, everywhere it has to be raised at once, and how a release is tagged. The [changelog](changelog-entries.md) that records each release has an article of its own.

## One Number for the Whole Repository

Every manifest in the repository carries the same version — the library's project file and `package.json` (see [below](#everything-that-has-to-move-together)) — and they are raised together, **even when only one of them changed**. A change to one package still raises the others, and the other way round. The alternative is several numbers that drift apart, and then "which version does a consumer have" has no answer, only a list.

That an untouched package now claims a new version costs nothing. What it buys is that one number identifies one state of the whole repository, in every place the number appears.

A repository that publishes several independently installable packages is the exception, and it says so here.

## Raise It Before the Pull Request

The bump belongs **in the branch, in the change itself, before the pull request** — not as a step after the merge, and not when the package is published.

Where there is no release pipeline, the version on the default branch is the only record of what was released, and a bump that happens anywhere else is a bump that eventually does not happen at all. That is how a repository ends up sitting at `1.0.0` while it grows an entire new subsystem.

## Semantic Versioning, and Against What

The project follows [Semantic Versioning](https://semver.org). That only means something once it is clear what counts as the public surface. It is whatever other systems and other people depend on:

- The public and protected surface of the published assembly — its types, members, their signatures, and what they return.
- The target frameworks the package supports, which decide which projects can reference it at all.

Against that surface:

- **Major** — something that works today stops working: a type or member removed or renamed, a signature that no longer accepts what it did, a changed return type, or a **dropped target framework**, since a project that still targets it can no longer install the new version. Note that adding a member to a public interface is a breaking change for anyone who implements it.
- **Minor** — a new capability that takes nothing away: a new type, a new member, a new optional parameter with a default.
- **Patch** — a fix or an internal change that the surface does not notice, including documentation, tooling, and refactoring.

When a change is both, the highest one wins. A release that adds three capabilities and removes one is major, not minor.

## Everything That Has to Move Together

The version lives in two manifests, and nowhere else by default:

- **`source/[[ library_slug ]]/[[ product_name ]].csproj`** — the `<Version>` property, which is what NuGet publishes.
- **`package.json`** — the `"version"` field. The npm manifest is private and only declares the tooling, so nothing publishes it, but it is a manifest of this repository all the same, and it carries the same number rather than one of its own. `package-lock.json` repeats it, and `npm install` keeps the two in step.
- **`CHANGELOG.md`** — the release's own heading and date line (see [changelog](changelog-entries.md)).
- **Any version literal in the source** — a version a running program reports about itself.

The release workflow checks that the project file, both npm manifests, and the changelog agree before it tags a release (see [the release tags](#the-release-tags)). A version literal in the source it cannot check.

The sample app and the unit test project deliberately carry **no** version: neither is published, both set `IsPackable` to `false`, so a version on them would be a number nobody reads and everybody forgets to bump.

A repository that later grows a second publishable library raises both together, even when only one of them changed, so that one number identifies one state of the whole repository. State that here if it happens.

A version literal in the source is kept in step by nothing but this list. It is the one version an outside party actually reads. Reading it from the assembly instead would be better than remembering it — `Assembly.GetExecutingAssembly().GetName().Version` — and is worth doing the moment a second place needs it.

## The Release Tags

Every release has an annotated Git tag named exactly like the version, prefixed with `v` (`v0.1.0`, `v0.2.0`, and so on), pointing at the merge commit that brought the release into `[[ default_branch ]]`. The [Git workflow](git-workflow.md#tags) explains what a tag is and the rules every tag follows. A release is not complete until its tag exists and is pushed.

The [`Release`](../../../.github/workflows/release.yml) workflow creates the tag by itself once the release pull request is merged, and creates the GitHub Release from it (see [continuous integration](../tooling/continuous-integration.md#release-workflow)). Before it creates anything, it checks that the tag does not exist yet, that the release's date paragraph in the [changelog](changelog-entries.md) is set, and that the version is the same everywhere [it has to be](#everything-that-has-to-move-together), and it packs the library. Both texts come from [`.github/scripts/prepare-release.py`](../../../.github/scripts/prepare-release.py):

- **The tag message** repeats the release's changelog entry in plain text and follows the rules in [tag messages](commit-messages.md#tag-messages): the subject `Release vX.Y.Z (Month D, YYYY)`, with the date from the changelog, and the release's bullets, wrapped at 72 characters without breaking a code span.
- **The release notes** are the same bullets exactly as the changelog has them, unwrapped, since GitHub wraps them itself. The GitHub Release is titled `Release vX.Y.Z`, and the library's package and symbol package are attached to it.

The tag is created by `github-actions[bot]` and is not signed.

[%- if publish_to_nuget %]

Once the GitHub Release exists, a second job of the workflow publishes its package and symbol package to nuget.org, through NuGet's trusted publishing, which needs no API key in the repository (see [NuGet trusted publishing](../development-setup/setting-up-github.md#nuget-trusted-publishing)). A published version can never be replaced or deleted on nuget.org, only unlisted, so a version that turns out to be broken is fixed by releasing a new one.

[%- endif %]

The linters workflow runs the same script as a dry run on every pull request, so a changelog it cannot read fails long before the release. To see the tag message the next release will get, run it locally:

```shell
python3 .github/scripts/prepare-release.py --dry-run
```

When the workflow fails, the tag and the GitHub Release are created by hand instead, from the same texts. The script writes them into a directory, and the tag is pushed explicitly, since pushing a branch does not carry its tags along:

```shell
python3 .github/scripts/prepare-release.py --output-directory /tmp/release
git tag -a v0.1.0 <merge-commit> -F /tmp/release/tag-message.txt
git push origin v0.1.0
dotnet pack "source/[[ product_name ]].slnx" --configuration Release --output /tmp/packages
gh release create v0.1.0 --verify-tag --title "Release v0.1.0" --notes-file /tmp/release/release-notes.md /tmp/packages/*
```

[%- if publish_to_nuget %]

When only the publishing to nuget.org failed, re-run the failed job of the workflow run instead. It pushes with `--skip-duplicate`, so a package that already reached nuget.org does not fail it again. A trusted publishing token is only issued to the workflow itself, so a package is pushed by hand only with an API key created on nuget.org for that purpose.

[%- endif %]

The GitHub Release is always created from the existing tag. Typing a new tag name into GitHub's release form makes GitHub create the tag itself, and a tag GitHub creates is always lightweight, so the release would lose its tag message. `--verify-tag` makes the GitHub CLI fail instead.

To read the messages back:

```shell
git tag -n99 -l 'v*'   # every release tag with its full message
git tag -n99 v0.1.0    # one tag's message
git show v0.1.0        # the message plus the commit it points at
```

A tag that turns out to be wrong is deleted with `git tag -d v0.1.0` and recreated. Do that only while the tag is still local. Once it is pushed, other clones have it and it is treated as immutable — release a new version instead.

After the release pull request is merged, `[[ integration_branch ]]` is fast-forwarded to `[[ default_branch ]]` (see [bringing the integration branch back in step](git-workflow.md#bringing-the-integration-branch-back-in-step)). Creating and pushing a tag by hand, and the fast-forward, only happen when they were asked for (see [Git workflow](git-workflow.md#the-working-tree-belongs-to-the-author)).

## Package Validation

The library's project file sets `EnablePackageValidation`, so `dotnet pack` checks the package for consistency. Once a version has been released, set `<PackageValidationBaselineVersion>` in the library's project file to that version: every later package is then also compared against it, and a breaking change to the public API fails the pack.[% if not publish_to_nuget %] Package validation downloads the baseline package from a package source, and the package is not published on NuGet, so the directory that holds the package from that version's GitHub Release has to be a package source of the build, in a `nuget.config` next to the solution, or set `<PackageValidationBaselinePath>` to the package file instead.[% endif %] A breaking change that is intended, together with a raised major version, is accepted by generating a suppression file with `dotnet pack -p:GenerateCompatibilitySuppressionFile=true` and committing it.

## The Package and Its Symbols

`dotnet pack` writes two files for the library: the package itself, a `.nupkg`, and next to it a symbol package, a `.snupkg`, because the library's project file sets `IncludeSymbols` and `SymbolPackageFormat`. [% if publish_to_nuget %]The symbol package is published alongside the package. `dotnet nuget push` picks up a `.snupkg` lying next to the `.nupkg` and uploads it too, and nuget.org then serves it to debuggers through its symbol server, so that a consumer can step into the library's code.[% else %]Both are attached to every GitHub Release. A consumer who wants to step into the library's code adds the directory that holds the symbol package to the symbol paths of their debugger.[% endif %]

A package built on a GitHub Actions runner is deterministic. The root [`Directory.Build.props`](../../../Directory.Build.props) sets `ContinuousIntegrationBuild` to `true` whenever `GITHUB_ACTIONS` is `true`, which maps the runner's local source paths to repository-relative ones in the symbol files, so that a debugger finds the sources through Source Link. The setting is off everywhere else, because it makes local debugging harder, so a package built on a developer's machine carries that machine's paths instead.

## Related

- [Git workflow](git-workflow.md) — what a tag is, bringing `[[ integration_branch ]]` back in step after a release, and who runs which Git commands.
- [Commit messages](commit-messages.md) — how the bump is described, and the [tag message](commit-messages.md#tag-messages) rules.
- [Changelog](changelog-entries.md) — the release's entry, which the tag message repeats.
- [GitHub workflow](github-workflow.md) — the release issue, the release pull request, and the milestone.
- [Dependency management](dependency-management.md) — the lock files that move with the project files.
