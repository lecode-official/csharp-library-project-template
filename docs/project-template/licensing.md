# Licensing

This article covers how a generated project's `LICENSE` file is produced, the rule that decides whether a copyright notice may be substituted into it, and the terms under which the vendored license texts are redistributed.

## How the File Is Produced

[`template/LICENSE`](../../template/LICENSE) is one line:

```jinja
[% include "licenses/" ~ license ~ ".txt" %]
```

Copier's Jinja loader searches from the clone root rather than from the rendered subdirectory, so this reaches [`licenses/`](../../licenses/), which is never copied into a generated project. The included file is itself rendered, so any placeholder inside it is substituted in the same pass.

This is ordinary sandboxed Jinja. It needs **no `--trust`**, no network access, and it survives `copier update` — all three of which a download task would cost. A task is also re-run three times per update, because Copier renders the old and the new version of the template alongside the real destination.

## Not Every License May Be Modified

This is the part that is easy to get wrong. The copyright line is operative text in some licenses and off-limits in others:

| SPDX identifier                      | Substituted? | Why                                                                                                                                                                                                                |
| ------------------------------------ | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `MIT`                                | **Yes**      | `Copyright (c) [year] [fullname]` is part of the license grant. Leaving it unfilled makes the license meaningless.                                                                                                 |
| `BSD-2-Clause`, `BSD-3-Clause`       | **Yes**      | Same — the notice is the first line of the operative text.                                                                                                                                                         |
| `Apache-2.0`                         | **No**       | The text ships verbatim. Its `[yyyy] [name of copyright owner]` sits in an appendix whose own instructions say to put that boilerplate in **source file headers**, not in `LICENSE`.                               |
| `MPL-2.0`                            | **No**       | Verbatim. It carries no copyright placeholder at all. The notice is Exhibit A, again for source headers.                                                                                                           |
| `GPL-3.0-only`, `GPL-3.0-or-later`   | **No**       | Verbatim, and the document says so itself: *"Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed."*                                              |
| `LGPL-3.0-only`, `LGPL-3.0-or-later` | **No**       | Same. The `Copyright (C) 2007 Free Software Foundation, Inc.` line in those texts is the FSF's copyright **on the license document**, not the licensee's — substituting a name there would be a false attribution. |
| `UNLICENSED`                         | **Yes**      | A hand-written proprietary notice, so it is ours to template.                                                                                                                                                      |

Note also that **no project-name placeholder exists** in any of these licenses. Only BSD-4-Clause, NCSA, Vim and MulanPSL-2.0 have one, and none of those is offered. The product name therefore goes into the `<Copyright>` property, source-file headers and the read me — never into `LICENSE`.

For the verbatim licenses, the copyright year and holder are still collected, because they are still needed. They land in the project file's `<Copyright>` property instead.

## Where the Texts Come From

[`scripts/refresh-licenses.py`](../../scripts/refresh-licenses.py) vendors them, from two sources chosen for two different reasons:

- **The substituting licenses** come from [choosealicense.com](https://github.com/github/choosealicense.com)'s `_licenses/` directory, because that is the source that marks the fill-in spots with explicit `[year]` and `[fullname]` tokens. The script rewrites those tokens into `[[ copyright_year ]]` and `[[ copyright_holder ]]` **at vendoring time**, so that rendering a project needs nothing but Jinja. The repository publishes no releases, so the script pins a commit of its `gh-pages` branch, `CHOOSE_A_LICENSE_COMMIT`. If a token is missing from a downloaded text, because choosealicense.com renamed it, the script fails instead of vendoring a text with a literal token in its copyright line.
- **The verbatim licenses** come from the [SPDX license list](https://github.com/spdx/license-list-data), pinned to a tagged release rather than tracking a moving branch. Nothing in them is rewritten.

Every text is downloaded and checked before the first file is written, so a failed download or a failed check leaves `licenses/` exactly as it was, and every download gives up after 30 seconds instead of hanging. Re-run the script to refresh the texts, and bump `SPDX_LICENSE_LIST_VERSION` or `CHOOSE_A_LICENSE_COMMIT` in it deliberately when you want newer texts:

```shell
python3 scripts/refresh-licenses.py
```

## Under What Terms the Texts Are Redistributed

The template repository itself is licensed under the MIT license (see [`LICENSE`](../../LICENSE)). The vendored texts in [`licenses/`](../../licenses/) are not covered by it. Each comes with terms of its own:

- **The GNU license texts** (`GPL-3.0-only`, `GPL-3.0-or-later`, `LGPL-3.0-only`, `LGPL-3.0-or-later`) state their own terms in their first lines: *"Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed."* That is why they are vendored and rendered without a single change.
- **The choosealicense.com texts** (`MIT`, `BSD-2-Clause`, `BSD-3-Clause`) come from a repository that is itself licensed under the MIT license, copyright GitHub, Inc. and contributors. That license permits the modification the refresh script makes, rewriting the fill-in tokens into placeholders.
- **The Apache-2.0 and MPL-2.0 texts** come from the SPDX license list data, unchanged. They are the license documents as their stewards publish them, shipped the way every project that adopts one of these licenses ships it.
- **`UNLICENSED.txt`** is written by hand for this template, and falls under the template's own MIT license.

## The Delimiter Constraint

Because the included text is rendered as Jinja in this template's remapped delimiters, **a license text containing `[[`, `[%` or `[#` would break the include**. The refresh script checks every downloaded text for these opening delimiters, and for the closing ones, `]]`, `%]` and `#]`, as a precaution, because a stray closing delimiter is a sign of a text that was mangled on its way here. It fails loudly rather than vendoring a text that trips the check. The check runs before the fill-in tokens are rewritten, since the rewriting introduces `[[` and `]]` on purpose. None of the current texts trips it — the bracketed tokens in them are all single-bracket — but a newly added license could.

The check is worth re-running by hand after any manual edit. It leaves out `[[` and `]]`, which the three substituting texts contain in their copyright lines by design:

```shell
grep -rn '\[%\|\[#\|%\]\|#\]' licenses/
```

## The NuGet Side

The chosen identifier goes straight into the library's `<PackageLicenseExpression>`, which is what NuGet publishes. Two things to know:

- **`UNLICENSED` is not an SPDX identifier.** It is a NuGet extension to the expression grammar, and it is the right answer for a library that is not published publicly: it packs successfully, but nuget.org rejects it.
- **`GPL-3.0` and `LGPL-3.0` without a suffix are deprecated** SPDX identifiers, replaced by the `-only` and `-or-later` forms in SPDX 3.0. Only the current forms are offered, which is also why the SPDX data repository has no `text/GPL-3.0.txt` to vendor.

## Adding a License to the Choices

1. Add the identifier to the `license` question's `choices` in [`copier.yml`](../../copier.yml).
2. Add it to `SUBSTITUTING_LICENSES` or `VERBATIM_LICENSES` in [`scripts/refresh-licenses.py`](../../scripts/refresh-licenses.py) — decide which by the table above, not by convenience.
3. Re-run the script, and check the vendored file is what you expect.
4. Render a project with the new choice and confirm the `LICENSE` file is complete and carries no leftover placeholder.
5. Add an entry for it to the render matrix of [`.github/workflows/template.yml`](../../.github/workflows/template.yml), which renders every license on every push.

## Related

- [Template structure](template-structure.md) — why the include can reach outside the rendered subdirectory.
- [Questions](questions.md) — the `license`, `copyright_holder` and `copyright_year` questions.
- [Dependency management](../conventions/dependency-management.md) — how the vendored texts are pinned.
