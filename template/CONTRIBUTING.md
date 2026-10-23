# Contributing to [[ product_name ]]

Thanks for your interest in contributing. This document covers the process. For the coding, documentation, and commit-message conventions themselves, see the [documentation](docs/README.md).

All participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Security vulnerabilities are handled separately — see [`SECURITY.md`](SECURITY.md) instead of filing a public issue.

## Open an Issue First

Before forking the repository and starting work, open an issue describing what you want to do. This aligns your idea with where the project is already headed, and it can save you from doing work that overlaps with something already planned.

## Fork, Branch, and Pull Request

Fork the repository and work on a feature branch. Pull requests are always welcome once the corresponding issue has been discussed. To help the pull request merge quickly:

- **Match the project's conventions** — [C# style](docs/developer-manual/conventions/csharp-style.md) for code, [Markdown style](docs/developer-manual/conventions/markdown-style.md) for documentation, and [file and naming conventions](docs/developer-manual/conventions/file-and-naming-conventions.md) for anything new.
- **Comment and document your code** — see [comments and documentation comments](docs/developer-manual/conventions/comments-and-documentation.md) for what a documentation comment and a plain comment are each expected to cover.
- **Add unit tests for any new feature, in the same pull request.** A bug fix adds a test that reproduces the bug — see [testing](docs/developer-manual/conventions/testing.md) for how tests are structured and named.
- **Raise the version** in the same branch, before opening the pull request, in both the library's project file and `package.json` — see [versioning](docs/developer-manual/conventions/versioning.md).
- **Run the linters, the formatter, and the tests before opening the pull request** (see [tooling](docs/developer-manual/tooling/README.md)).
- **Write commit messages by [the project's rules](docs/developer-manual/conventions/commit-messages.md).**

## Using AI to Contribute

Using AI tools to help write a contribution is fine, but two rules apply, without exception:

- **Disclose it.** Say in the pull request description, and in the commit messages themselves, whether AI was involved and what exactly it did — the same rule that governs every commit to this repository (see [commit messages](docs/developer-manual/conventions/commit-messages.md)). An undisclosed AI contribution is treated as a violation of this policy, not as a neutral omission.
- **Review it yourself, fully, before submitting.** You are responsible for every line of a contribution as if you had written it by hand: you have to understand it, be able to explain and defend it, and have actually run the relevant tests and linters against it. AI is a tool you use, not a substitute for that responsibility.

A pull request that is raw, unreviewed AI output — one the contributor cannot explain or has not verified — **will be rejected**, disclosed or not. This is not about rejecting AI assistance, it is about rejecting contributions nobody has actually taken responsibility for.

## Update the Project's Records

A pull request that adds a contribution is expected to also update the records that track the project's history:

- **[`CONTRIBUTORS.md`](CONTRIBUTORS.md)** — add yourself, in alphabetical order, if this is your first contribution. You may use your real name or a pseudonym. Please link to your profile.
- **[`CHANGELOG.md`](CHANGELOG.md)** — document what changed, under the version it will ship in.
- **[`docs/`](docs/README.md)** — if your change affects how the project is built, used, or contributed to, update or add the relevant article. A new article is listed in the index of its manual ([Developer Manual](docs/developer-manual/README.md) or [User Manual](docs/user-manual/README.md)), and in its section's index where it has one.

## Licensing of Contributions

The project is licensed under `[[ license ]]` (see [`LICENSE`](LICENSE)). By contributing, you agree that your contribution is licensed under the same terms and, if your contribution includes anything you hold a patent on, that you grant the patent rights needed to use it. If your contribution contains anything a third party holds a patent for, you must provide written consent from the patent holder granting the patent rights needed to use it. This is not legal advice — read the [license file](LICENSE) for the actual terms.
