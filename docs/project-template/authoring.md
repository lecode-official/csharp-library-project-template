# Authoring

This article covers working on the template body: the delimiters, adding a file, and checking that a change actually renders.

## The Delimiters Are Not the Jinja Defaults

| Purpose    | Default   | Used here |
| ---------- | --------- | --------- |
| Expression | `{{ … }}` | `[[ … ]]` |
| Block      | `{% … %}` | `[% … %]` |
| Comment    | `{# … #}` | `[# … #]` |

The remap is inherited from the sibling templates in this family, where it is required so that a framework's own `{{ }}` interpolation passes through untouched. Keeping the same delimiters everywhere means articles and snippets stay copy-pasteable between templates. It also stops YAML and JSON formatters from mangling the delimiters.

The practical consequence: **`{{ }}` in a template file is literal text**, which is exactly what makes the GitHub Actions workflows under `template/.github/workflows/` work without escaping — their `${{ … }}` expressions pass straight through.

## No `.jinja` Extension

`_templates_suffix` is set to `""`, so **every** file in the body is processed as a template and no file needs a second extension. The reason is tooling: dprint treats a `.jinja` extension as HTML, which makes it throw on Markdown and strip whitespace from JSON.

Copier copies a file verbatim if it cannot read it as a template, so binary files are unaffected.

## Placeholders in File and Directory Names

Copier renders path names too, which is why the body contains directories and files like:

```text
template/source/[[ product_name ]].slnx
template/source/[[ library_slug ]]/[[ product_name ]].csproj
```

This is load-bearing for the C# layout, where a project file is named after the product rather than after its directory.

One consequence to keep in mind: `[` and `]` are character-class syntax in a glob, so a shell pattern that spells out a literal placeholder path matches nothing. Quote such paths, or match the directory with a `*`.

## Conditional Blocks

Content that only exists for some answers, such as the publishing to NuGet, which only exists when `publish_to_nuget` is true, goes into a `[% if %]` block. The template does not set `trim_blocks` in `_envops`, so a block tag leaves its line break behind, and every rendered file would get blank lines where a tag stood. Put each tag on a line of its own, with a blank line before it, and open it with `[%-`, which strips every whitespace character before the tag, the blank line and the line break above it included. What follows the tag is kept as it is, so a blank line after the tag is a blank line in the rendered file:

````markdown
Add the package to a project.

[%- if publish_to_nuget %]

```shell
dotnet add package [[ package_id ]]
```

[%- else %]

Download the package from the GitHub Release.

[%- endif %]

Then call it.
````

Laid out like this, the template and both renderings have exactly one blank line around every paragraph and every fenced code block, so the generated project's MarkdownLint accepts all three, and the template can be linted with it as it is. In a file where the conditional content continues the lines above it without a blank line, such as a comment in a workflow, leave out the blank line after the tag instead. A clause inside a sentence stays inline, as in `packed [% if publish_to_nuget %]and published [% endif %]as`, and a comment that differs in more than a clause is given in full in each branch of an `[% if %]`/`[% else %]` block, rather than split across a tag in the middle of its sentence.

A placeholder breaks a URL in Markdown, since its spaces end the link: `<https://www.nuget.org/packages/[[ package_id ]]>` is neither an autolink in the template nor a link MarkdownLint accepts. Put such an address in a code span instead.

Render the file once with each answer, and check that neither rendering has a missing or a doubled blank line. A Markdown article that only exists for some answers would get a conditional file name, but a section is usually enough. Never use an `[% if false %]` block to hide something, though (see [template structure](template-structure.md)).

## Adding a File to the Body

1. Put it under [`template/`](../../template/), at the path it should have in the generated project.
2. Use `[[ answer_name ]]` for anything project-specific. If the value is not a question yet, add one — see [questions](questions.md).
3. If it is Markdown, remember that the generated project's own MarkdownLint and CSpell will check it, using the configuration in `template/.markdownlint.yml` and `template/.cspell.json`, not this repository's.
4. If it is a Markdown article, list it in the generated project's [documentation index](../../template/docs/README.md), the relevant section index, **and** the `nav` in `template/properdocs.yml`. All three are hand-maintained.
5. Render and check.

## Avoid Markdown Tables with Placeholders

dprint pads a Markdown table's cells to align its pipes. A placeholder inside a table is padded at its *template* width, and substitution then changes that width — so the rendered project has a misaligned table that its own MarkdownLint flags with `MD060`, in a file nobody touched.

Put placeholders in prose, a list, or a fenced code block instead. None of those is aligned. This repository's own articles are free to use tables with placeholders in them, because they are never rendered. [Markdown style](../conventions/markdown-style.md#placeholders-in-body-markdown) covers the other places a placeholder is unsafe in Markdown.

## Files That Are Both Templated and Formatted

Every file in the body has to satisfy dprint twice: once as the template, and once as the rendered output. The two can disagree — the Markdown-table case above is the sharpest example, and the answers file is the other.

[`template/.copier-answers.yml`](../../template/.copier-answers.yml) writes the recorded answers with a single expression piped through `to_nice_yaml` and then `trim`. The `trim` matters: `to_nice_yaml` ends its output with a newline and the template file ends with one of its own, so without it the rendered file would end with two and `dprint check` would fail in a generated project before anyone had touched the code.

The generated project's own `dprint.json` therefore excludes the files whose formatting belongs to the tool that writes them — the answers file, and the npm and NuGet lock files. Note that the `**/*-lock.json` pattern does *not* match `packages.lock.json`, so both patterns are needed.

## Verifying a Change

A file can be valid as a template and invalid once rendered. Linting the template catches the first. Only rendering catches the second.

```shell
# Render the working tree with a throwaway answer set; "--vcs-ref HEAD" makes Copier render HEAD plus every uncommitted change, without it Copier
# renders the newest tag as soon as one exists; no --trust: if this ever starts demanding it, an unsafe feature has crept in, and that is a change
# worth making deliberately rather than by accident
copier copy --defaults --vcs-ref HEAD --data product_name="Render Test" --data root_namespace=RenderTest \
    --data product_description="A scratch render." --data author="Example" \
    --data repository_url=https://example.com/x --data maintainer_url=https://example.com \
    . /tmp/render-test

cd /tmp/render-test
npm install && npm run lint
dotnet test --solution "source/Render Test.slnx" --configuration Release
```

Then check the things that only a render reveals:

```shell
grep -rn '\[\[' /tmp/render-test             # no placeholder survived
grep -rnE "\['[^']*'\]\(" /tmp/render-test   # no link label rendered as a Python list (see markdown style)
grep -rn 'if false' template/                # no conditional crept back in
```

The second is worth keeping as a habit: `[% if false %]` blocks are the workaround this layout exists to remove (see [template structure](template-structure.md)).

One render with the default answers is the minimum. [Testing](../conventions/testing.md) covers which other answers a change needs to be rendered with, and how to check that an update applies cleanly.

## Related

- [Template structure](template-structure.md) — what is inside the body and what is not.
- [Questions](questions.md) — adding an answer to use.
- [Rendering and updating](rendering-and-updating.md) — what a consumer does with the result.
- [Conventions](../conventions/README.md) — how the files in the body are written, on top of the generated project's own conventions.
- [Testing](../conventions/testing.md) — which renders a change needs.
