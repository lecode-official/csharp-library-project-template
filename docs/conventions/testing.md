# Testing

This article covers how a change to the template is tested, locally and in continuous integration, and the conventions for the tests the template body ships.

## Rendering Is the Test Suite

The template has no test project of its own. Its test is a render: generate a project from the working tree, then run that project's own linters, build and tests, exactly as a consumer would on day one. [Authoring](../project-template/authoring.md#verifying-a-change) has the commands.

A change is not done until a render of it is green. Build and test the render in Release, as its continuous integration does: the body's static code analysis treats warnings as errors only in Release builds, so a Debug build passes code that every generated project's first pull request would fail on. A render that fails its linters or its tests is a defect in the template, even when the failing file is one the change never touched, because it fails the same way in every project generated from now on.

## Which Renders to Run

One render with the default answers catches most mistakes. A change that touches something an answer feeds needs more than one:

- **A product name with spaces and a dot**, such as `Render.Test Library`. It appears in file names, in `InternalsVisibleTo`, in quoted shell commands in the hooks and the npm scripts, and in the documentation website's title, and it is the answer most likely to break one of them.
- **Every choice of a multiple-choice question the change touches.** A change to `template/LICENSE` or `licenses/` is rendered once per license.
- **Each serviced SDK band**, for a change to `template/global.json` or the workflows. `dotnet_sdk_version` is a free string, so render once with the newest version of each band its help text names (see [questions](../project-template/questions.md#dotnet_sdk_version)).
- **An update, for a structural change.** When a file is moved, renamed or restructured, render a project from the last tag, commit it in its own Git repository, and run `copier update --vcs-ref HEAD` in it against your working tree. The conflicts you see there are the conflicts every consumer will see.

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

Two workflows automate the checks above on every push to any branch and on every pull request, including one from a fork. They mirror the generated project's `Linters` and `Tests` workflows: one lints, the other tests.

The [`Linters`](../../.github/workflows/linters.yml) workflow has one job:

- **Lint Template Repository** runs `npm ci` and `npm run lint` on this repository's own files, and fails if `grep -rn 'if false' template/` finds anything.

The [`Tests`](../../.github/workflows/tests.yml) workflow has two jobs:

- **Render** renders the body without `--trust`, once per answer set of its matrix. The answer sets are the default answers, a product name with spaces and a dot, `Render.Test Library`, with the `10.0.114` SDK, and one set for each remaining license, so that together they cover every license and both serviced SDK bands. Each render is checked for surviving placeholders and for link labels rendered as Python lists, then installed with `npm install` and linted, tested with `dotnet test` in Release, and packed with `dotnet pack`. The default answer set also builds the documentation website with `properdocs build --strict`.
- **Update From the Last Release** renders the last release with the default answers, commits it in a Git repository of its own, and updates it to the current commit with `copier update --defaults --vcs-ref HEAD --conflict inline`, as described above. The last release is the newest `v*` tag that the current commit contains, other than a tag on the current commit itself, so that pushing a release updates from the release before it. The job fails if the update leaves conflict markers or `.rej` files behind, or changes a file the template only creates, whose paths it reads from the update-only `_exclude` patterns in [`copier.yml`](../../copier.yml). It then runs the same placeholder checks, linters, tests and packaging as the render job.

Copier is installed at an exact version in both jobs (see [dependency management](dependency-management.md#the-roots-own-dependencies)).

The workflows are a safety net, not a substitute for rendering locally. They check only what is pushed, the update job only updates from the last release with the default answers, and they report a problem only after the change has left your machine. Render and check a change locally before pushing it, as described above.

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
