# Versioning

This article covers the version number: what it means here, when it is raised, everywhere it has to be raised at once, and how a release is recorded.

## One Number for the Whole Repository

Every manifest in the repository carries the same version — so far, that is the library's project file (see [below](#everything-that-has-to-move-together)) — and they are raised together, **even when only one of them changed**. A change to one package still raises the others, and the other way round. The alternative is several numbers that drift apart, and then "which version does a consumer have" has no answer, only a list.

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

The version lives in one manifest, and nowhere else by default:

- **`source/[[ library_slug ]]/[[ product_name ]].csproj`** — the `<Version>` property, which is what NuGet publishes.
- **`CHANGELOG.md`** — the release's own heading and date line.
- **Any version literal in the source** — a version a running program reports about itself.

The sample app and the unit test project deliberately carry **no** version: neither is published, both set `IsPackable` to `false`, so a version on them would be a number nobody reads and everybody forgets to bump.

A repository that later grows a second publishable library raises both together, even when only one of them changed, so that one number identifies one state of the whole repository. State that here if it happens.

A version literal in the source is kept in step by nothing but this list. It is the one version an outside party actually reads. Reading it from the assembly instead would be better than remembering it — `Assembly.GetExecutingAssembly().GetName().Version` — and is worth doing the moment a second place needs it.

## The Changelog

[`CHANGELOG.md`](../../../CHANGELOG.md) at the repository root lists every release, newest first. Each release is a level-two heading naming the version, followed by a single italic paragraph with the release date, followed by a flat list of changes:

```markdown
## Release v0.3.0

*Released on August 12, 2026.*

- Change 1
- Change 2
```

An unreleased version's date paragraph reads `*Release date to be determined.*` until it ships. The entries follow the same prose rules as everything else here: past tense, periods rather than semicolons, and backticks around file names, paths, identifiers, and code.

## The Release Tags

Every release has an **annotated** Git tag named exactly like the version, prefixed with `v` (`v0.1.0`, `v0.2.0`, and so on), pointing at the commit that bumped the version. Lightweight tags are not used, because the tag message is part of the release record. A release is not complete until its tag exists and is pushed.

The tag message repeats the release's changelog entry in plain text, and follows the rules in [tag messages](commit-messages.md#tag-messages). Write it into a file first and pass it with `-F`, so the wrapping is preserved exactly rather than being re-wrapped or mangled by a shell quoting mistake. Tags are pushed explicitly — pushing a branch does not carry its tags along:

```shell
git tag -a v0.1.0 <commit> -F <message-file>
git push origin v0.1.0
```

To read the messages back:

```shell
git tag -n99 -l 'v*'   # every release tag with its full message
git tag -n99 v0.1.0    # one tag's message
git show v0.1.0        # the message plus the commit it points at
```

A tag that turns out to be wrong is deleted with `git tag -d v0.1.0` and recreated. Do that only while the tag is still local. Once it is pushed, other clones have it and it is treated as immutable — release a new version instead.

## Package Validation

The library's project file sets `EnablePackageValidation`, so `dotnet pack` checks the package for consistency. Once a version has been published, set `<PackageValidationBaselineVersion>` in the library's project file to that version: every later package is then also compared against it, and a breaking change to the public API fails the pack. A breaking change that is intended, together with a raised major version, is accepted by generating a suppression file with `dotnet pack -p:GenerateCompatibilitySuppressionFile=true` and committing it.

## The Package and Its Symbols

`dotnet pack` writes two files for the library: the package itself, a `.nupkg`, and next to it a symbol package, a `.snupkg`, because the library's project file sets `IncludeSymbols` and `SymbolPackageFormat`. The symbol package is published alongside the package. `dotnet nuget push` picks up a `.snupkg` lying next to the `.nupkg` and uploads it too, and nuget.org then serves it to debuggers through its symbol server, so that a consumer can step into the library's code.

A package built on a GitHub Actions runner is deterministic. The root [`Directory.Build.props`](../../../Directory.Build.props) sets `ContinuousIntegrationBuild` to `true` whenever `GITHUB_ACTIONS` is `true`, which maps the runner's local source paths to repository-relative ones in the symbol files, so that a debugger finds the sources through Source Link. The setting is off everywhere else, because it makes local debugging harder, so a package built on a developer's machine carries that machine's paths instead.

## Related

- [Git workflow](git-workflow.md) — who runs which Git commands, which includes creating and pushing a release tag.
- [Commit messages](commit-messages.md) — how the bump is described, and the [tag message](commit-messages.md#tag-messages) rules.
- [Markdown style](markdown-style.md) — the conventions the changelog is written to.
- [Dependency management](dependency-management.md) — the lock files that move with the project files.
