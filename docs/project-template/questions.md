# Questions

This article covers every question the template asks, what each answer feeds, how each answer is validated, and how to add a question.

Copier asks questions **in declaration order**, and a question may only reference the answers above it — which is why `dotnet_sdk_version` is declared after `target_framework`, and `package_id` after `root_namespace`.

## Types and Validation

Every question is declared with `type: str`. Only `target_framework` and `license` restrict the answer to a list of `choices`. Every other question accepts free text, and its `validator` rejects an answer that would break the generated project, with a message that says what is allowed.

An answer ends up in file names, C# code, XML, JSON, YAML, Markdown and Python strings. Rather than escaping every answer for every format it lands in, the validators only allow characters that are safe in all of them. Each validator uses the `regex_search` filter of the `jinja2_ansible_filters` extension, which Copier always loads, so none of them costs a `--trust`.

A validator runs on every answer Copier collects, including a default the person accepts and an answer passed with `--data`. The tables below give each rule in words. [`copier.yml`](../../copier.yml) holds the exact expressions and messages.

## Naming

| Question              | Default                     | Validation                                                                                                                                                                        | Feeds                                                                                                                                                            |
| --------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `product_name`        | —                           | Only letters, digits, spaces, dots, hyphens, underscores and plus signs. Starts with a letter or a digit, and does not end with a space, a dot, a hyphen or an underscore.        | The `.slnx` and every `.csproj` file name, `AssemblyTitle`, `Product`, the assembly name `InternalsVisibleTo` references, and the documentation website's title. |
| `product_slug`        | derived from `product_name` | Lowercase letters and digits in groups separated by single dashes, `^[a-z0-9]+(-[a-z0-9]+)*$`.                                                                                    | The root `package.json` name, and the clone directory in the read me.                                                                                            |
| `product_description` | —                           | Not empty, and none of `"`, `\`, `<`, `>` and `&`.                                                                                                                                | The NuGet `Description`, the website's `site_description`, and the read me.                                                                                      |
| `library_slug`        | `product_slug`              | The same pattern as `product_slug`, and not `sample-app`, which is the sample app's directory.                                                                                    | The library's directory under `source/`, which is also its build output directory under `build/`.                                                                |
| `root_namespace`      | —                           | One or more PascalCase identifiers separated by dots, each starting with an uppercase letter and containing only letters and digits, such as `CliNetCore` or `LeCode.CliNetCore`. | `RootNamespace`, and the `namespace` in every `.cs` file. The sample app derives its own namespace from it.                                                      |
| `package_id`          | `root_namespace`            | Letters, digits and underscores in groups separated by single dots or hyphens, and at most 100 characters, which are NuGet's own rules for a package identifier.                  | The NuGet `PackageId`.                                                                                                                                           |

The product name and the slug are deliberately separate, because the product name is a display name that ends up in file names with spaces, while the slug is a URL- and directory-safe identifier. See [file and naming conventions](../../template/docs/developer-manual/conventions/file-and-naming-conventions.md) in the generated project for how the two are used.

The `product_slug` default lowercases the product name and turns every run of characters other than a lowercase letter or a digit into a single dash, then strips a leading or trailing dash. So `CLI.NET Core` becomes `cli-net-core`. An earlier default only replaced spaces, which turned the same name into `cli.net-core`, a slug the validator now rejects.

## Authorship

| Question           | Default          | Validation                                                                                                 | Feeds                                                                                       |
| ------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `author`           | —                | Not empty, and none of `"`, `\`, `[`, `]`, `<`, `>` and `&`.                                               | The NuGet `Authors`, and the `author` of the root `package.json`.                           |
| `copyright_holder` | `author`         | Not empty, and none of `"`, `\`, `<`, `>` and `&`.                                                         | The `<Copyright>` property, and the license text for the licenses that take a substitution. |
| `copyright_year`   | the current year | Exactly four digits.                                                                                       | The same two places.                                                                        |
| `maintainer_name`  | `author`         | Not empty, and none of `"`, `\`, `[`, `]`, `<`, `>` and `&`.                                               | `SECURITY.md`, `CODE_OF_CONDUCT.md` and `CONTRIBUTORS.md`, as the contact for reports.      |
| `maintainer_url`   | —                | Starts with `http://`, `https://` or `mailto:`, and contains no whitespace, `"`, `<`, `>`, or parentheses. | The same three files.                                                                       |

The maintainer's name and URL are written into a Markdown link, `[name](url)`, which is why the name may not contain square brackets and the URL may not contain parentheses. `author` follows the same rule as `maintainer_name`, because it is that question's default.

The `copyright_year` default is rendered as `[[ '%Y' | strftime ]]`, so it is always the year the project is generated in, and never needs updating by hand. `strftime` is a filter of the `jinja2_ansible_filters` extension, which Copier always loads, so it costs no `--trust`. `copier update` reuses the recorded answer, so a project's copyright year never moves after it was generated.

