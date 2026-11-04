# Setting up Visual Studio Code

This article covers installing Visual Studio Code and setting it up for the project. Visual Studio Code is recommended, though not required: every check it runs is also available on the command line (see [tooling](../tooling/README.md)).

## What Visual Studio Code Is

[Visual Studio Code](https://code.visualstudio.com/) is a free source code editor by Microsoft, available for Windows, macOS, and Linux. On its own it is a lightweight editor, and extensions add support for languages and tools. The repository ships a configuration for it under `.vscode/`, which formats every file on save, shows the findings of the linters while typing, and runs the npm scripts as tasks.

## Installing It

Install Visual Studio Code by following the [official setup instructions](https://code.visualstudio.com/docs/setup/setup-overview) for your operating system. They also cover adding the `code` command to the shell, which opens a folder in the editor:

```shell
code .
```

## Installing the Extensions

Open the root of the repository as a folder. On first opening it, Visual Studio Code offers to install the extensions recommended in [`extensions.json`](../../../.vscode/extensions.json). Install all of them. If the offer was dismissed, run "Extensions: Show Recommended Extensions" from the command palette and install them from there.

One of them, [Workspace Config Plus](https://marketplace.visualstudio.com/items?itemName=Swellaby.workspace-config-plus), is not optional in practice. The repository splits its editor configuration into a committed shared layer and a personal local layer, and that extension is what merges the two into the configuration the editor actually reads. Without it, **none** of the shared configuration takes effect: format-on-save, the solution path the C# extension reads, and the linter integrations all silently do nothing, with no error to explain why.

The C# extension needs the [.NET SDK](installing-the-tools.md#net-sdk) to be installed first, and the dprint extension uses the project's own `dprint`, which `npm ci` installs (see [installing the tools](installing-the-tools.md)).

## How the Configuration Works

[Visual Studio Code integration](../tooling/editor-integration.md) explains the shared and the local layer, what each setting does, the tasks, and which extension uses which engine. Read it before changing anything under `.vscode/`.

## Related

- [Installing the tools](installing-the-tools.md) — what the extensions run.
- [Visual Studio Code integration](../tooling/editor-integration.md) — how the editor configuration works.
