# [[ product_name ]]

[[ product_description ]]

## Project Structure

The repository is organized into a few top-level directories:

- **[`source/`](source/)** — the source code of [[ product_name ]] itself, and the sample app that demonstrates it.
- **[`tests/`](tests/)** — the unit tests.
- **[`docs/`](docs/README.md)** — the project documentation. Start with [`docs/README.md`](docs/README.md).

The solution, [`source/[[ product_name ]].slnx`](source/), groups three projects: the library, a runnable sample app that references it, and the xUnit test project under `tests/`.

## Installation

[[ product_name ]] is published on NuGet as `[[ package_id ]]`:

```shell
dotnet add package [[ package_id ]]
```

See the [User Manual](docs/user-manual/README.md) for how to use it.

## Development

### Developer Setup

Building and working on [[ product_name ]] requires the .NET SDK — the exact version pinned in [`global.json`](global.json) — and Node.js with npm, which is used to run the linters and the code formatter.

```shell
git clone [[ repository_url ]]
cd [[ product_slug ]]
npm ci
dotnet restore "source/[[ product_name ]].slnx"
```

Use `npm ci` rather than `npm install` for a fresh clone, so that the exact locked versions are installed. See [developer setup](docs/developer-manual/tooling/developer-setup.md) for the full walkthrough, including the Python toolchain the documentation website needs.

### Building

```shell
npm run build
```

The build settings every project shares, including the static code analysis, live in the root `Directory.Build.props`. Build output does not land next to the source: two more `Directory.Build.props` files redirect every project's `bin` and `obj` into `build/<project folder name>/` instead. See [architecture](docs/developer-manual/architecture.md).

### Running

```shell
npm start
```

runs the sample app, which demonstrates the library.

### Testing

The library's behavior is verified by an xUnit test project, [`tests/unit-tests`](tests/unit-tests/). Every new feature is expected to come with unit tests covering it, in the same pull request (see [`CONTRIBUTING.md`](CONTRIBUTING.md)).

```shell
npm test
```

See [testing and code coverage](docs/developer-manual/tooling/testing-and-code-coverage.md) for how coverage is collected and reported.

### Dependencies

Every dependency is pinned to an exact version — NuGet packages, the dprint plugins, the linters, the .NET SDK itself, and the Python packages that build the documentation website. NuGet package versions are declared once, in `Directory.Packages.props`, and every project sets `RestorePackagesWithLockFile`, so a package change is followed by `dotnet restore` and the resulting `packages.lock.json` files are committed alongside it. See [dependency management](docs/developer-manual/conventions/dependency-management.md).

### Code Formatting & Linting

The project separates *formatting* from *linting*: a single formatter, [dprint](https://dprint.dev), owns all code formatting, while the linters only check for quality issues. This split is deliberate — no lint rule that would reformat code is ever added.

#### Formatting

[dprint](https://dprint.dev) is configured in [`dprint.json`](dprint.json) and formats C#, XML (including `.csproj` and `.slnx`), Markdown, JSON, YAML, and TOML. Run it with:

```shell
# Formats the entire code base
npm run format
```

#### Linting

The linter configuration lives at the repository root, where each tool discovers it on its own:

- **MarkdownLint** ([`.markdownlint.yml`](.markdownlint.yml)) — lints the Markdown files across the repository, including this read me.
- **CSpell** ([`.cspell.json`](.cspell.json)) — checks the spelling of code, comments, and documentation.
- **The static code analyzers** ([`.globalconfig`](.globalconfig)) — check the C# code on every build.

```shell
# Runs the code formatter in check mode and every linter
npm run lint

# Runs a single linter
npm run lint:dprint
npm run lint:markdownlint
npm run lint:cspell
```

`npm run lint` runs its steps with `run-s --continue-on-error`, so one failing linter does not hide the findings of the others, and the command still fails when any of them does.

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

[[ product_name ]] is licensed under `[[ license ]]`. The full text is in [`LICENSE`](LICENSE), and the library's project file declares the same identifier as its `PackageLicenseExpression`, which is what NuGet publishes. **This is no legal advice and you should read the [license file](LICENSE) for more information.**
