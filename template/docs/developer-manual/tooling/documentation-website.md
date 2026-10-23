# Documentation Website

This article covers the [ProperDocs](https://properdocs.org/) site, themed with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), that publishes everything under [`docs/`](../README.md).

A project that does not publish a website deletes [`properdocs.yml`](../../../properdocs.yml), and [`requirements.txt`](../../../requirements.txt), and this article with them. The documentation itself is written to be read on the repository host either way — the site is an addition, never a prerequisite.

## Why ProperDocs, Not MkDocs

The site was originally built on [MkDocs](https://www.mkdocs.org/), which has gone unmaintained. [ProperDocs](https://properdocs.org/) is a fork by MkDocs' own last active maintainer, positioned as a drop-in continuation of the MkDocs 1.x line rather than a break from it: it reads the same configuration format, and it registers both `mkdocs.*` and `properdocs.*` plugin and theme entry points, so [mkdocs-material](https://squidfunk.github.io/mkdocs-material/), [mkdocs-gen-files](https://github.com/oprypin/mkdocs-gen-files), and [mkdocs-literate-nav](https://oprypin.github.io/mkdocs-literate-nav/) — all still published under their original MkDocs-branded package names — work with it unmodified. Only the engine changed.

## Configuration

[`properdocs.yml`](../../../properdocs.yml) lives at the repository root and points `docs_dir` at the existing [`docs/`](../README.md) tree, so every hand-written article is part of the site without having been moved or renamed. `site_dir` is set to `build/documentation-website`, alongside the rest of the build output, rather than ProperDocs' default of `site/`.

Three plugins are enabled:

- **search** — the built-in full-text search.
- **gen-files** — runs a Python script at the start of every build to produce a generated section.
- **literate-nav** — lets a `nav` entry point at a directory instead of a file, so that generated section brings its own navigation.

`markdown_extensions` adds [mdx_truly_sane_lists](https://github.com/radude/mdx_truly_sane_lists) with `nested_indent: 3`. Without it, Python-Markdown only recognizes a nested list item indented by a fixed four spaces, regardless of the parent marker's width — so a sub-list nested under a `1.`-style marker with the natural three-space indent renders as a second top-level list. Setting the indent relative to the parent marker fixes every such list without reformatting a single Markdown file.

## Light and Dark Mode

`theme.palette` lists two [palettes](https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/#color-palette-toggle), one for `scheme: default` and one for `scheme: slate`, each tied to a `media: "(prefers-color-scheme: ...)"` query, so the site opens in whichever mode the visitor's system is set to. Each palette also carries a toggle that lets a visitor override that for the session, which the theme remembers.

## Build Scripts

Anything under `docs_dir` that is not excluded is copied into the built site as-is, at the same relative path. `exclude_docs` therefore excludes the whole `docs/build/` directory, because the Python scripts in it are run at build time rather than published. Without that exclusion the site generator would copy the scripts themselves into the built site as static files, and with them the `__pycache__` directory that Python writes next to them as soon as the hooks are loaded. Excluding the directory rather than the individual scripts covers both.

## Links Outside `docs/`

An article is free to link to a file anywhere else in the repository — source code, `README.md`, a workflow — with an ordinary relative Markdown link. That renders correctly on the repository host, which resolves it against the file's real position. The built site has no such files: `docs_dir` is the only part of the repository that is ever copied into `site_dir`, so the same link would 404 there.

A `hooks:` module closes that gap with an `on_page_markdown` function — a plain [MkDocs hooks](https://www.mkdocs.org/user-guide/configuration/#hooks) event, so no plugin package is needed. For every link, it resolves the target against the page's own file on disk:

- **Inside `docs_dir`** — left untouched. The site generator already resolves these correctly.
- **Outside `docs_dir`, inside the repository** — rewritten to an absolute link at `repo_url` against the default branch, with `tree` for a directory and `blob` for a file, preserving any fragment.
- **Outside the repository** — left untouched. Such a link is already broken on the host, and rewriting it is not this hook's concern.

## Navigation Is One Hand-Maintained List

The site navigation is the single `nav` list in [`properdocs.yml`](../../../properdocs.yml). There is no `.pages` file anywhere and no plugin that derives the hand-written navigation from the directory tree. Adding, removing, moving, or reordering an article means editing that one list — and the hand-maintained indexes, which every article must also appear in: the index of its manual ([Developer Manual](../README.md) or [User Manual](../../user-manual/README.md)) and, for a tooling or conventions article, its section's index ([tooling](README.md) or [conventions](../conventions/README.md)).

The one exception is a generated section, whose file list is not known until a build runs. Its `nav` entry ends in a slash, which tells literate-nav to look for a navigation file inside that directory, and the generating script writes that file itself alongside the pages it lists.

## A Generated API Reference

A project whose API reference is generated from its source's own documentation comments produces that section at build time and **never commits it**. There is no such directory in the repository and none is expected to appear, so there is no `.gitignore` entry for it either — nothing ever writes it to disk. Every build regenerates it from whatever the documentation comments currently say, which is the point: a committed API reference is one that is eventually wrong.

The generating script builds the project, shells out to the pinned documentation generator writing into a temporary directory — never into `docs/` — and re-emits every file through `mkdocs_gen_files.open()`, which hands the content to the in-memory build. While doing so it records each page in an `mkdocs_gen_files.Nav` and writes that navigation out for literate-nav to read.

One C#-specific trap is worth recording: the compiler never expands `<inheritdoc/>` into real text in the generated XML documentation file, it is left in verbatim. Any tool reading that file — the documentation generator, or a consumer's editor tooltip — therefore sees an empty member. A package that rewrites `<inheritdoc/>` with the real inherited text as a build step is what fixes it, and it only runs for non-`Debug` builds, so the generation step has to build in `Release`.

## Running It Locally

Install the pinned Python dependencies into a virtual environment (see [developer setup](developer-setup.md)), then, from the repository root:

```shell
properdocs serve     # http://127.0.0.1:8000, with live reload
properdocs build     # the static site, into build/documentation-website/
```

Both regenerate every generated section from scratch, so there is nothing to clean up afterwards.

`properdocs build --strict` turns every warning into an error, above all a link to a page or file that does not exist. Run it before pushing a documentation change, so that a broken link is caught before it is published.

## Related

- [Developer setup](developer-setup.md) — installing Python and the pinned dependencies.
- [Dependency management](../conventions/dependency-management.md) — how `requirements.txt` and the local tools pin their versions.
- [Markdown style](../conventions/markdown-style.md) — the conventions the published articles follow.
