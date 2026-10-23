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

## Adding a File to the Body

1. Put it under [`template/`](../../template/), at the path it should have in the generated project.
2. Use `[[ answer_name ]]` for anything project-specific. If the value is not a question yet, add one — see [questions](questions.md).
3. If it is a Markdown article, list it in the generated project's [documentation index](../../template/docs/README.md), **and** the relevant section index. Both are hand-maintained.
4. Render and check.

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
