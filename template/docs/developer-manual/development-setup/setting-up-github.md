# Setting up GitHub

This article covers what to set up on GitHub for the project, once its repository exists there: its labels, its repository settings, and GitHub Pages for the documentation website. All of it is done with the [GitHub CLI](installing-the-tools.md#the-github-cli), as scripts to run from a clone of the repository, so that the repository gets them exactly as documented. Running a script again is safe, since every command sets a value rather than adding one.

The scripts are written for a POSIX shell, such as Bash or Zsh. On Windows, run them in Git Bash or in the Windows Subsystem for Linux.

## Labels

The labels sort issues and pull requests, as the [GitHub workflow](../conventions/github-workflow.md#labels) describes. This script creates every one of them, with its color and description, written the way the table in the GitHub workflow writes them. `--force` updates a label that already exists instead of failing, so the script also brings existing labels back in step with the table in the GitHub workflow:

```shell
while IFS='|' read -r name color description; do
    gh label create "$name" --color "${color#\#}" --description "$description" --force
done <<'EOF'
Type: Bug|#B60205|The issue or pull request concerns the fixing of a bug.
Type: CI/CD|#6800E7|The issue or pull request concerns the continuous integration and deployment (CI/CD) pipeline.
Type: Content|#A7DA8B|The issue or pull request concerns the addition or updating of content, for example on a website.
Type: Design|#E99695|The issue or pull request concerns visual design.
Type: Documentation|#3545AF|The issue or pull request concerns the updating or adding of content to the documentation.
Type: Idea or Request|#1D76DB|The issue or pull request concerns an idea or the request for adding a new feature.
Type: Implementation|#006B75|The issue or pull request concerns the implementation of a new feature.
Type: Release|#F9D0C4|The issue or pull request concerns the preparation of a release.
Type: Testing & Linting|#FF7518|The issue or pull request concerns unit tests, integration tests, linting, or formatting.
Priority: Critical|#B60205|The issue or pull request has a critical priority.
Priority: High|#E99695|The issue or pull request has a high priority.
Priority: Medium|#1D76DB|The issue or pull request has a medium priority.
Priority: Low|#0E8A16|The issue or pull request has a low priority.
Status: Abandoned|#B60205|The issue or pull request was abandoned and no longer needs to be addressed.
Status: Blocked|#D93F0B|The issue or pull request is blocked until other issues or pull requests are completed.
Status: Can't Reproduce|#750DB3|The issue or pull request tries to address a bug, which cannot be reproduced.
Status: Confirmed|#0E8A16|The issue or pull request concerns a bug, which was confirmed to be reproducible.
Status: Duplicate|#FEB6A8|The issue or pull request is a duplicate of another issue or pull request.
Status: Needs Information|#FBCA04|The issue or pull request needs more information to proceed.
Status: Won't Do/Fix|#5319E7|The issue or pull request concerns a feature request or bug that will not be addressed.
Dependabot: GitHub Actions Update|#0366D6|The pull request was opened by Dependabot and updates the GitHub Actions actions.
Dependabot: NuGet Update|#0366D6|The pull request was opened by Dependabot and updates the NuGet packages.
Dependabot: .NET SDK Update|#0366D6|The pull request was opened by Dependabot and updates the .NET SDK.
Dependabot: npm Update|#0366D6|The pull request was opened by Dependabot and updates the npm packages.
Dependabot: pip Update|#0366D6|The pull request was opened by Dependabot and updates the Python packages.
EOF
```

A new repository on GitHub starts with GitHub's default labels, such as `bug` and `enhancement`, which the labels above replace. Delete them, so that nobody picks one by mistake. `gh label delete` fails for a label that does not exist, which is harmless:

```shell
for name in 'bug' 'documentation' 'duplicate' 'enhancement' 'good first issue' 'help wanted' 'invalid' 'question' 'wontfix'; do
    gh label delete "$name" --yes
done
```

A label that is added to the GitHub workflow is added to the script in the same change, so that the two never disagree.

Run the script before Dependabot opens its first pull request. Dependabot labels its pull requests with the `Dependabot:` labels, but it never creates a label, and it silently leaves out one that does not exist.

## Repository Settings

The repository settings match the [Git workflow](../conventions/git-workflow.md#the-branches) and the [GitHub workflow](../conventions/github-workflow.md#pull-requests):

- **Merge commits only.** Squash merging and rebase merging are turned off, because a pull request is always merged with a merge commit.
- **The pull request's title and description as the default merge message.** A merge message is written by hand anyway, but a merge through GitHub's web interface then starts from the pull request rather than from GitHub's generic message.
- **No wiki and no projects.** The documentation lives in the repository, and the work is tracked with issues and milestones.

```shell
gh repo edit --enable-merge-commit --enable-squash-merge=false --enable-rebase-merge=false --enable-wiki=false --enable-projects=false
gh api --method PATCH 'repos/{owner}/{repo}' -f merge_commit_title=PR_TITLE -f merge_commit_message=PR_BODY
```

`gh api` replaces `{owner}` and `{repo}` with the repository of the current directory.

## GitHub Pages

The docs workflow publishes the [documentation website](../tooling/documentation-website.md) through GitHub Pages on every push to the default branch, and it fails until Pages is enabled with "GitHub Actions" as its source:

```shell
gh api --method POST 'repos/{owner}/{repo}/pages' -f build_type=workflow
```

The same is done by hand in the repository settings on GitHub, under **Settings** and **Pages**, by choosing "GitHub Actions" as the source. GitHub Pages needs a public repository, or a paid plan for a private one.

## Related

- [Installing the tools](installing-the-tools.md) — installing and signing in to the GitHub CLI.
- [GitHub workflow](../conventions/github-workflow.md) — what the labels mean and how the settings are used.
- [Documentation website](../tooling/documentation-website.md) — what GitHub Pages publishes.
