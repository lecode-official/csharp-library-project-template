# Spell Checking (CSpell)

This article covers the spell checking of the template's own files.

## The Root's Configuration

[CSpell](https://cspell.org/) checks the template's own files against the root's [`.cspell.json`](../../.cspell.json). The template's documentation is written in American English only, so unlike a generated project, the root installs no further language dictionaries. It enables the keyword dictionaries of the languages the repository talks about, such as `csharp`, `python`, `bash` and `node`, plus a set of general technical dictionaries.

It ignores `template/`, which the body's own configuration checks, `licenses/`, whose texts are verbatim, and itself, because its `flagWords` would otherwise report it as full of spelling mistakes.

## Running It

```shell
npm run lint:cspell
```

The script checks the root's Markdown, and [`copier.yml`](../../copier.yml). The editor extension and the Claude Code hook check every file you open or edit, so a word in a configuration file is flagged there even though the script does not cover it.

## Handling Findings

When a legitimate technical term or proper noun is flagged, add it to the `words` list rather than rewording the text to avoid it. Do not disable the check, and do not add a real misspelling.

Add a word to the configuration of the side it appears on:

- A word in the root's files goes into the root's [`.cspell.json`](../../.cspell.json).

A word that appears on both sides goes into both lists.

## Answers Are Spell-Checked Too

A generated project spell-checks its files after substitution, so every answer that lands in prose, such as the product name or the description, is checked by the generated project's CSpell. An unusual product name is the consumer's word to add to their own list, not the template's. Do test a change with a product name made of real words, though, so that a finding in the render points at the template rather than at the answer.

## Related

- [MarkdownLint](linting-markdownlint.md) — the companion Markdown linter.
- [Tooling](README.md) — the full tool set.
