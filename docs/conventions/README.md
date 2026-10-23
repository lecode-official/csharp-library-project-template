# Conventions

This section covers the conventions for authoring the template: how the files in this repository are written, styled, named, committed, and released.

1. [Comments and Documentation](comments-and-documentation.md)
2. [Markdown Style](markdown-style.md)
3. [Line Length](line-length.md)
4. [File and Naming Conventions](file-and-naming-conventions.md)
5. [Commit Messages](commit-messages.md)
6. [Git Workflow](git-workflow.md)
7. [Versioning](versioning.md)
8. [Dependency Management](dependency-management.md)
9. [Testing](testing.md)

## Two Sets of Files, One Set of Rules

The [split](../project-template/template-structure.md) between the root and `template/` means every file here belongs to one of two projects:

- **A file at the root** belongs to the template itself. It follows the articles in this section.
- **A file under `template/`** becomes a file of the generated project. Once rendered, it *is* that project's code, so it follows the generated project's own conventions, to the letter. The articles in this section add only what is different about writing such a file as a template: where placeholders may go, what changes once they are substituted, and how to check the result.

The two rule sets are deliberately the same wherever they can be, so that moving between the root and the body does not mean switching styles. Where a rule of the generated project changes, change its article in the body, every body file it affects, and the matching article here, in the same change.

These conventions are not suggestions. A template file that departs from the generated project's conventions teaches that departure to every project rendered from it, and a generated project's first reviewer reads the code it shipped with as the example to follow.