## Repository

| Question             | Default       | Validation                                                                                                               | Feeds                                                                                                                                                                        |
| -------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `repository_url`     | —             | Starts with `http://` or `https://`, contains no whitespace, `"`, `<` or `>`, and does not end with a slash.             | `RepositoryUrl`, `PackageProjectUrl`, the read me badges, the website's `repo_url`, and the link-rewriting hook that turns relative links out of `docs/` into absolute ones. |
| `default_branch`     | `main`        | Letters, digits, dots, slashes, hyphens and underscores, starting and ending with a letter or a digit, and without `..`. | The docs workflow's trigger, the link-rewriting hook's branch, and the editor's branch protection.                                                                           |
| `integration_branch` | `development` | The same rule as `default_branch`, and different from `default_branch`.                                                  | The editor's branch protection, alongside `default_branch`.                                                                                                                  |

The branch names are limited to the characters Git allows in a branch name that are also safe in the YAML and JSON they end up in.

## Toolchain and License

| Question             | Default                  | Validation                                                                                                         | Feeds                                                                               |
| -------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| `target_framework`   | `net10.0`                | One of the `choices`, of which `net10.0` is the only one.                                                          | The `TargetFramework` of both projects, and the build output paths that contain it. |
| `dotnet_sdk_version` | `10.0.402` for `net10.0` | A full release version of the form `X.Y.ZZZ`, starting with the target framework's version, `10.0.` for `net10.0`. | The SDK version pinned exactly in `global.json`.                                    |
| `license`            | `LGPL-3.0-or-later`      | One of the `choices`.                                                                                              | The `LICENSE` file, and the library's `PackageLicenseExpression`.                   |

### `target_framework`

Only `net10.0` today. .NET 10 is the current LTS release, supported until 14 November 2028. .NET 11 is at release-candidate stage with no stable SDK, so there is nothing else to offer.

It is still a question with `choices` rather than a constant, although it has a single answer. Every generated project records it in `.copier-answers.yml`, so the day a new .NET release is added as a second choice, a project can switch to it with `copier update` and keep every file that depends on it consistent. A constant would have to be turned into a question first. Add a choice here when a new release ships, together with its branch in the `dotnet_sdk_version` default.

### `dotnet_sdk_version`

The version pinned exactly in `global.json`. A .NET SDK version is `major.minor.<band><patch>`, and a new feature band opens when the tooling gains features rather than when the runtime changes, so every band of a release carries the same runtime.

**It is a free string, not a list of choices.** Copier rejects any answer that is not one of a question's `choices`, and it does so also when it replays the recorded answers during `copier update`. With a list, dropping a superseded version from it would make every project that had picked that version impossible to update. A free string keeps every recorded version valid, and the validator still rejects an answer that is not a release version or that belongs to a different .NET release than the target framework.

The `help` text names the feature bands that still receive servicing updates, with the newest patch of each: `10.0.4xx`, currently `10.0.402`, for the newest tooling, and `10.0.1xx`, currently `10.0.113`, for the original band. The `10.0.2xx` and `10.0.3xx` bands stopped receiving patches in May and August 2026, so the help no longer names them, although the validator still accepts their versions.

The default is rendered from `target_framework`, as `[% if target_framework == 'net10.0' %]10.0.402[% endif %]`. When a new SDK ships:

1. Raise the version in the default, if the new SDK is the newest patch of the newest serviced band.
2. Update the bands and the versions named in the `help` text, and drop a band that stopped receiving patches.
3. Render a project with the new version (see [testing](../conventions/testing.md)).

### `license`

An SPDX identifier, which becomes both the `LICENSE` file's content and the library's `PackageLicenseExpression`. See [licensing](licensing.md) — in particular for why only some of these take a copyright substitution.

## Adding a Question

1. Declare it in [`copier.yml`](../../copier.yml), **after** any question it references. Give it a `help` string. It is the only explanation a person rendering the template sees.
2. Give it a `validator` that allows only the characters that are safe everywhere the answer lands, and a message that says what is allowed. Its default has to pass the validator too.
3. Prefer a free string over `choices` for any answer whose valid values change over time, because a recorded answer that drops out of the `choices` breaks `copier update` for every project that picked it.
4. Use it somewhere in [`template/`](../../template/).
5. Add it to the tables above, with its default, its validation rule and what it feeds.
6. Render a project and confirm the answer lands everywhere you expected.

A question that only ever has one sensible answer, and is not expected to grow a second one, is better expressed as a constant in the template body than as a question nobody reads. `target_framework` is the exception, for the reason given above.

## Related

- [Template structure](template-structure.md) — where the answers are recorded, and why that file lives inside the body.
- [Licensing](licensing.md) — the `license` question in detail.
- [Authoring](authoring.md) — using an answer in a template file.
- [Rendering and updating](rendering-and-updating.md) — how recorded answers are replayed during an update.
