# Changelog

All notable changes to the C# library project template are documented here, newest release first. Each release corresponds to an annotated Git tag of the same name.

## Release v1.1.0

*Release date to be determined.*

- Fixed the alignment of the logo in the title of the generated read me, which sat above the title text. An existing project keeps its read me on `copier update`, because the template only creates it, so it copies the new title line by hand.
- Documented fast-forwarding the integration branch after a release, creating the GitHub Release from an existing annotated tag, and deleting merged feature branches, in the conventions of the template repository and of the generated project.
- Added the rule that Markdown files contain no comments to the conventions of the template repository and of the generated project.
- Moved the changelog conventions out of the versioning articles into an article of their own, in the conventions of the template repository and of the generated project.
- Rewrote the Git workflow articles of the template repository and of the generated project to cover the branches, the `feature/` and `fix/` branch names, rebasing a branch to bring it up to date, and tags, stated that a release tag points at the merge commit that brought the release into the default branch, and moved fast-forwarding the integration branch after a release there from the versioning articles.
- Added an article on the GitHub workflow to the conventions of the template repository and of the generated project, covering issues, issue and pull request titles, labels, milestones, pull requests, and releases.
- Added a development setup section to the documentation of the template repository and of the generated project. It moves the developer setup articles there as "Installing the Tools", which now also cover Git and the optional GitHub CLI, and adds articles on setting up Visual Studio Code and on setting up GitHub, with scripts for the labels, the repository settings, and, in the generated project, GitHub Pages. The read me of the generated project now only lists the requirements and links to the new section. An existing project keeps its read me on `copier update`, because the template only creates it, so it can replace its "Developer Setup" section and remove its "Visual Studio Code Integration" section by hand.
- Labeled the pull requests of Dependabot with a `Dependabot:` label per ecosystem, `Dependabot: GitHub Actions Update`, `Dependabot: NuGet Update`, `Dependabot: .NET SDK Update`, `Dependabot: npm Update`, and `Dependabot: pip Update`, instead of the labels Dependabot creates itself, and documented how a Dependabot pull request is reviewed. Dependabot never creates these labels, so an existing project creates them with the label script in its development setup, deletes the `dependencies` label and the ecosystem labels Dependabot created, and relabels the Dependabot pull requests that are still open.
- Added messages that Copier shows after generating and after updating a project. The message after generating lists what has to happen before the first commit and points to a new first steps article in the generated project, which covers everything else to do once. The message after updating lists the steps every update needs and a hint for every release that changed something to carry over by hand, and points to a new migration guide in the template repository. Neither needs `--trust`.
- Excluded the files every project fills with its own content from every update: the read mes, the changelog, the list of contributors, the sample app, the index and the getting started article of the User Manual, and now also the logo files, the brand colors, and the logo design article. `copier update` neither overwrites them nor creates them again once a project has deleted them, which `_skip_if_exists` did before. The template now needs Copier 9.6.0 or newer. A project that still uses the placeholder logo copies `docs/assets/images/header-logo-dark.svg` and `header-logo-light.svg` from a fresh render, since the new title line of the read me expects them cropped.

## Release v1.0.0

*Released on October 23, 2026.*

- Added the tooling of the template repository itself: formatting with dprint, Markdown linting with MarkdownLint, spell checking with CSpell, the Visual Studio Code integration, and the Claude Code hooks.
- Added the conventions of the template repository, its `AGENTS.md`, and its community files.
- Added the Copier template: the core questions with their validators, and the split between the template repository and the template body in `template/`.
- Added the `license` question, with ten vendored license texts and the script that refreshes them.
- Added the documentation of the generated project: its read me, `AGENTS.md`, community files, changelog, and the developer and user manuals.
- Added the C# solution of the generated project: the library, the sample app, and the pinned .NET SDK.
- Added the NuGet packaging of the library: package metadata, inherited documentation comments, package validation, and a symbol package.
- Added the unit test project of the generated project, based on xUnit v3 and Microsoft.Testing.Platform, with code coverage.
- Added Central Package Management, lock files, and the NuGet vulnerability audit to the generated project.
- Added formatting with dprint, Markdown linting with MarkdownLint, and spell checking with CSpell to the generated project.
- Added strict static code analysis to the generated project, with the .NET analyzers, StyleCop Analyzers, Roslynator, and Nullable.Extended.
- Added the documentation website of the generated project, built with ProperDocs, including a generated API reference.
- Added the continuous integration workflows and the Dependabot configuration of the generated project.
- Added the Visual Studio Code integration of the generated project.
- Added the Claude Code integration of the generated project.
- Added a placeholder logo to the generated project, used in its read me, its documentation website, its favicon, and its package icon.
- Added the continuous integration of the template repository, which renders the template with every license and both serviced SDK bands.
