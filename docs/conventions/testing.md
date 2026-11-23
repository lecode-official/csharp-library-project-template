# Testing

This article covers how a change to the template is tested, locally and in continuous integration, and the conventions for the tests the template body ships.

## Rendering Is the Test Suite

The template has no test project of its own. Its test is a render: generate a project from the working tree, then run that project's own linters, build and tests, exactly as a consumer would on day one. [Authoring](../project-template/authoring.md#verifying-a-change) has the commands.

A change is not done until a render of it is green. Build and test the render in Release, as its continuous integration does: the body's static code analysis treats warnings as errors only in Release builds, so a Debug build passes code that every generated project's first pull request would fail on. A render that fails its linters or its tests is a defect in the template, even when the failing file is one the change never touched, because it fails the same way in every project generated from now on.

## Which Renders to Run

One render with the default answers catches most mistakes. A change that touches something an answer feeds needs more than one:

- **A product name with spaces and a dot**, such as `Render.Test Library`. It appears in file names, in `InternalsVisibleTo`, in quoted shell commands in the hooks and the npm scripts, and in the documentation website's title, and it is the answer most likely to break one of them. The same goes for the sample app's name, and for a change to the sample app, render once with a name, a slug, and a namespace of its own too, such as `Render.Test Playground`, `playground-app`, and `RenderTest.Playground`.
- **Every choice of a multiple-choice question the change touches.** A change to `template/LICENSE` or `licenses/` is rendered once per license.
- **Each serviced SDK band**, for a change to `template/global.json` or the workflows. `dotnet_sdk_version` is a free string, so render once with the newest version of each band its help text names (see [questions](../project-template/questions.md#dotnet_sdk_version)).
- **An update, for a structural change.** When a file is moved, renamed or restructured, render a project from the last tag, commit it in its own Git repository, and run `copier update --vcs-ref HEAD` in it against your working tree. The conflicts you see there are the conflicts every consumer will see.
- **The minimum Copier version, for a change that depends on how Copier behaves**, such as a new `_exclude` pattern or a new Copier setting. Render and update once more with the version `_min_copier_version` in [`copier.yml`](../../copier.yml) declares, for example through `uvx --from copier==<version> copier`, and update from the oldest release as well as from the last one. Copier's behavior on an update can depend on what the old release contained: before 9.10.3, an update from v1.0.0 deleted every file the template only creates, while an update from v1.1.0 left them alone.

An update is rendered like this, with the same answers as a fresh render. The template is given by its absolute path, because Copier records it in the project's `.copier-answers.yml`, and `copier update` reads it from there:

```shell
copier copy --defaults --vcs-ref v1.1.0 --data product_name="Render Test" --data root_namespace=RenderTest \
    --data product_description="A scratch render." --data author="Example" \
    --data repository_url=https://example.com/x --data maintainer_url=https://example.com \
    "$PWD" /tmp/update-test

cd /tmp/update-test
git init && git add --all && git commit --message "Rendered v1.1.0"
copier update --defaults --vcs-ref HEAD --conflict inline
git status
```

`git status` then shows what the update changed. None of it may be a file the template only creates (see [rendering and updating](../project-template/rendering-and-updating.md#files-the-template-only-creates)), no file may contain conflict markers, and the project still has to pass its linters and tests.

After every render, check that no placeholder survived, and that none was rendered as a Python list (see [Markdown style](markdown-style.md)):

```shell
grep -rn '\[\[' /tmp/render-test
grep -rnE "\['[^']*'\]\(" /tmp/render-test
```

## Continuous Integration

Two workflows automate the checks above, on every pull request, including one from a fork, and on every push to `main` and `development`. They mirror the generated project's `Linters` and `Tests` workflows: one lints, the other tests. A push to a work branch is checked by its pull request rather than on its own, so that no job has to be skipped to avoid checking a pull request twice: GitHub counts a skipped job as a passed check, which would defeat a required check of the same name (see [branch protection](../development-setup/setting-up-github.md#branch-protection)). Open a draft pull request to have a work branch checked before it is ready.

The [`Linters`](../../.github/workflows/linters.yml) workflow has one job:

- **Lint Template Repository** runs `npm ci` and `npm run lint` on this repository's own files, and fails if `grep -rn 'if false' template/` finds anything.

The [`Tests`](../../.github/workflows/tests.yml) workflow has three jobs:

- **Render** renders the body without `--trust`, once per answer set of its matrix. The answer sets are the default answers, which leave `root_namespace` and `sample_app_namespace` to their derived defaults, a product name and a sample app name with spaces and a dot, `Render.Test Library` and `Render.Test Playground`, with a sample app slug of its own, `playground-app`, its own namespaces, and the `10.0.114` SDK, and one set for each remaining license, so that together they cover every license and both serviced SDK bands, and the default answers once more with the minimum Copier version, the one `_min_copier_version` in [`copier.yml`](../../copier.yml) declares. Each render is checked for surviving placeholders and for link labels rendered as Python lists, then installed with `npm install` and linted, tested with `dotnet test` in Release, and packed with `dotnet pack`. The default answers and the set with spaces and dots also build the documentation website with `properdocs build --strict`, whose API reference is generated from the sample app's build output.
- **Update From the Last Release** renders the last release with the default answers, commits it in a Git repository of its own, and updates it to the current commit with `copier update --defaults --vcs-ref HEAD --conflict inline`, as described above. The last release is the newest `v*` tag that the current commit contains, other than a tag on the current commit itself, so that a run on the commit a release tag points at updates from the release before it. The job fails if the update leaves conflict markers or `.rej` files behind, or changes a file the template only creates, whose paths it reads from the update-only `_exclude` patterns in [`copier.yml`](../../copier.yml). It then runs the same placeholder checks, linters, tests and packaging as the render job. It runs twice, once with the pinned Copier version and once with the minimum version.
- **Tests Passed** fails unless every render and update job succeeded. It sums them up in a single check, so that branch protection requires this one check rather than every job of the two matrices, and a new answer set needs no change to the rulesets.

A third workflow, [`Pull Requests`](../../.github/workflows/pull-requests.yml), has a single job, **Check Source Branch**, which fails a pull request into `main` unless it comes from `development` (see [GitHub workflow](github-workflow.md#pull-requests)). It runs again when a pull request is edited, since changing its base branch is an edit.

A fourth workflow, [`Dependabot Security Updates`](../../.github/workflows/dependabot-security-updates.yml), has a single job, **Retarget Security Update**, which points a pull request that Dependabot opens against `main`, which is what a security update is, at `development`, and gives it the `Dependabot:` label of its ecosystem (see [GitHub workflow](github-workflow.md#dependabot-pull-requests)). It runs on `pull_request_target`, since a workflow Dependabot triggers on `pull_request` gets a read-only token, and so it runs as it is on `main`, with `pull-requests: write` as its only permission. It never checks out or runs the code of the pull request, which is what makes `pull_request_target` safe here: it reads the ecosystem with `dependabot/fetch-metadata`, which also verifies that every commit of the pull request comes from Dependabot, and changes the pull request through the REST API. An ecosystem without a label in its `case` statement still has its pull request pointed at `development`, and then fails the job, so a new ecosystem in `.github/dependabot.yml` gets its label there too.

Copier is installed at the exact version `PINNED_COPIER_VERSION` names, or, for the minimum version, at the version the workflow reads from `_min_copier_version`, so that the tested floor cannot fall behind the declared one (see [dependency management](dependency-management.md#the-roots-own-dependencies)).

The workflows are a safety net, not a substitute for rendering locally. They check only what is pushed, the update job only updates from the last release with the default answers, so it cannot reveal how an update from an older release behaves, and they report a problem only after the change has left your machine. Render and check a change locally before pushing it, as described above.

## Tests in the Body

The tests in `template/tests/unit-tests/` follow the generated project's [testing](../../template/docs/developer-manual/conventions/testing.md) conventions unchanged: one `sealed` test class per source type named `<TypeName>Tests`, in the mirroring namespace and folder, test method names that run the member, the scenario and the outcome together, Arrange-Act-Assert separated by blank lines, and a documentation comment on every member that explains why the scenario matters.

Every type in the body's library has tests, in the same change that adds it. A generated project starts with a passing suite that demonstrates these conventions, and a type without a test would be the first thing it teaches its developers to skip.

The library's placeholder type and its test class are a pair. Change one and the other changes with it, and a consumer replaces both together.

## Related

- [Authoring](../project-template/authoring.md) — the render commands.
- [C# style](csharp-style.md) — the conventions the test code also follows.
- [Questions](../project-template/questions.md) — the answers worth varying between renders.
- [Tooling](../tooling/README.md) — the linters the `Linters` workflow runs on this repository's own files.
- [Testing](../../template/docs/developer-manual/conventions/testing.md) — the generated project's full rule set.
