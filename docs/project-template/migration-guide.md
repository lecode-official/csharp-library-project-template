# Migration Guide

This article covers what a generated project does by hand when it updates to a newer release of the template, in addition to what `copier update` does on its own. The message Copier shows after an update lists these steps briefly and links here.

There is one section per pair of consecutive releases, newest first. A project that skipped releases works through every section from the release it was generated from or last updated to, up to the release it updates to, oldest first. `.copier-answers.yml` records that release as `_commit`.

## Every Update

Some steps apply to every update, whatever changed (see [rendering and updating](rendering-and-updating.md#updating-a-project)):

- **Resolve the conflicts.** Copier applies the difference between the two releases to the project, and leaves a change that collides with the project's own as conflict markers in the file, or as a `.rej` file next to it.
- **Bring the lock files up to date.** When an update changed `package.json`, run `npm install`, and when it changed `Directory.Packages.props`, run `dotnet restore`. Commit the updated `package-lock.json` and `packages.lock.json` files with the update, since continuous integration fails on outdated ones.
- **Read the changelog.** The [changelog](../../CHANGELOG.md) of every release in between lists what changed, from the point of view of a generated project.
- **Update the files the project owns by hand.** Copier never updates the [files the template only creates](rendering-and-updating.md#files-the-template-only-creates), such as `README.md` and the logo. The sections below say when one of them changed, and how to carry the change over.

## Migrate from v1.0.0 to v1.1.0

No dependency changed, so the lock files stay as they are.

### The Read Me

`README.md` is only created by the template, so `copier update` leaves it alone. Three parts of it changed:

- **The title line.** The logo used to sit above the title text. Replace the first line, and the comment below it, with the new title line, which keeps the logo on the same line as the title:

  ```markdown
  # <img src="docs/assets/images/header-logo-light.svg#gh-light-mode-only" alt="Logo" height="40" align="top"> <img src="docs/assets/images/header-logo-dark.svg#gh-dark-mode-only" alt="Logo" height="40" align="top"> Product Name
  ```

- **The "Developer Setup" section.** It linked to `docs/developer-manual/tooling/developer-setup.md`, which moved to the new development setup section. Replace its content, including the code listing, with a short list of the requirements and a link to `docs/developer-manual/development-setup/README.md`.
- **The "Visual Studio Code Integration" section.** Remove it. How to run the tasks is now described in `docs/developer-manual/tooling/editor-integration.md`.

A fresh render with the project's own answers shows the new read me in full (see [files the template only creates](rendering-and-updating.md#files-the-template-only-creates)).

### The Logo

From v1.1.0 on, an update also leaves the logo files, the logo design article, and the index of the User Manual alone, so that a project's own logo and articles are never overwritten, and it no longer creates a file the template only creates again once the project has deleted it (see [files the template only creates](rendering-and-updating.md#files-the-template-only-creates)). This already applies to the update to v1.1.0 itself.

The new title line of the read me expects the header logos cropped to the drawing and 40 pixels high, which the placeholder's `docs/assets/images/header-logo-dark.svg` and `header-logo-light.svg` now are. A project that still uses the placeholder logo copies both files from a fresh render. A project with its own logo crops its own header logos the same way instead (see the project's `docs/developer-manual/logo-design.md`).

### The Labels on GitHub

Dependabot now labels its pull requests with a `Dependabot:` label per ecosystem instead of the labels it created itself. Dependabot never creates a label, so:

1. Create the new labels with the label script in the project's `docs/developer-manual/development-setup/setting-up-github.md`. The script also brings the existing labels in step with the GitHub workflow.
2. Delete the labels Dependabot created itself: `dependencies`, and one per ecosystem, such as `github_actions` and `javascript`.
3. Add the new labels to the Dependabot pull requests that are still open, since Dependabot does not relabel them.

### The Repository Settings

The new `docs/developer-manual/development-setup/setting-up-github.md` also has a script for the repository settings: merge commits only, the pull request's title and description as the default merge message, and no wiki and no projects. Run it if the repository is not set up that way yet.

## Related

- [Rendering and updating](rendering-and-updating.md) — what `copier update` does, and what it leaves alone.
- [Versioning](../conventions/versioning.md) — the releases this guide moves between.
- [Changelog](../conventions/changelog-entries.md) — how the template's changelog records each release.
