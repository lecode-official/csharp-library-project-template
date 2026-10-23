# C# Library Project Template

A [Copier](https://copier.readthedocs.io/) template for C# library projects. It generates a repository with a full set of conventions documentation, and the linting, formatting, editor and continuous integration setup that goes with them.

## Generating a Project

Install [Copier](https://copier.readthedocs.io/en/stable/#installation), then:

```shell
copier copy gh:lecode-official/csharp-library-project-template my-new-library
```

Copier asks a handful of questions and writes the rendered project into `my-new-library`. Every answer is validated, so an answer that would break the generated project is rejected with a message that says what is allowed. **No `--trust` flag is needed** — this template deliberately uses no tasks, no migrations and no Jinja extensions, so nothing runs on your machine during generation.

Afterwards, in the generated project:

```shell
cd my-new-library
git init
```

See [rendering and updating](docs/project-template/rendering-and-updating.md) for the full walkthrough, and [questions](docs/project-template/questions.md) for what each question means.

## Updating a Project

A project generated from this template records its answers in `.copier-answers.yml`, so it can pull in later template changes:

```shell
copier update
```

Copier re-renders the old and the new version of the template and applies the difference to your working tree, leaving conflicts for you to resolve. Commit your work first — `copier update` requires a clean working tree. Files that every project fills with its own content, such as the read me and the changelog, are created once and never touched by an update (see [rendering and updating](docs/project-template/rendering-and-updating.md#files-the-template-only-creates)).

## How This Template Is Laid Out

This repository is **not** itself a renderable project. It is split in two:

```text
.
├── copier.yml          the questions and the Copier settings
├── README.md           this file — the template's own documentation
├── AGENTS.md           rules for working on the template
├── CONTRIBUTING.md     how to contribute, next to CODE_OF_CONDUCT.md, SECURITY.md, and CONTRIBUTORS.md
├── docs/               how the template works and how to change it
└── template/           ← the template body; only this is ever rendered
```

Everything outside `template/` belongs to the template itself and is never copied into a generated project. That split is the whole point, and [template structure](docs/project-template/template-structure.md) explains what it buys.

## Documentation

The [documentation index](docs/README.md) lists every article. It is split into three sections:

- [Project template](docs/project-template/README.md) — the repository as a Copier template.
  - [Template structure](docs/project-template/template-structure.md) — the two-level layout, and the four problems it solves.
  - [Questions](docs/project-template/questions.md) — every question, what it feeds, and how to add one.
  - [Rendering and updating](docs/project-template/rendering-and-updating.md) — generating a project, and keeping it in step with the template.
  - [Authoring](docs/project-template/authoring.md) — the delimiters, adding a file, and verifying a change.
- [Conventions](docs/conventions/README.md) — how the files on both sides of the split are written, styled, named, committed, and released.
- [Tooling](docs/tooling/README.md) — the formatter, the linters, the editor setup, and the Claude Code hooks used to work on the template.

## Requirements

- **Copier 9.5.0 or newer**, the floor `copier.yml` declares with `_min_copier_version`.

Working on the template's own files needs only Node.js, for the formatter and the linters that check them. Verifying a change to the template body also needs Copier (see [developer setup](docs/tooling/developer-setup.md)).

## Use of AI

This template is developed with the help of AI, and that is disclosed rather than hidden. A project template is mostly boilerplate — configuration files, workflows, scaffolding, and the documentation that explains them — and most of that boilerplate was produced with AI. What was not delegated is every decision about the template: which tools it uses, which conventions it enforces, which questions it asks, and how a generated project is laid out. Each of those decisions was made by a human, and every change an AI produced was reviewed, verified by rendering the template, and, where necessary, rewritten before it was committed. Concretely, AI is used for:

- **Boilerplate** — the configuration files, the workflows, the project scaffolding, and the sample code of the template body.
- **Documentation** — writing and revising the documentation, the read me files, and the comments in the configuration files.
- **Difficult bugs** — tracking down rendering and build problems where a second pair of eyes helps.
- **Research and review** — researching tools and their configuration, and reviewing the template for inconsistencies. The resulting decisions are always made by a human.

Every commit message states whether AI was involved and, if it was, what exactly the AI did. Such commits additionally carry a `Co-Authored-By` trailer for every AI model involved, naming the exact model and version, for example `Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>`, so that the extent of AI involvement, and what produced it, can be traced through the Git history. Commits without such a note were written entirely by hand. See [commit messages](docs/conventions/commit-messages.md).

If you are contributing to the template yourself, see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the AI-assistance rules that apply to contributions.

## Contributing

Bug reports, feature requests, and changes to the template are all welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full process, including how AI-assisted contributions are handled, and [`SECURITY.md`](SECURITY.md) for reporting a vulnerability privately. Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md), and everyone who has contributed is listed in [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

## License

The template repository is licensed under the MIT license (see [`LICENSE`](LICENSE)). That license covers the template itself, not the projects generated from it.
