# Testing

This article covers how a change to the template is tested.

## Rendering Is the Test Suite

The template has no test project of its own. Its test is a render: generate a project from the working tree, then run that project's own build, exactly as a consumer would on day one. [Authoring](../project-template/authoring.md#verifying-a-change) has the commands.

A change is not done until a render of it is green. A render that fails its build is a defect in the template, even when the failing file is one the change never touched, because it fails the same way in every project generated from now on.

## Which Renders to Run

One render with the default answers catches most mistakes. A change that touches something an answer feeds needs more than one:

- **A product name with spaces and a dot**, such as `Render.Test Library`. It appears in file names, and it is the answer most likely to break one of them.
- **An update, for a structural change.** When a file is moved, renamed or restructured, render a project from the last tag, commit it in its own Git repository, and run `copier update --vcs-ref HEAD` in it against your working tree. The conflicts you see there are the conflicts every consumer will see.

After every render, check that no placeholder survived, and that none was rendered as a Python list (see [Markdown style](markdown-style.md)):

```shell
grep -rn '\[\[' /tmp/render-test
grep -rnE "\['[^']*'\]\(" /tmp/render-test
```

## Related

- [Authoring](../project-template/authoring.md) — the render commands.
- [Questions](../project-template/questions.md) — the answers worth varying between renders.
- [Tooling](../tooling/README.md) — the linters the workflow runs on this repository's own files.
