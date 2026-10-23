# Questions

This article covers every question the template asks, what each answer feeds, how each answer is validated, and how to add a question.

Copier asks questions **in declaration order**, and a question may only reference the answers above it.

## Types and Validation

Every question is declared with `type: str` and accepts free text, and its `validator` rejects an answer that would break the generated project, with a message that says what is allowed.

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

The product name and the slug are deliberately separate, because the product name is a display name that ends up in file names with spaces, while the slug is a URL- and directory-safe identifier. See [file and naming conventions](../conventions/file-and-naming-conventions.md) for how the two are used in paths.

The `product_slug` default lowercases the product name and turns every run of characters other than a lowercase letter or a digit into a single dash, then strips a leading or trailing dash. So `CLI.NET Core` becomes `cli-net-core`. An earlier default only replaced spaces, which turned the same name into `cli.net-core`, a slug the validator now rejects.

## Authorship

| Question           | Default          | Validation                                                   | Feeds                                                             |
| ------------------ | ---------------- | ------------------------------------------------------------ | ----------------------------------------------------------------- |
| `author`           | —                | Not empty, and none of `"`, `\`, `[`, `]`, `<`, `>` and `&`. | The NuGet `Authors`, and the `author` of the root `package.json`. |
| `copyright_holder` | `author`         | Not empty, and none of `"`, `\`, `<`, `>` and `&`.           | The `<Copyright>` property.                                       |
| `copyright_year`   | the current year | Exactly four digits.                                         | The same two places.                                              |

`author` may not contain square brackets, because an author's name is commonly written into a Markdown link, `[name](url)`.

The `copyright_year` default is rendered as `[[ '%Y' | strftime ]]`, so it is always the year the project is generated in, and never needs updating by hand. `strftime` is a filter of the `jinja2_ansible_filters` extension, which Copier always loads, so it costs no `--trust`. `copier update` reuses the recorded answer, so a project's copyright year never moves after it was generated.

## Repository

| Question             | Default       | Validation                                                                                                               | Feeds                                                                                                                                                                        |
| -------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `repository_url`     | —             | Starts with `http://` or `https://`, contains no whitespace, `"`, `<` or `>`, and does not end with a slash.             | `RepositoryUrl`, `PackageProjectUrl`, the read me badges, the website's `repo_url`, and the link-rewriting hook that turns relative links out of `docs/` into absolute ones. |
| `default_branch`     | `main`        | Letters, digits, dots, slashes, hyphens and underscores, starting and ending with a letter or a digit, and without `..`. | The docs workflow's trigger, the link-rewriting hook's branch, and the editor's branch protection.                                                                           |
| `integration_branch` | `development` | The same rule as `default_branch`, and different from `default_branch`.                                                  | The editor's branch protection, alongside `default_branch`.                                                                                                                  |

The branch names are limited to the characters Git allows in a branch name that are also safe in the YAML and JSON they end up in.

## Adding a Question

1. Declare it in [`copier.yml`](../../copier.yml), **after** any question it references. Give it a `help` string. It is the only explanation a person rendering the template sees.
2. Give it a `validator` that allows only the characters that are safe everywhere the answer lands, and a message that says what is allowed. Its default has to pass the validator too.
3. Prefer a free string over `choices` for any answer whose valid values change over time, because a recorded answer that drops out of the `choices` breaks `copier update` for every project that picked it.
4. Use it somewhere in [`template/`](../../template/).
5. Add it to the tables above, with its default, its validation rule and what it feeds.
6. Render a project and confirm the answer lands everywhere you expected.

A question that only ever has one sensible answer, and is not expected to grow a second one, is better expressed as a constant in the template body than as a question nobody reads.

## Related

- [Template structure](template-structure.md) — where the answers are recorded, and why that file lives inside the body.
- [Authoring](authoring.md) — using an answer in a template file.
- [Rendering and updating](rendering-and-updating.md) — how recorded answers are replayed during an update.
