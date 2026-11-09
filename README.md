# C# Library Project Template

A [Copier](https://copier.readthedocs.io/) template for C# library projects. It generates a repository with a library, a sample app, an xUnit test project, a published documentation website, a full set of conventions documentation, and the linting, formatting, editor and continuous integration setup that goes with them.

## Generating a Project

Install [Copier](https://copier.readthedocs.io/en/stable/#installation), then:

```shell
copier copy gh:lecode-official/csharp-library-project-template my-new-library
```

Copier asks a handful of questions and writes the rendered project into `my-new-library`. Every answer is validated, so an answer that would break the generated project is rejected with a message that says what is allowed. **No `--trust` flag is needed** — this template deliberately uses no tasks, no migrations and no Jinja extensions, so nothing runs on your machine during generation.

Afterwards, Copier lists what to do before the first commit: create the Git repository, install the npm packages, and restore the NuGet packages. The template ships no lock files, so this first `npm install` writes `package-lock.json`, and `dotnet restore` writes a `packages.lock.json` per project. Commit them with the first commit, since the project's continuous integration fails without them. Everything else, from setting up GitHub to replacing the placeholder logo, is described in the generated project's own [first steps](template/docs/developer-manual/first-steps.md).

The generated project builds, tests, formats and lints green out of the box. The library it ships is a placeholder class that exists so all of that is true on day one — replace it with the real thing.

See [rendering and updating](docs/project-template/rendering-and-updating.md) for the full walkthrough, and [questions](docs/project-template/questions.md) for what each question means.

## Updating a Project

A project generated from this template records its answers in `.copier-answers.yml`, so it can pull in later template changes:

```shell
copier update
```

Copier re-renders the old and the new version of the template and applies the difference to your working tree, leaving conflicts for you to resolve. Commit your work first — `copier update` requires a clean working tree. Afterwards, Copier lists what to do by hand, and the [migration guide](docs/project-template/migration-guide.md) covers it in detail, release by release. Files that every project fills with its own content, such as the read me and the changelog, are created once and never touched by an update (see [rendering and updating](docs/project-template/rendering-and-updating.md#files-the-template-only-creates)).

## How This Template Is Laid Out

This repository is **not** itself a renderable project. It is split in two:

```text
.
├── copier.yml          the questions and the Copier settings
├── README.md           this file — the template's own documentation
├── AGENTS.md           rules for working on the template
├── CONTRIBUTING.md     how to contribute, next to CODE_OF_CONDUCT.md, SECURITY.md, and CONTRIBUTORS.md
├── docs/               how the template works and how to change it
├── licenses/           the vendored license texts the LICENSE file pulls from
├── scripts/            maintenance scripts, run by hand
├── .github/            the template repository's own continuous integration and Dependabot
└── template/           ← the template body; only this is ever rendered
```

Everything outside `template/` belongs to the template itself and is never copied into a generated project. That split is the whole point, and [template structure](docs/project-template/template-structure.md) explains what it buys.

## Documentation

The [documentation index](docs/README.md) lists every article. It is split into four sections:

- [Project template](docs/project-template/README.md) — the repository as a Copier template.
  - [Template structure](docs/project-template/template-structure.md) — the two-level layout, and the four problems it solves.
  - [Questions](docs/project-template/questions.md) — every question, what it feeds, and how to add one.
  - [Licensing](docs/project-template/licensing.md) — how the `LICENSE` file is produced, and which licenses take a copyright substitution.
  - [Rendering and updating](docs/project-template/rendering-and-updating.md) — generating a project, and keeping it in step with the template.
  - [Migration guide](docs/project-template/migration-guide.md) — what a project does by hand when it updates, release by release.
  - [Authoring](docs/project-template/authoring.md) — the delimiters, adding a file, and verifying a change.
- [Development setup](docs/development-setup/README.md) — what to install and set up before working on the template.
- [Conventions](docs/conventions/README.md) — how the files on both sides of the split are written, styled, named, committed, and released.
- [Tooling](docs/tooling/README.md) — the formatter, the linters, the editor setup, and the Claude Code hooks used to work on the template.

## Requirements

- **Copier 9.10.3 or newer**, the floor `copier.yml` declares with `_min_copier_version`. The template's continuous integration renders and updates it with Copier 9.19.1, and with that floor.
- **The .NET SDK** pinned by the generated project's `global.json`, to build what comes out.
- **Node.js and Python**, for the generated project's linters and its documentation website respectively.
- **The GitHub CLI**, optionally, to run the scripts that set up a repository on GitHub.

Working on the template's own files needs only Git and Node.js, for the formatter and the linters that check them. Verifying a change to the template body also needs Copier and everything a render needs. The [development setup](docs/development-setup/README.md) covers installing all of it, setting up the repository on GitHub, and setting up Visual Studio Code.

## Continuous Integration

Two workflows run on every push and pull request. The [`Linters`](.github/workflows/linters.yml) workflow lints this repository's own files. The [`Tests`](.github/workflows/tests.yml) workflow renders the template body with several answer sets, which together cover every license, and updates a project rendered from the last release to the current commit, and runs each generated project's linters, tests and packaging, exactly as a consumer would. [Testing](docs/conventions/testing.md#continuous-integration) covers what it checks, and why it does not replace rendering a change locally before pushing it.

## Use of AI

This template is developed with the help of AI, and that is disclosed rather than hidden. A project template is mostly boilerplate — configuration files, workflows, scaffolding, and the documentation that explains them — and most of that boilerplate was produced with AI. What was not delegated is every decision about the template: which tools it uses, which conventions it enforces, which questions it asks, and how a generated project is laid out. Each of those decisions was made by a human, and every change an AI produced was reviewed, verified by rendering the template, and, where necessary, rewritten before it was committed. Concretely, AI is used for:

- **Boilerplate** — the configuration files, the workflows, the project scaffolding, and the sample code of the template body.
- **Documentation** — writing and revising the documentation, the read me files, and the comments in the configuration files.
- **Design assets** — drafting the placeholder logo, from which the final design was chosen and refined.
- **Difficult bugs** — tracking down rendering and build problems where a second pair of eyes helps.
- **Research and review** — researching tools and their configuration, and reviewing the template for inconsistencies. The resulting decisions are always made by a human.

Every commit message states whether AI was involved and, if it was, what exactly the AI did. Such commits additionally carry a `Co-Authored-By` trailer for every AI model involved, naming the exact model and version, for example `Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>`, so that the extent of AI involvement, and what produced it, can be traced through the Git history. Commits without such a note were written entirely by hand. See [commit messages](docs/conventions/commit-messages.md).

If you are contributing to the template yourself, see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the AI-assistance rules that apply to contributions.

## Contributing

Bug reports, feature requests, and changes to the template are all welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full process, including how AI-assisted contributions are handled, and [`SECURITY.md`](SECURITY.md) for reporting a vulnerability privately. Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md), and everyone who has contributed is listed in [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

## License

The template repository is licensed under the MIT license (see [`LICENSE`](LICENSE)). That license covers the template itself, not the projects generated from it. A generated project gets the license chosen at render time, from the texts vendored in [`licenses/`](licenses/) — see [licensing](docs/project-template/licensing.md) for where each of those texts comes from and under what terms it is redistributed.
