# Contributing to the C# Library Project Template

Thanks for your interest in contributing. This document covers the process. For the conventions themselves, see the [documentation](docs/README.md), and above all [template structure](docs/project-template/template-structure.md), which explains the split between the root of this repository and the template body every change has to respect.

All participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Security vulnerabilities are handled separately — see [`SECURITY.md`](SECURITY.md) instead of filing a public issue.

## Open an Issue First

Before forking the repository and starting work, open an issue describing what you want to do. This aligns your idea with where the template is already headed, and it can save you from doing work that overlaps with something already planned. A change to the template body reaches every project generated from it, so a new tool, question, or convention is worth discussing before it is built.

## Fork, Branch, and Pull Request

Fork the repository and work on a feature branch. Pull requests are always welcome once the corresponding issue has been discussed. To help the pull request merge quickly:

- **Follow the conventions of the side you change.** Root files follow the [conventions](docs/conventions/README.md) of this repository. Files in the template body follow the generated project's own conventions, plus what the root conventions add about writing them as templates — see [authoring](docs/project-template/authoring.md).
- **Keep the documentation in step.** A new question, file, or convention is not done until the articles that describe it are updated — see the list in [`AGENTS.md`](AGENTS.md#keep-the-documentation-up-to-date), which applies to human contributors just as much.
- **Verify the change by rendering the template**, not only by linting it. Render a project, then run its Release build (see [testing](docs/conventions/testing.md)). A file can be valid as a template and broken once rendered.
- **Run `npm run lint` before opening the pull request.** It checks this repository's own files.
- **Write commit messages by [the template's rules](docs/conventions/commit-messages.md)**, including whether the change affects projects generated from the template.

## Using AI to Contribute

Using AI tools to help write a contribution is fine, but two rules apply, without exception:

- **Disclose it.** Say in the pull request description, and in the commit messages themselves, whether AI was involved and what exactly it did — the same rule that governs every commit to this repository (see [commit messages](docs/conventions/commit-messages.md)). An undisclosed AI contribution is treated as a violation of this policy, not as a neutral omission.
- **Review it yourself, fully, before submitting.** You are responsible for every line of a contribution as if you had written it by hand: you have to understand it, be able to explain and defend it, and have actually rendered the template and run the relevant linters, builds, and tests against it. AI is a tool you use, not a substitute for that responsibility.

A pull request that is raw, unreviewed AI output — one the contributor cannot explain or has not verified — **will be rejected**, disclosed or not. This is not about rejecting AI assistance, it is about rejecting contributions nobody has actually taken responsibility for.

## Update the Template's Records

A pull request that adds a contribution is expected to also update the records that track the template's history:

- **[`CONTRIBUTORS.md`](CONTRIBUTORS.md)** — add yourself, in alphabetical order, if this is your first contribution. You may use your real name or a pseudonym, and you may link to your profile.
- **[`CHANGELOG.md`](CHANGELOG.md)** — document what changed, under the version it will ship in, from the point of view of a consumer deciding whether to run `copier update` (see [versioning](docs/conventions/versioning.md)).
- **[`docs/`](docs/README.md)** — if your change affects how the template is used, rendered, or worked on, update or add the relevant article. A new article goes into the section it belongs to and is listed in the [documentation index](docs/README.md) and in its section's index.

## Licensing of Contributions

The template is licensed under the MIT license (see [`LICENSE`](LICENSE)). By contributing, you agree that your contribution is licensed under the same terms. This is not legal advice — read the [license file](LICENSE) for the actual terms.
