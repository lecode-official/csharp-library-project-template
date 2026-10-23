# Tooling

This section covers the tools used to work on the template: the formatter, the linters, the editor setup, and the Claude Code hooks. Each article covers the tool as this repository configures it for its own files, and how the same tool reaches the template body.

1. [Developer Setup](developer-setup.md)
2. [Visual Studio Code Integration](editor-integration.md)
3. [Code Formatting (dprint)](formatting-dprint.md)
4. [Markdown Linting (MarkdownLint)](linting-markdownlint.md)
5. [Spell Checking (CSpell)](spell-checking-cspell.md)
6. [Claude Code Hooks](claude-code-hooks.md)

## Two Configurations for Every Tool

Every tool here exists twice, once for each side of the [split](../project-template/template-structure.md):

- **The root's configuration** checks the template's own files, though not every tool checks all of them. dprint formats and checks every Markdown, JSON, YAML and TOML file, the configuration files themselves included. MarkdownLint checks the Markdown: the articles under `docs/`, `README.md`, `AGENTS.md` and `CHANGELOG.md`. CSpell checks only the Markdown, `copier.yml` and the scripts. The configuration lives at the root: [`dprint.json`](../../dprint.json), [`.markdownlint.yml`](../../.markdownlint.yml) and [`.cspell.json`](../../.cspell.json).
- **The body's configuration** is a template file like any other. It checks the generated project, and only ever runs in a render. It lives where the generated project expects it, at the root of the body: `template/dprint.json`, `template/.cspell.json`, `template/.markdownlint.yml`, and `template/.globalconfig`.

Every root configuration excludes `template/`, because the files in it are Jinja templates rather than valid documents of their own type, and `licenses/`, because those texts are verbatim copies that must never be touched. So no tool in this repository checks the body. A render does (see [testing](../conventions/testing.md)).

Formatting and linting are kept separate on both sides: **dprint owns all formatting, and the linters only check quality.** No lint rule that would reformat a file is ever enabled.

## How to Run

```shell
npm run format     # format the root's files with dprint
npm run lint       # dprint check, then MarkdownLint, then CSpell
```

Each tool also has its own script, `lint:dprint`, `lint:markdownlint` and `lint:cspell`. `npm run lint` runs them with `run-s --continue-on-error`, from the `npm-run-all2` package, rather than joining them with `&&`. So every tool runs even after one of them fails, a single run reports everything that is wrong, and the command still exits with an error if any of them failed. Joining them with `;` would do neither reliably. A shell returns only the last command's exit code, so a dprint or MarkdownLint failure would go unreported, and `cmd.exe`, which npm uses on Windows, does not treat `;` as a separator at all.

## Continuous Integration

The [`Template`](../../.github/workflows/template.yml) workflow runs `npm run lint` on every push and pull request, checks that no `[% if false %]` block crept into the body, and renders the body with several answer sets to run each generated project's own checks. [Testing](../conventions/testing.md#continuous-integration) covers it in full. It does not replace running `npm run lint` and rendering a change locally before pushing it, which is still where a change is verified first.

## Related

- [Conventions](../conventions/README.md) — what the tools and the reviewers enforce.
- [Testing](../conventions/testing.md) — rendering a change, and the continuous integration that does it on every push.
- [Tooling](../../template/docs/developer-manual/tooling/README.md) — the generated project's tooling, which the body configures.
