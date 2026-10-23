# Rendering and Updating

This article covers generating a project from this template and keeping it in step with later template changes.

## Generating a Project

```shell
copier copy gh:lecode-official/csharp-library-project-template my-new-library
```

Copier clones the template, asks the questions in [questions](questions.md), and writes the rendered project into `my-new-library`. Every answer is checked by its question's validator, and an answer that would break the generated project is rejected with a message that says what is allowed.

**No `--trust` is needed.** Copier gates three "unsafe features" behind that flag — tasks, migrations, and Jinja extensions — and this template uses none of them. If `copier copy` ever refuses with `UnsafeTemplateError` and an exit code of 4, one has crept in. That is a change to make deliberately, not to work around with a flag.

To render a specific version rather than the newest tag:

```shell
copier copy --vcs-ref v1.0.0 gh:lecode-official/csharp-library-project-template my-new-library
```

## After Generating

The generated project is complete but not yet a repository:

```shell
cd my-new-library
git init
dotnet restore "source/<Product Name>.slnx"
dotnet test --solution "source/<Product Name>.slnx"
```

`dotnet restore` resolves the pinned dependencies and writes the `packages.lock.json` of every project. [Dependency management](../conventions/dependency-management.md#no-lock-files-in-the-body) explains why the template does not ship them.

**Commit all of the lock files with the first commit.** From then on the project restores in locked mode, which fails without them.

Everything should pass immediately. The library that ships is a placeholder class whose only job is to make that true — replace it, and its test, with the real thing.

## Updating a Project

The generated project's `.copier-answers.yml` records which template and which version it came from, plus every answer. That is what makes an update possible:

```shell
git status          # must be clean
copier update
```

Copier re-renders the template at the old version and at the new one, diffs them, and applies that diff to your working tree — so your own changes survive, and genuine conflicts are left as conflict markers for you to resolve.

Prerequisites, all of which Copier enforces:

- The destination is a Git repository with a **clean** working tree.
- It has a valid `.copier-answers.yml`.
- The template is **tagged**. Copier updates between tags, so an untagged template has no versions to move between.

By default, `copier update` asks every question again, with the recorded answers filled in as the defaults, so pressing Enter keeps an answer and typing a new one changes it. A few flags change that:

- `--defaults` skips the prompts and reuses every recorded answer, falling back to the default for a question the template added since.
- `--skip-answered` skips the questions that already have a recorded answer, and prompts only for the ones the template added since.
- `--data name=value` sets a single answer, overriding the recorded one, as in `copier update --defaults --data license=MIT`.

Each answer, recorded or new, is checked by its question's validator again.

## What an Update Will and Will Not Do

It applies the *difference between two template versions*. So a template change that adds a file gives you that file, and a template change that edits a line you also edited gives you a conflict.

It does not re-render files that the template did not change, and it does not remove files you added. It also cannot reconcile a change you made to a file the template later restructured — that is an ordinary merge conflict, resolved the ordinary way.

It leaves a file you deleted deleted, even when the template changed that file, with the exception of the files below.

## Files the Template Only Creates

Some files every project keeps, but fills with its own content. The template only provides a starting point for them, so `_skip_if_exists` in [`copier.yml`](../../copier.yml) lists them:

- `README.md`, `CHANGELOG.md` and `CONTRIBUTORS.md` at the root of the project.
- `docs/user-manual/getting-started.md`.
- The `README.md` of each project directory under `source/`, the library's and the sample app's.
- `source/sample-app/Program.cs`.

Copier creates a listed file when the project is generated, and never touches it again in an update. A template change to one of them can neither conflict with the project's own content nor bring back a placeholder the project has long replaced.

The catch is deletion. When a listed file does not exist, Copier creates it, and it does so on every update, so a project that deletes a listed file gets it back with the next `copier update`. Without an entry, an update leaves a deletion alone. That is why only files a project keeps belong in the list, and why the placeholder `Greeter` class and its `GreeterTests` are deliberately absent from it: a project deletes them when it replaces them with the real thing, and an entry would bring them back on every update.

A consumer who does want a template change to a listed file can still pull it in by hand. Render a fresh project at the new version with the project's own answers, outside the project, and compare the file with the project's copy:

```shell
copier copy --defaults --vcs-ref v1.1.0 --data-file .copier-answers.yml gh:lecode-official/csharp-library-project-template /tmp/fresh
diff /tmp/fresh/README.md README.md
```

Then carry over whatever is worth keeping.

## Releasing a Template Version

Because `copier update` moves between tags, a template change is only available to consumers once it is tagged:

```shell
git tag -a v1.1.0 -F <message-file>
git push origin v1.1.0
```

Use semantic versioning against the *generated project's* surface: a renamed or removed question, or a restructured layout that an update cannot reconcile cleanly, is a major change. A new optional question with a default is minor. A documentation or wording fix is a patch. [Versioning](../conventions/versioning.md) covers the version number, the changelog and the tag message in full.

## Related

- [Questions](questions.md) — what Copier asks, what each answer feeds, and how it is validated.
- [Template structure](template-structure.md) — why the answers file lives inside the body.
- [Authoring](authoring.md) — making and verifying a template change.
- [Versioning](../conventions/versioning.md) — releasing a template version.
