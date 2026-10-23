# Tooling

This section gives an overview of the tools used for development, including code editors, linters, and the code formatter:

1. [Developer Setup](developer-setup.md)
2. [Code Formatting (dprint)](formatting-dprint.md)
3. [Markdown Linting (MarkdownLint)](linting-markdownlint.md)
4. [Spell Checking (CSpell)](spell-checking-cspell.md)
5. [Testing and Code Coverage](testing-and-code-coverage.md)

Formatting and linting are kept strictly separate: **one formatter owns all formatting, and the linters only check quality.** No lint rule that would reformat code is ever added.

## The Tools

- **Formatting:** [dprint](formatting-dprint.md), which covers C#, XML (including `.csproj` and `.slnx`), Markdown, JSON, YAML, and TOML.
- **Linting:** [MarkdownLint](linting-markdownlint.md) for the documentation, and [CSpell](spell-checking-cspell.md) for spelling across the whole repository.
- **Compiling and testing:** the .NET SDK itself. There is no separate type-check step, because the compiler *is* the type check — `dotnet build` and `dotnet test` are what catch a type error (see [testing and code coverage](testing-and-code-coverage.md)).

## Where the Configuration Lives

Every linter and formatter configuration lives at the repository root, where each tool discovers it on its own, so no script, hook, or editor setting has to point a tool at its configuration:

- [`.cspell.json`](../../../.cspell.json)
- [`.markdownlint.yml`](../../../.markdownlint.yml)
- [`dprint.json`](../../../dprint.json)

dprint has no choice anyway: it rejects its own `incremental` setting inside an extended configuration.

## How to Run

```shell
npm run format     # format the whole repository with dprint
npm run lint       # dprint check, then MarkdownLint, then CSpell
npm run build      # build the solution
npm test           # run the unit tests
npm start          # run the sample app
```

Each check also has its own script: `lint:dprint`, `lint:markdownlint`, and `lint:cspell`. The npm scripts are thin wrappers so that a single command works the same on every developer's machine. The underlying `dotnet` and `npx` invocations are equally fine to run directly.

## Why the Aggregate Uses `run-s --continue-on-error`

`npm run lint` runs its three scripts through `run-s --continue-on-error`, from the `npm-run-all2` package, rather than joining them with `&&`, so every check runs even after one of them fails. A single run therefore reports everything that is wrong, instead of stopping at the first tool with a finding, and it still exits with an error if any of them failed. Joining the scripts with `;` would run them all too, but `;` does not work in the Windows command shell that npm uses there, and the exit code would only be that of the last script.

## The Docs Are Linted Too

This `docs/` tree is Markdown, so MarkdownLint and CSpell check it and dprint formats it. `README.md` and `AGENTS.md` are covered the same way. Keep every article passing all three.

## Related

- [Conventions](../conventions/README.md) — what the linters and reviewers enforce.
- [Architecture](../architecture.md) — the projects these tools run against.
