# Template Documentation

This is the documentation for the template itself: how it is laid out, what it asks, how to change it, and the conventions and tools that go with changing it. It is never copied into a generated project.

1. [Project Template](project-template/README.md) — the repository as a Copier template.
   1. [Template Structure](project-template/template-structure.md) — the two-level layout, and the four problems it solves.
   2. [Questions](project-template/questions.md) — every question, what it feeds, and how to add one.
   3. [Rendering and Updating](project-template/rendering-and-updating.md) — generating a project, and keeping it in step with the template.
   4. [Authoring](project-template/authoring.md) — the delimiters, adding a file, and verifying a change.
2. [Conventions](conventions/README.md) — how the files on both sides of the split are written.
   1. [Comments and Documentation](conventions/comments-and-documentation.md) — what the root and the body each explain, and how.
   2. [Markdown Style](conventions/markdown-style.md) — the shared Markdown rules, and placeholders in body Markdown.
   3. [Line Length](conventions/line-length.md) — the 150-character limit, and what a placeholder does to it.
   4. [File and Naming Conventions](conventions/file-and-naming-conventions.md) — naming files, and placeholders in paths.
   5. [Commit Messages](conventions/commit-messages.md) — the 50/72 rule, AI disclosure, and tag messages.
   6. [Git Workflow](conventions/git-workflow.md) — who runs which Git command, and rendering without committing.
   7. [Versioning](conventions/versioning.md) — the template's version, its tags, and its changelog.
   8. [Dependency Management](conventions/dependency-management.md) — exact pins on both sides.
   9. [Testing](conventions/testing.md) — rendering as the test suite.
3. [Tooling](tooling/README.md) — the tools used to work on the template.
   1. [Developer Setup](tooling/developer-setup.md) — Node.js, Copier, and what a render needs.
   2. [Visual Studio Code Integration](tooling/editor-integration.md) — the root's shared and local editor configuration.
   3. [Code Formatting (dprint)](tooling/formatting-dprint.md) — the root's formatter.
   4. [Markdown Linting (MarkdownLint)](tooling/linting-markdownlint.md) — the Markdown linting of the root.
   5. [Spell Checking (CSpell)](tooling/spell-checking-cspell.md) — the spell checking of the root.
   6. [Claude Code Hooks](tooling/claude-code-hooks.md) — the root's hooks.

Start with [template structure](project-template/template-structure.md) if you have not worked on this repository before. The split between the root and `template/` is the thing that makes everything else make sense.
