# Testing

This article covers how a change to the template is tested, and the conventions for the tests the template body ships.

## Rendering Is the Test Suite

The template has no test project of its own. Its test is a render: generate a project from the working tree, then run that project's own linters, build and tests, exactly as a consumer would on day one. [Authoring](../project-template/authoring.md#verifying-a-change) has the commands.

A change is not done until a render of it is green. Build and test the render in Release, as the generated project's continuous integration does: the body's static code analysis treats warnings as errors only in Release builds, so a Debug build passes code that every generated project's first pull request would fail on. A render that fails its linters or its tests is a defect in the template, even when the failing file is one the change never touched, because it fails the same way in every project generated from now on.

## Which Renders to Run

One render with the default answers catches most mistakes. A change that touches something an answer feeds needs more than one:

- **A product name with spaces and a dot**, such as `Render.Test Library`. It appears in file names, in `InternalsVisibleTo`, and in quoted shell commands in the npm scripts, and it is the answer most likely to break one of them.
- **Every choice of a multiple-choice question the change touches.** A change to `template/LICENSE` or `licenses/` is rendered once per license.
- **Each serviced SDK band**, for a change to `template/global.json` or the workflows. `dotnet_sdk_version` is a free string, so render once with the newest version of each band its help text names (see [questions](../project-template/questions.md#dotnet_sdk_version)).
- **An update, for a structural change.** When a file is moved, renamed or restructured, render a project from the last tag, commit it in its own Git repository, and run `copier update --vcs-ref HEAD` in it against your working tree. The conflicts you see there are the conflicts every consumer will see.

After every render, check that no placeholder survived, and that none was rendered as a Python list (see [Markdown style](markdown-style.md)):

```shell
grep -rn '\[\[' /tmp/render-test
grep -rnE "\['[^']*'\]\(" /tmp/render-test
```

## Tests in the Body

The tests in `template/tests/unit-tests/` follow the generated project's [testing](../../template/docs/developer-manual/conventions/testing.md) conventions unchanged: one `sealed` test class per source type named `<TypeName>Tests`, in the mirroring namespace and folder, test method names that run the member, the scenario and the outcome together, Arrange-Act-Assert separated by blank lines, and a documentation comment on every member that explains why the scenario matters.

Every type in the body's library has tests, in the same change that adds it. A generated project starts with a passing suite that demonstrates these conventions, and a type without a test would be the first thing it teaches its developers to skip.

The library's placeholder type and its test class are a pair. Change one and the other changes with it, and a consumer replaces both together.

## Related

- [Authoring](../project-template/authoring.md) — the render commands.
- [C# style](csharp-style.md) — the conventions the test code also follows.
- [Questions](../project-template/questions.md) — the answers worth varying between renders.
- [Tooling](../tooling/README.md) — the linters the workflow runs on this repository's own files.
- [Testing](../../template/docs/developer-manual/conventions/testing.md) — the generated project's full rule set.
