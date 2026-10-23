# Spell Checking (CSpell)

This article covers spell checking of code, comments, and documentation.

[CSpell](https://cspell.org/) is configured in [`.cspell.json`](../../../.cspell.json) and checks American English, German, Spanish, and French.

## Dictionaries

The command-line interface does not bundle the German, Spanish, and French dictionaries, so they are installed as dev dependencies (`@cspell/dict-de-de`, `@cspell/dict-es-es`, `@cspell/dict-fr-fr`) and registered through the `import` field. The editor extension imports the same `.cspell.json` (see [editor integration](editor-integration.md)), including its `import` field, so it resolves the dictionaries from the same dev dependencies once `npm install` has run. That is why the extension recommendations name only the spell checker itself and none of its separate language add-ons.

The language dictionaries are `en-us`, `de-DE`, `es-ES`, and `fr-FR`, together with `en-us-common-misspellings` and `en-common-misspellings`. Beyond them, the configuration enables the keyword dictionaries of the languages and tools in the repository (`bash`, `csharp`, `docker`, `git`, `node`, `npm`, `sql`), plus a set of general technical dictionaries, so that ordinary industry vocabulary does not have to be listed by hand: `companies`, `computing-acronyms`, `filetypes`, `fonts`, `fullstack`, `lorem-ipsum`, `misc`, `networking-terms`, `public-licenses`, `software-terms`, `software-term-suggestions`, `software-tools`, `coding-compound-words`, and `web-services`.

## Ignored Paths and Custom Words

Build output and dependencies are ignored, along with lock files, SVGs, local environment files, and operating-system file-preview databases. `.cspell.json` ignores itself, because it contains the `flagWords` that are always treated as errors and would otherwise report itself as full of spelling mistakes.

The `words` list starts out with only the vocabulary of the toolchain — tool names, extension publishers, configuration keys. The project's own domain vocabulary is added to it as the code and the documentation need it.

## Running It and Handling Findings

```shell
npm run lint:cspell
```

When a legitimate technical term or proper noun is flagged, add it to the `words` list **in alphabetical order**, rather than rewording the text to avoid it.

Do not disable the check, and do not add a real misspelling to `words`. There is one narrow exception: a third-party API that misspells its own identifier forces the misspelling into the code that calls it. Whitelist that word with a comment saying which API requires it, so that the next reader does not "fix" it and break the call.

`flagWords` holds short strings that are always treated as errors regardless of case — common typos too short for CSpell's default minimum word length to catch.

This documentation is spell-checked as well, so keep new prose free of unknown words, or add legitimate terms to the dictionary in the same change.

## Editor Task

The Visual Studio Code "Lint Spelling" task uses a custom problem matcher, because CSpell has no built-in one (see [editor integration](editor-integration.md)).

## Related

- [Tooling](README.md) — the full linter set.
- [MarkdownLint](linting-markdownlint.md) — the companion Markdown linter.
- [Continuous integration](continuous-integration.md) — the pinned version used there.
