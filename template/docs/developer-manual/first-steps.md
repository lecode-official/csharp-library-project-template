# First Steps

This article covers what to do once, right after [[ product_name ]] was generated from the C# library project template: turning it into a repository, publishing it on GitHub, and replacing what the template only provides as a placeholder. The message Copier shows after generating the project lists only the first of these steps. This article covers all of them, in the order they are best done in.

## Creating the Repository

The generated project is complete, but it is not a Git repository yet, and it has no lock files. Install the [tools](development-setup/installing-the-tools.md) first, then, in the root of the project:

```shell
git init --initial-branch=[[ default_branch ]]
npm install
dotnet restore "source/[[ product_name ]].slnx"
dotnet test --solution "source/[[ product_name ]].slnx"
```

This is the one time `npm install` is right. The template ships no `package-lock.json`, so `npm ci` has nothing to install from yet, and `npm install` resolves the pinned dependencies and writes the lock file. `dotnet restore` does the same for the `packages.lock.json` of every project. Every later install uses `npm ci` (see [dependency management](conventions/dependency-management.md)).

**Commit all of the lock files with the first commit.** From then on, the project installs with `npm ci` and restores in locked mode, and its [continuous integration](tooling/continuous-integration.md) fails until the lock files are committed.

Everything should pass right away: the build, the tests, the formatter, and the linters.

## Publishing It on GitHub

Create an empty repository on GitHub at <[[ repository_url ]]>, without a read me, a license, or a `.gitignore`, since the project brings its own. Then [set it up](development-setup/setting-up-github.md), with its labels and its repository settings, **before** the first push. Dependabot opens its first pull requests as soon as its configuration arrives on GitHub, and it silently leaves out a label that does not exist yet.

Then push the project, and create the integration branch next to the default branch (see [Git workflow](conventions/git-workflow.md#the-branches)):

```shell
git remote add origin [[ repository_url ]]
git push --set-upstream origin [[ default_branch ]]
git switch --create [[ integration_branch ]]
git push --set-upstream origin [[ integration_branch ]]
```

Finally, enable [GitHub Pages](development-setup/setting-up-github.md#github-pages), or the workflow that publishes the documentation website fails on every push to `[[ default_branch ]]`.

## Setting up Visual Studio Code

Visual Studio Code is optional, but the repository ships a configuration for it. [Setting up Visual Studio Code](development-setup/setting-up-visual-studio-code.md) covers installing it and its extensions.

## Replacing the Placeholders

The template provides a few things that only exist so that the project works on day one. Replace them with the real thing:

- **The library.** The `Greeter` class in `source/[[ library_slug ]]/` and its `GreeterTests` in `tests/unit-tests/` only exist to make the build and the tests pass. Replace them with the library's real code and tests.
- **The sample app.** `source/sample-app/Program.cs` demonstrates the `Greeter` class. Rewrite it to demonstrate the real library.
- **The documentation.** The [getting started](../user-manual/getting-started.md) article of the User Manual and the read mes under `source/` describe the placeholder library. Rewrite them for the real one.
- **The logo.** Every generated project ships an open book with C# on its pages as its mark, used in the read me, the documentation website, the favicon, and the package icon. [Replacing the placeholder](logo-design.md#replacing-the-placeholder) lists the files and the steps.

## Deciding on the Documentation Website

The [documentation website](tooling/documentation-website.md) works as soon as the Python dependencies are installed and GitHub Pages is enabled. A project that will not publish one deletes `properdocs.yml`, `requirements.txt`, `docs/build/`, and the docs workflow, `.github/workflows/docs.yml`, rather than leaving them to rot.

## What to Read First

- [Architecture](architecture.md) — where the code lives and how the solution is put together.
- [Contributing](contribution-guide.md) — the process every change goes through.
- [Conventions](conventions/README.md) — how the code and the documentation are written.
- [`AGENTS.md`](../../AGENTS.md) — the rules for AI assistants, and which article to read for which task.

## Related

- [Development setup](development-setup/README.md) — installing the tools, and setting up GitHub and Visual Studio Code.
- [Logo design](logo-design.md) — the logo that replaces the placeholder.
- [Dependency management](conventions/dependency-management.md) — why the template ships no lock files.
