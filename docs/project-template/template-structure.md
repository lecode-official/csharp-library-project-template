# Template Structure

This article covers the two-level layout of this repository, and the problems it solves.

## The Split

```text
.
├── copier.yml          the questions and the Copier settings
├── README.md           the template's own front door
├── AGENTS.md           rules for working on the template
├── CONTRIBUTING.md     how to contribute, next to CODE_OF_CONDUCT.md, SECURITY.md, and CONTRIBUTORS.md
├── docs/               these articles
├── licenses/           the vendored license texts
├── scripts/            maintenance scripts
├── dprint.json         the template's own formatter configuration
├── .markdownlint.yml   the template's own Markdown linting
├── .cspell.json        the template's own spell checking
├── package.json        the template's own linters
└── template/           ← _subdirectory; the only thing that is ever rendered
```

`copier.yml` sets `_subdirectory: template`, which makes Copier walk **only** that directory when it generates a project. Everything beside it belongs to the template itself.

## Why Not Make the Whole Repository the Template

The obvious alternative — the one every other template in this family uses — is to let the repository *be* the template body, with `copier.yml` sitting among the files it renders. That works, and it causes four problems that the split removes outright:

1. **Documentation about the template has nowhere to live.** In a single-level template, a paragraph explaining how to render the template would be rendered *into* every generated project, where it is nonsense. The workaround is to wrap it in `[% if false %]`, which is invisible to the reader and easy to forget. Here, the template's documentation is simply outside the body, and the generated project's documentation is inside it. No conditional is needed anywhere, and `grep -rn "if false" template/` finding nothing is a check worth keeping.
2. **The template's own files could not be linted or installed.** Project files in the body contain Jinja — a `package.json` whose `name` is a placeholder is not a valid `package.json`, so `npm install` may refuse it, and the linters then cannot run at all. The `[ -x node_modules/.bin/<tool> ] || exit 0` guard on every tool hook in those templates is then not a corner case but the normal state, and the hooks never check anything. Here, the root has a real `package.json`, real dependencies, and its own linters that actually run. Its hooks carry the same guard, but only for a fresh clone before the first `npm ci` (see [Claude Code hooks](../tooling/claude-code-hooks.md)).
3. **Linter settings could not differ between the two.** They frequently should. This repository's own `.markdownlint.yml` governs articles that talk *about* placeholders, while the generated project's governs articles that *contain* them.
4. **The repository could not explain how to use itself.** A `README.md` at the root of a single-level template is the generated project's read me, so the instructions for rendering it have nowhere to go but an external wiki. Here the root read me is exactly that: instructions for rendering.

## What Copier Requires of This Layout

Three constraints, each verified against Copier's own behavior:

- **`copier.yml` must stay at the repository root.** Copier globs for `copier.*` in the clone root and never recurses. A copy inside `template/` would be silently ignored *and* copied into every generated project as an ordinary file.
- **The answers file template must live inside the body**, at [`template/.copier-answers.yml`](../../template/.copier-answers.yml). Only the subdirectory is walked, so a copy at the root would never be rendered — and without a rendered `.copier-answers.yml`, a generated project cannot be updated at all.
- **`_exclude` patterns are matched against the generated project's paths**, not the template's, so none of them carries a `template/` prefix. Copier also defaults `_exclude` to empty once `_subdirectory` names a real directory, because nothing outside it is reachable in the first place. The patterns follow the `.gitignore` syntax, so a pattern for a root-level directory or file is anchored with a leading slash, as in `/build`. An unanchored `build` would match at any depth and also drop the body's `docs/build/`.

## The One Thing That Reaches Across

Jinja's `include` is the deliberate exception. Copier's template loader searches from the **clone root**, not from the subdirectory, so a file inside `template/` can include a file beside `copier.yml`:

```jinja
[% include "licenses/" ~ license ~ ".txt" %]
```

That is how [`template/LICENSE`](../../template/LICENSE) gets its content out of [`licenses/`](../../licenses/) without those texts ever being copied into a project as files of their own. It is ordinary sandboxed Jinja rather than an unsafe feature, so it costs no `--trust` (see [licensing](licensing.md)).

The loader rejects any path that resolves outside the clone root, and rejects symlinks that escape it, so this reaches sideways but not out.

## Related

- [Questions](questions.md) — what the template asks and what each answer feeds.
- [Licensing](licensing.md) — the include mechanism in practice.
- [Authoring](authoring.md) — adding a file to the body.
- [Rendering and updating](rendering-and-updating.md) — what a consumer of the template does.
