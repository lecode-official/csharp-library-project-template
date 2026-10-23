# AGENTS.md

Guidance for AI assistants working on [[ product_name ]]. Humans should read the [documentation](docs/README.md) too.

## What This Project Is

[[ product_description ]]

The repository holds one solution, [`source/[[ product_name ]].slnx`](source/), with three projects — the library itself (`[[ library_slug ]]`), a sample app that references it (`sample-app`), and its xUnit test project (`tests/unit-tests`). All three target `[[ target_framework ]]` with nullable reference types and implicit usings enabled.

Start from [docs/developer-manual/architecture.md](docs/developer-manual/architecture.md).

## Golden Rules

- **Match the surrounding code and the documented conventions** ([docs/developer-manual/conventions/](docs/developer-manual/conventions/README.md)). This code is heavily and consistently documented — follow it.
- **Formatting is owned by dprint** ([docs/developer-manual/tooling/formatting-dprint.md](docs/developer-manual/tooling/formatting-dprint.md)), which covers C#, XML (including `.csproj` and `.slnx`), Markdown, JSON, YAML, and TOML. Run `npm run format` before finishing. The Roslyn plugin drives whitespace only. The structural conventions below are checked by the analyzers instead.
- **Run `npm run lint` and `npm test` before finishing.** The docs and this file are Markdown and are linted too.
- **The build runs strict static code analysis** — the .NET SDK analyzers, StyleCop Analyzers, Roslynator, and Nullable.Extended, configured in [`.globalconfig`](.globalconfig) — and a Release build fails on any warning. Fix a finding rather than suppressing it, and never turn a rule off without a comment saying why ([docs/developer-manual/tooling/static-code-analysis.md](docs/developer-manual/tooling/static-code-analysis.md)).
- **C# structure**: file-scoped namespaces, `#region` blocks on every type in the documented order, an XML documentation comment on **every member, including `private` ones**, `<inheritdoc/>` where a member implements or overrides, `sealed` classes by default, explicit `this.` on member access, expression-bodied members where the implementation is a single expression, and `camelCase` private fields with no underscore. Full detail: [C# style](docs/developer-manual/conventions/csharp-style.md).
- **Nullable reference types and implicit usings are enabled everywhere.** Write genuinely null-safe code rather than silencing the analyzer with `!`. A `!` that is genuinely needed carries a `// !` justification comment, or the build fails ([C# style](docs/developer-manual/conventions/csharp-style.md#nullability-and-implicit-usings)).
- **Markdown headings are title case** at every level, in every file ([docs/developer-manual/conventions/markdown-style.md](docs/developer-manual/conventions/markdown-style.md)). Preserve the real casing of code spans, brand names (`dprint`), and acronyms.
- **Wrap code in backticks** in prose everywhere — the docs, this file, and commit messages. XML documentation comments are the one exception: they are XML, not Markdown, so use `<see cref="..."/>` for identifiers and `<c>` for code instead.
- **Prose uses periods, not semicolons.** In prose — the docs, XML documentation comments, this file — end each sentence with a period rather than joining two with a semicolon. Plain `//` comments do the reverse: sentences are separated by semicolons and the last one takes no terminal punctuation.
- **No line exceeds 150 characters, and none stops short of it either** — comments, documentation comments, and split string literals are filled up to the limit and broken only when the next word does not fit ([docs/developer-manual/conventions/line-length.md](docs/developer-manual/conventions/line-length.md)). Markdown is exempt: never hard-wrap prose.
- **Files and directories are kebab-case**, except well-known and tool-mandated names. Inside a C# project's own source tree they switch to PascalCase, one type per file. The project and solution files are named after the product, spaces included ([docs/developer-manual/conventions/file-and-naming-conventions.md](docs/developer-manual/conventions/file-and-naming-conventions.md)).
- **Every dependency is pinned to an exact version — never a range.** Package versions live in `Directory.Packages.props` (Central Package Management), never in a project file. Every project sets `RestorePackagesWithLockFile`, so a package change must be followed by `dotnet restore` and the resulting `packages.lock.json` files committed alongside it ([docs/developer-manual/conventions/dependency-management.md](docs/developer-manual/conventions/dependency-management.md)).
- **Every new feature is unit tested, in the same change.** A bug fix adds a test that reproduces the bug. Test classes mirror the source namespace and folder and are named `<TypeName>Tests`. `internal` types are tested directly through `InternalsVisibleTo`. Run `npm test` before finishing ([docs/developer-manual/conventions/testing.md](docs/developer-manual/conventions/testing.md)).
- **Raise the version before opening a pull request**, in the library's `<Version>` property and the `"version"` field of `package.json` together, and add the release to `CHANGELOG.md` ([docs/developer-manual/conventions/versioning.md](docs/developer-manual/conventions/versioning.md)).
- **Write commit messages by the rules** ([docs/developer-manual/conventions/commit-messages.md](docs/developer-manual/conventions/commit-messages.md)) — the 50/72 rule, a title-cased, past-tense subject, and a prose body. State whether AI was involved and, if it was, what exactly the AI did. When you did any of the work, add a co-author trailer with your tool's no-reply address that names the exact model and version you are, not just the product, for example:

  ```text
  Co-Authored-By: Claude Opus 5.5 Medium <noreply@anthropic.com>
  ```

- **Never run a Git command that changes state or history unless asked for that exact thing** — `git commit`, `git push`, `git tag`, `git rebase`, `git reset`, `git cherry-pick`, and `git add`/`git restore --staged` alike. Edit the files and stop. Each instruction authorizes only itself: "write a commit message" means write it and stop, so the user can review it before anything is committed, and "commit this" does not authorize a push ([docs/developer-manual/conventions/git-workflow.md](docs/developer-manual/conventions/git-workflow.md)).
- **The staging area is the user's review record**, not a step on the way to a commit. Staging or unstaging on their behalf destroys it.

## When Working on X, Read Y

- **Repository layout, the solution, the projects** → [docs/developer-manual/architecture.md](docs/developer-manual/architecture.md).
- **C# source code** → [docs/developer-manual/conventions/csharp-style.md](docs/developer-manual/conventions/csharp-style.md) and [comments and documentation comments](docs/developer-manual/conventions/comments-and-documentation.md).
- **Installing the SDK, Node.js, or the editor** → [docs/developer-manual/tooling/developer-setup.md](docs/developer-manual/tooling/developer-setup.md).
- **Linting, formatting, spell checking, editor setup** → [docs/developer-manual/tooling/](docs/developer-manual/tooling/README.md).
- **An analyzer finding, or changing a rule's severity** → [docs/developer-manual/tooling/static-code-analysis.md](docs/developer-manual/tooling/static-code-analysis.md).
- **The GitHub Actions workflows, a failing check, or Dependabot** → [docs/developer-manual/tooling/continuous-integration.md](docs/developer-manual/tooling/continuous-integration.md).
- **The documentation website, its navigation, or the generated API reference** → [docs/developer-manual/tooling/documentation-website.md](docs/developer-manual/tooling/documentation-website.md).
- **Markdown and documentation style** → [docs/developer-manual/conventions/markdown-style.md](docs/developer-manual/conventions/markdown-style.md).
- **Line length, or filling a comment or a split string literal to the limit** → [docs/developer-manual/conventions/line-length.md](docs/developer-manual/conventions/line-length.md).
- **Naming a new file or directory** → [docs/developer-manual/conventions/file-and-naming-conventions.md](docs/developer-manual/conventions/file-and-naming-conventions.md).
- **Adding or upgrading a dependency** → [docs/developer-manual/conventions/dependency-management.md](docs/developer-manual/conventions/dependency-management.md).
- **Writing or running unit tests, measuring code coverage** → [docs/developer-manual/conventions/testing.md](docs/developer-manual/conventions/testing.md) and [testing and code coverage](docs/developer-manual/tooling/testing-and-code-coverage.md).
- **Writing commit messages** → [docs/developer-manual/conventions/commit-messages.md](docs/developer-manual/conventions/commit-messages.md).
- **Releasing, or raising the version** → [docs/developer-manual/conventions/versioning.md](docs/developer-manual/conventions/versioning.md).
- **Committing, pushing, rebasing, or anything else touching Git** → [docs/developer-manual/conventions/git-workflow.md](docs/developer-manual/conventions/git-workflow.md).
- **A formatting-only commit, or `.git-blame-ignore-revs`** → [docs/developer-manual/conventions/git-blame.md](docs/developer-manual/conventions/git-blame.md).
- **Opening an issue, submitting a pull request, the AI-contribution policy** → [CONTRIBUTING.md](CONTRIBUTING.md).
- **How consumers use the library** → [docs/user-manual/](docs/user-manual/README.md), starting with [getting started](docs/user-manual/getting-started.md).

## Conventions in Brief

Files use file-scoped namespaces and always group members into `#region` blocks (`Constructors`, `Private Fields`, `Public Methods`, and so on), even in small files, ordered constructors, constants, fields, properties, methods, then interface implementations — with no access modifier in an interface-implementation region's name. Every member, including `private` ones, is documented with XML comments that explain *why*, not just what, and marks up keywords like `null` or `sealed` with `<see langword="..."/>`. Sealed types compose the framework types they wrap instead of inheriting from them. Markdown headings are title case everywhere, and prose ends sentences with periods. Plain code comments do the reverse. Full detail: [docs/developer-manual/conventions/](docs/developer-manual/conventions/README.md).

## Keep the Documentation up to Date

**This is important.** Whenever you change, add, remove, or discover something about the project, update the relevant [`docs/`](docs/README.md) article **and** this `AGENTS.md` in the same change:

- Keep the "When Working on X" routing table above accurate.
- Keep the indexes accurate — every article must be listed. An article is listed in the index of its manual, the [Developer Manual index](docs/developer-manual/README.md) or the [User Manual index](docs/user-manual/README.md), and an article in the tooling or conventions section also in that section's index, [tooling](docs/developer-manual/tooling/README.md) or [conventions](docs/developer-manual/conventions/README.md). The [documentation index](docs/README.md) lists only the two manuals.
- Keep the `nav` list in [`properdocs.yml`](properdocs.yml) accurate, since the published website's navigation comes from it rather than from the indexes.
- A change to the public API updates the User Manual (how consumers use it), not only the Developer Manual (how the codebase itself is built) — the two serve different audiences, and the same change often needs a separate edit to each.
- If a change introduces a topic that does not fit an existing article, add a new small, single-topic article, link it from the relevant index, and reference it here if relevant.
- If a change invalidates something a doc says, fix the doc — do not leave it stale.

Treat the docs as part of the code: a change is not done until the docs and this file reflect it.
