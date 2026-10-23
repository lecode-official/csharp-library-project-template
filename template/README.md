# [[ product_name ]]

[[ product_description ]]

## Project Structure

The repository is organized into a few top-level directories:

- **[`docs/`](docs/README.md)** — the project documentation. Start with [`docs/README.md`](docs/README.md).

## Use of AI

This project is developed with the help of AI, and that is disclosed rather than hidden. The heart of the project — its architecture, its public API, and the implementation of its core — is written by hand. AI is a tool used for the work around that core, never a substitute for it, and everything an AI produces is reviewed and, where necessary, rewritten before it is committed. Concretely, AI is used for:

- **Documentation** — writing and revising the documentation, the read me files, and code comments.
- **Design assets** — generating logo designs and other visual assets.
- **Boilerplate** — generating repetitive, mechanical code, project scaffolding, and configuration files.
- **Difficult bugs** — tracking down bugs where a second pair of eyes helps.
- **Architecture** — discussing design and architecture decisions as a sounding board. The decisions themselves are always made by a human.

Every commit message states whether AI was involved and, if it was, what exactly the AI did. Such commits additionally carry a `Co-Authored-By` trailer for every AI model involved, naming the exact model and version, for example `Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>`, so that the extent of AI involvement, and what produced it, can be traced through the Git history. Commits without such a note were written entirely by hand. See [commit messages](docs/developer-manual/conventions/commit-messages.md).

If you are contributing to the project yourself, see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the AI-assistance rules that apply to contributions.

## Contributing

If you would like to contribute, there are multiple ways to help out — bug reports, feature requests, or code. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full process, including how AI-assisted contributions are handled. Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

To report a security vulnerability, please do not open a public issue — see [`SECURITY.md`](SECURITY.md) for how to report it privately.

## License

[[ product_name ]] is licensed under `[[ license ]]`. The full text is in [`LICENSE`](LICENSE). **This is no legal advice and you should read the [license file](LICENSE) for more information.**
