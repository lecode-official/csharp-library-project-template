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

The generated project is complete, but it is not a Git repository yet, and it has no lock files. Copier's message after generating it lists the steps that have to happen before the first commit:

```shell
cd my-new-library
git init --initial-branch=main
npm install
dotnet restore "source/<Product Name>.slnx"
```

This is the one time `npm install` is right in a generated project. The template ships no `package-lock.json`, so `npm ci` has nothing to install from yet, and `npm install` resolves the pinned dependencies and writes the lock file. `dotnet restore` does the same for the `packages.lock.json` of every project. [Dependency management](../conventions/dependency-management.md#no-lock-files-in-the-body) explains why the template does not ship them. **Commit all of the lock files with the first commit**, since the project's continuous integration fails without them.

Everything else is described in the generated project's own [first steps](../../template/docs/developer-manual/first-steps.md), which the message points to: publishing the project on GitHub and setting up its labels, its repository settings, and GitHub Pages, setting up Visual Studio Code, replacing the placeholder library and logo, and deciding on the documentation website. The steps live in the project, rather than in this article, so that they stay readable there after the terminal is closed.

## Updating a Project

The generated project's `.copier-answers.yml` records which template and which version it came from, plus every answer. That is what makes an update possible:

```shell
git status          # must be clean
copier update
```

Copier re-renders the template at the old version and at the new one, diffs them, and applies that diff to your working tree — so your own changes survive, and genuine conflicts are left as conflict markers for you to resolve.

Copier's message after the update lists what to do by hand: the steps every update needs, and a short hint for every release that changed something an update cannot carry over on its own, such as a file the template only creates. The [migration guide](migration-guide.md) covers each of these hints in detail, release by release.

Prerequisites, all of which Copier enforces:

- The destination is a Git repository with a **clean** working tree.
- It has a valid `.copier-answers.yml`.
- The template is **tagged**. Copier updates between tags, so an untagged template has no versions to move between.

By default, `copier update` asks every question again, with the recorded answers filled in as the defaults, so pressing Enter keeps an answer and typing a new one changes it. A few flags change that:

- `--defaults` skips the prompts and reuses every recorded answer, falling back to the default for a question the template added since.
- `--skip-answered` skips the questions that already have a recorded answer, and prompts only for the ones the template added since.
- `--data name=value` sets a single answer, overriding the recorded one, as in `copier update --defaults --data license=MIT`.

Each answer, recorded or new, is checked by its question's validator again.

## The Messages

Both messages are set in [`copier.yml`](../../copier.yml), as `_message_after_copy` and `_message_after_update`. They are rendered like any template file, so they can use the answers, and they are no unsafe feature, so they need no `--trust`. `copier copy --quiet` suppresses them.

A message cannot tell which release a project is updated from. No variable holds it outside of migrations, and migrations would need `--trust`. So every hint in the update message is worded for a project that updates from before the release that introduced it, as in "When updating from a version before v1.1.0", and the hints are kept newest first, so that a project that skipped releases sees every one that applies to it.

### Writing the Update Message

A change has to be carried over by hand whenever an update cannot apply it: a change to one of the [files the template only creates](#files-the-template-only-creates), or anything outside the files, such as a new label on GitHub. Such a change updates the message and the migration guide in the same change as the work itself:

1. **Find the block of the release** in `_message_after_update` in [`copier.yml`](../../copier.yml), headed `When updating from a version before vX.Y.Z:` with the version the change will ship in. If it does not exist yet, add it above the blocks of the earlier releases, so that the newest one comes first.
2. **Add a hint** to that block: one bullet that names the file or the place, and says in a few words what to do, as in `README.md: replace the title line`. A hint is a reminder, not the instructions, and the message has no room for code.
3. **Add the instructions** to the release's section of the [migration guide](migration-guide.md), `Migrate from vX.Y.Z to vX.Y.Z` with the previous and the upcoming release, and add the section first if it does not exist yet. Say what changed, why, and exactly how to carry it over, with the new content where it fits, such as a changed line, a command, or the file to copy from a fresh render.
4. **Mention it in the changelog entry** of the change (see [changelog](../conventions/changelog-entries.md#writing-the-entries)).

A change to the placeholder logo is the case that is easiest to miss, since nothing conflicts and nothing fails. A project that replaced the logo does not want the change, but a project that still uses the placeholder does, so the hint and the instructions are worded for the latter, as in `If the project still uses the placeholder logo, copy docs/assets/images/ from a fresh render.` The same goes for the colors in `brand-colors.css` and for the logo design article.

## What an Update Will and Will Not Do

It applies the *difference between two template versions*. So a template change that adds a file gives you that file, and a template change that edits a line you also edited gives you a conflict.

It does not re-render files that the template did not change, and it does not remove files you added. It also cannot reconcile a change you made to a file the template later restructured — that is an ordinary merge conflict, resolved the ordinary way.

It leaves a file you deleted deleted, even when the template changed that file.

## Files the Template Only Creates

Some files every project fills with its own content. The template only provides a starting point for them:

- `README.md`, `CHANGELOG.md` and `CONTRIBUTORS.md` at the root of the project.
- `docs/user-manual/README.md` and `docs/user-manual/getting-started.md`, the index of the User Manual and its first article.
- The `README.md` of each project directory under `source/`, the library's and the sample app's.
- `source/sample-app/Program.cs`.
- The logo: its vector masters and their read me in `design/`, its copies, the favicon, and the package icon in `docs/assets/favicon/` and `docs/assets/images/`, its colors in `docs/assets/styles/brand-colors.css`, and `docs/developer-manual/logo-design.md`, which describes it.

Copier creates them when the project is generated, like any other file. An update then never touches them: it neither changes them nor creates them again, and it does not add a new file under one of the directories either. So a template change can neither conflict with the project's own content nor bring back a placeholder the project has replaced, renamed, or deleted. A project that bakes its logo to PNG, for example, deletes the SVG copies of the placeholder for good (see the generated project's [logo design](../../template/docs/developer-manual/logo-design.md#replacing-the-placeholder)).

The files are excluded from every update by `_exclude` patterns in [`copier.yml`](../../copier.yml) that only apply when `_copier_operation` is `update`, which is why the template needs Copier 9.6.0 or newer. The update job of the template's continuous integration reads these patterns and fails if an update changes one of the files (see [testing](../conventions/testing.md#continuous-integration)), so each of them keeps the form `"[% if _copier_operation == 'update' %]/README.md[% endif %]"`, on a line of its own, with the anchored path between the two tags. `_skip_if_exists` is not used, because it creates a listed file again on every update once a project has deleted it, which would leave a project no way to drop a read me or a placeholder it does not want.

The placeholder `Greeter` class and its `GreeterTests` are deliberately not excluded. A project replaces them, but one that keeps them for a while still needs the template's changes to them, such as a fix for a new analyzer rule, and one that deleted them is not affected, since an update leaves a deletion alone.

The catch is that a template change to one of these files never reaches a project on its own, not even one that still uses the placeholder. Such a change needs a hint in the update message and a step in the [migration guide](migration-guide.md) (see [writing the update message](#writing-the-update-message)). A consumer can also pull a change in by hand: render a fresh project at the new version with the project's own answers, outside the project, and compare the file with the project's copy:

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

Use semantic versioning against the *generated project's* surface: a renamed or removed question, or a restructured layout that an update cannot reconcile cleanly, is a major change. A new optional question with a default is minor. A documentation or wording fix is a patch. [Versioning](../conventions/versioning.md) covers the version number and the tag message in full, and [changelog](../conventions/changelog-entries.md) covers the release's entry. A release that a generated project has to follow up by hand also has its hints in the update message and its section in the [migration guide](migration-guide.md) (see [the messages](#the-messages)).

## Related

- [Questions](questions.md) — what Copier asks, what each answer feeds, and how it is validated.
- [Template structure](template-structure.md) — why the answers file lives inside the body.
- [Migration guide](migration-guide.md) — what a project does by hand when it updates.
- [Authoring](authoring.md) — making and verifying a template change.
- [Versioning](../conventions/versioning.md) — releasing a template version.
