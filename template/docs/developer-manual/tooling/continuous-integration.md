# Continuous Integration

This article covers the GitHub Actions workflows in [`.github/workflows/`](../../../.github/workflows/): [`linters.yml`](../../../.github/workflows/linters.yml), [`tests.yml`](../../../.github/workflows/tests.yml), [`pull-requests.yml`](../../../.github/workflows/pull-requests.yml), [`dependabot-security-updates.yml`](../../../.github/workflows/dependabot-security-updates.yml), and [`docs.yml`](../../../.github/workflows/docs.yml), and the [Dependabot configuration](../../../.github/dependabot.yml) that keeps their pinned versions current. The workflows are independent of each other — any one can fail, be re-run, or be extended without touching the others, and a commit or pull request shows them as separate checks.

A project hosted somewhere other than GitHub replaces these files with the equivalent for its own platform. What the workflows *do* is the part worth keeping: the same tools, the same pinned versions, the same never-stop-at-the-first-failure behavior.

## What Every Workflow Shares

- **Least-privilege permissions.** Each workflow declares `permissions` explicitly instead of inheriting the repository's or organization's default, which may be write access to everything. The linters and tests workflows get `contents: read` and nothing else, the pull requests workflow gets no permission at all, and the Dependabot security updates workflow gets `pull-requests: write` alone, since it changes a pull request. The docs workflow additionally gets `pages: write` and `id-token: write`, which the GitHub Pages deployment needs.
- **A timeout on every job.** `timeout-minutes` stops a run that hangs instead of letting it use up GitHub's default limit of six hours.
- **Actions pinned to a commit SHA.** Every action is referenced by the full commit SHA of a release, with the version in a comment next to it, because a tag can be moved to point at different code, while a commit SHA cannot. [Dependabot](#dependabot) keeps the pins up to date.
- **Versions read from the repository.** The Node.js version is read from [`.nvmrc`](../../../.nvmrc) and the .NET SDK version from [`global.json`](../../../global.json), rather than being written into a workflow. A version duplicated in two places is a version that eventually disagrees with itself.

## When the Linters and Tests Workflows Run

Both run on every `pull_request`, and on every `push` to `[[ default_branch ]]` and `[[ integration_branch ]]`:

```yaml
on:
  push:
    branches:
      - "[[ default_branch ]]"
      - "[[ integration_branch ]]"
  pull_request:
```

A pull request is checked by the `pull_request` event, whether it comes from a branch of this repository or from a fork, whose pushes happen in another repository. A push to a work branch runs nothing on its own, since its pull request checks it, and the pushes to the two protected branches check what the merge of a pull request produced. So every check runs once, and no job has to be skipped to avoid checking a pull request twice. That matters once the branches are [protected](../development-setup/setting-up-github.md#branch-protection): GitHub counts a job that was skipped by its condition as a passed check, so a skipped job with the same name as a required check would let a pull request through, whatever the other run found. Open a draft pull request early to have a work branch checked before it is ready.

A `concurrency` group per workflow and ref cancels a run that is still in progress when a newer commit arrives on the same branch or pull request, since only the result for the newest commit matters.

## Linters Workflow

A single job on the latest Ubuntu runner checks out the repository, installs Node.js, runs `npm ci`, and then runs each check as its own step, through the same npm scripts a developer runs locally: `npm run lint:dprint`, `npm run lint:markdownlint`, and `npm run lint:cspell`. It does not set up .NET, because none of these tools needs it. The C# code is checked by the analyzers in the tests workflow's build instead.

Every step after the first carries `if: ${{ !cancelled() }}`, so a single failing tool does not hide the findings of the ones after it. One run reports everything it can, which is the same reason `npm run lint` uses `run-s --continue-on-error` (see [tooling](README.md)). Each check being its own step also shows at a glance which tool failed.

Formatting is checked with `dprint check "**/*"`, which verifies that every file dprint covers is already formatted and, unlike `dprint fmt`, never modifies one.

`npm ci` fails instead of silently updating `package-lock.json` when it no longer matches `package.json`, and it fails outright when there is no `package-lock.json` at all, so the lock file has to be committed (see [dependency management](../conventions/dependency-management.md)). Together with `npx` resolving the pinned versions out of `node_modules`, that is what makes a local pass reliably predict a green run.

## Tests Workflow

A separate workflow rather than a step in the linters one, so that "the tests failed" and "a linter failed" are two different signals. Its single job installs the .NET SDK, then:

1. **Restores in `--locked-mode`.** A package change that was not restored and committed locally fails the restore rather than silently resolving a different dependency graph.
2. **Verifies that the lock files are committed.** `--locked-mode` only compares against lock files that exist. When a project has none, the restore succeeds and simply writes one, so a project whose `packages.lock.json` was never committed would pass the step above without anything being checked. The "Verify Lock Files Are Committed" step therefore fails whenever `git status --porcelain -- '**/packages.lock.json'` reports anything, which means the restore created or changed a lock file that is missing from or outdated in the commit (see [dependency management](../conventions/dependency-management.md)).
3. **Builds and tests in the Release configuration**, with coverage collection. Release is what turns every analyzer warning into an error (see [static code analysis](static-code-analysis.md)), so a warning that is tolerated while working locally fails the check.
4. **Reports the coverage.** A ReportGenerator summary is written into the run's own summary page, and the full HTML report is uploaded as an artifact (see [testing and code coverage](testing-and-code-coverage.md)).

There is no enforced minimum coverage percentage that fails the build. See [testing](../conventions/testing.md) for what is expected of a change instead of a numeric threshold.

## Pull Requests Workflow

A single job, `Check Source Branch`, which fails a pull request into `[[ default_branch ]]` unless it comes from the `[[ integration_branch ]]` branch of this repository, as the [GitHub workflow](../conventions/github-workflow.md#pull-requests) requires. A pull request into any other branch passes it. It runs when a pull request is opened, reopened, or pushed to, and when it is edited, since changing a pull request's base branch is an edit, so a pull request that is moved onto `[[ default_branch ]]` is checked again. It needs neither a checkout nor any permission, because it only reads the branch names from the event.

The check only stops anything once a ruleset requires it (see [branch protection](../development-setup/setting-up-github.md#branch-protection)). Then a pull request opened against `[[ default_branch ]]` by mistake cannot be merged there until its base branch is changed to `[[ integration_branch ]]`. For a Dependabot security update, the next workflow changes it.

## Dependabot Security Updates Workflow

Dependabot applies `target-branch` and `labels` only to version updates, so it opens a security update against `[[ default_branch ]]` and without a label. A single job, `Retarget Security Update`, points such a pull request at `[[ integration_branch ]]` and gives it the `Dependabot:` label of its ecosystem as soon as it is opened (see [GitHub workflow](../conventions/github-workflow.md#dependabot-pull-requests)). It only acts on a pull request into `[[ default_branch ]]` that Dependabot opened from a branch of this repository, and skips every other one.

It runs on `pull_request_target` rather than `pull_request`, because a workflow that Dependabot triggers on `pull_request` gets a read-only token, which cannot change the pull request. `pull_request_target` runs the workflow as it is on `[[ default_branch ]]`, with a token of this repository, so the workflow only takes effect once it has reached `[[ default_branch ]]`. What makes it safe is that it never checks out or runs the code of the pull request: `dependabot/fetch-metadata` reads the ecosystem through the API, and verifies that every commit of the pull request comes from Dependabot, and the pull request is changed through the REST API, with `pull-requests: write` as the only permission.

A `case` statement maps Dependabot's name of each ecosystem in [`.github/dependabot.yml`](../../../.github/dependabot.yml) to its label. An ecosystem it does not know still has its pull request pointed at `[[ integration_branch ]]`, and then fails the job, so that the missing label is noticed. A new ecosystem therefore gets its label there, too.

## Docs Workflow

Runs only on pushes to the default branch — unlike the linters and tests workflows, it deploys to GitHub Pages, so it only ever needs to run against what is actually published.

It is split into a build job and a deploy job, so that the deployment goes through the dedicated `github-pages` environment and gets its own audit trail. The build job installs the .NET SDK, restores the local .NET tools, installs the pinned Python dependencies from [`requirements.txt`](../../../requirements.txt), and runs `properdocs build --strict`, which regenerates the API section from the source's own documentation comments (see [documentation website](documentation-website.md)). `--strict` turns every warning into an error, above all a link to a page or file that does not exist, so a broken link fails the deployment instead of being published.

Its concurrency group ensures at most one deployment runs at a time, and an in-progress one is allowed to finish rather than being cancelled, because a cancelled deployment can leave the site partially updated.

## One-Time Setup

The docs workflow cannot deploy until GitHub Pages is enabled for the repository. In the repository's settings, under "Pages", set the source to "GitHub Actions". Until then, the workflow's "Configure Pages" step fails on every push to the default branch.

## Dependabot

[`.github/dependabot.yml`](../../../.github/dependabot.yml) opens a pull request whenever a newer version of a dependency is released. Since every dependency is pinned to an exact version and every action to a commit SHA, nothing is ever upgraded implicitly, and these pull requests are what keeps the pins from going stale.

Every ecosystem is checked once a week: the GitHub Actions actions, the NuGet packages, the .NET SDK in `global.json`, the npm packages, and the Python packages in `requirements.txt`. All updates of an ecosystem are grouped into a single pull request, so the upgrades arrive as one reviewable change per ecosystem instead of a pull request per package, labeled with the `Dependabot:` label of the ecosystem. Such a pull request runs through the same workflows as any other, including the lock-file verification. What a Dependabot pull request cannot do on its own is described in [dependency management](../conventions/dependency-management.md).

## Related

- [Tooling](README.md) — the tools these workflows run.
- [Formatting (dprint)](formatting-dprint.md) — the check-mode invocation.
- [Testing and code coverage](testing-and-code-coverage.md) — the commands the tests workflow runs, in more detail.
- [Static code analysis](static-code-analysis.md) — the rules a Release build enforces.
- [Documentation website](documentation-website.md) — what the docs workflow builds and deploys.
- [Dependency management](../conventions/dependency-management.md) — how the pinned versions these workflows use are kept exact.
