# AGENTS.md

Guidance for AI assistants working on this Copier template. Humans should read the [documentation](docs/README.md) too.

## What This Project Is

This repository is a [Copier](https://copier.readthedocs.io/) template that generates C# library projects. It is **not** itself a C# project, and it is not a renderable project either — it is split in two:

- **The root** — `copier.yml`, this file, [`README.md`](README.md), the community files ([`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`SECURITY.md`](SECURITY.md), [`CONTRIBUTORS.md`](CONTRIBUTORS.md)), [`docs/`](docs/README.md), [`licenses/`](licenses/), [`scripts/`](scripts/), and the linter configuration that checks *these* files. None of it is ever copied into a generated project.
- **[`template/`](template/)** — the template body. `copier.yml` sets `_subdirectory: template`, so this is the only directory Copier walks.

Start from [docs/project-template/template-structure.md](docs/project-template/template-structure.md). That split is the single most important thing to understand before changing anything here.

## Golden Rules

- **Know which side of the split you are editing.** A change under `template/` changes every project generated from now on. A change at the root changes only this repository. Confusing the two is the mistake to watch for.
- **The delimiters are remapped**: `[[ expression ]]`, `[% block %]`, `[# comment #]`. Plain `{{ }}` is literal text in a template file, which is what lets the GitHub Actions workflows keep their `${{ … }}` expressions unescaped ([docs/project-template/authoring.md](docs/project-template/authoring.md)).
- **Never add an `[% if false %]` block.** It is the workaround this layout exists to remove — documentation about the template belongs at the root, not hidden inside the body. `grep -rn "if false" template/` returning nothing is a check worth keeping.
- **Never introduce an unsafe feature.** `_tasks`, `_migrations` and `_jinja_extensions` all force every consumer to render with `--trust`. The license handling deliberately uses a Jinja `include` instead, precisely to avoid that ([docs/project-template/licensing.md](docs/project-template/licensing.md)). If `copier copy` starts demanding `--trust`, something regressed.
- **Follow the conventions of the side you are on.** Root files follow [docs/conventions/](docs/conventions/README.md). Body files follow the generated project's own conventions to the letter, plus what [docs/conventions/](docs/conventions/README.md) adds about writing them as templates.
- **Verify by rendering, not only by linting.** No linter in this repository checks the body, and no hook fires when you edit it. A file can be valid as a template and broken once rendered ([docs/conventions/testing.md](docs/conventions/testing.md)).
- **Run `npm run lint` before finishing.** It checks this repository's own files, not the body's.
- **Never run a Git command that changes state or history unless asked for that exact thing** — `git commit`, `git push`, `git rebase`, `git reset`, `git tag`, and `git add`/`git restore --staged`/`git mv`/`git rm` alike. Edit the files and stop. Each instruction authorizes only itself, and the staging area is the user's review record ([docs/conventions/git-workflow.md](docs/conventions/git-workflow.md)).
- **Write commit messages by the rules** in [docs/conventions/commit-messages.md](docs/conventions/commit-messages.md), including what any AI involvement actually did and a co-author trailer that names the exact model and version, not just the product.

## When Working on X, Read Y

- **The two-level layout, or anything about how Copier walks this repository** → [docs/project-template/template-structure.md](docs/project-template/template-structure.md).
- **Adding, changing, or removing a question or its validator** → [docs/project-template/questions.md](docs/project-template/questions.md).
- **Anything touching `LICENSE` or `licenses/`** → [docs/project-template/licensing.md](docs/project-template/licensing.md). Check its table before substituting anything into a license text.
- **Adding a file to the body, or verifying a change** → [docs/project-template/authoring.md](docs/project-template/authoring.md) and [docs/conventions/testing.md](docs/conventions/testing.md).
- **What a consumer does with the template, or `_skip_if_exists`** → [docs/project-template/rendering-and-updating.md](docs/project-template/rendering-and-updating.md).
- **Comments, documentation comments, docstrings, or deciding where an explanation belongs** → [docs/conventions/comments-and-documentation.md](docs/conventions/comments-and-documentation.md).
- **Markdown, including placeholders in body Markdown and tables** → [docs/conventions/markdown-style.md](docs/conventions/markdown-style.md).
- **Line length, or a placeholder that changes a line's width** → [docs/conventions/line-length.md](docs/conventions/line-length.md).
- **Naming a file or directory, or putting a placeholder in a path** → [docs/conventions/file-and-naming-conventions.md](docs/conventions/file-and-naming-conventions.md).
- **Writing commit or tag messages** → [docs/conventions/commit-messages.md](docs/conventions/commit-messages.md).
- **Committing, staging, tagging, or anything else touching Git** → [docs/conventions/git-workflow.md](docs/conventions/git-workflow.md).
- **Releasing a template version, or the changelog** → [docs/conventions/versioning.md](docs/conventions/versioning.md).
- **Adding or upgrading a dependency, at the root or in the body** → [docs/conventions/dependency-management.md](docs/conventions/dependency-management.md).
- **Installing what working on the template needs** → [docs/tooling/developer-setup.md](docs/tooling/developer-setup.md).
- **Formatting, linting, spell checking, or the editor setup** → [docs/tooling/](docs/tooling/README.md).
- **The Claude Code hooks** → [docs/tooling/claude-code-hooks.md](docs/tooling/claude-code-hooks.md).

## Keep the Documentation up to Date

**This is important.** A change here is not done until the documentation reflects it:

- A new or changed question, default, or validator updates the tables in [docs/project-template/questions.md](docs/project-template/questions.md), including its validation rule.
- A new or changed `_skip_if_exists` entry updates the list in [docs/project-template/rendering-and-updating.md](docs/project-template/rendering-and-updating.md#files-the-template-only-creates).
- A new license updates the table in [docs/project-template/licensing.md](docs/project-template/licensing.md) **and** `scripts/refresh-licenses.py`.
- A new article under `template/docs/` is listed in two places, both hand-maintained: the generated project's documentation index and its section index.
- A new article at the root goes into the section directory under `docs/` it belongs to, and is listed in [docs/README.md](docs/README.md) and in that section's `README.md`. A new section, and a new article in the project template section, is also listed in [README.md](README.md).
- A changed convention of the generated project updates the matching article under [docs/conventions/](docs/conventions/README.md) too, so that the two rule sets stay the same wherever they can.
- A new route to an article updates the "When Working on X" list above.

Treat the docs as part of the template: a change is not done until they reflect it.
