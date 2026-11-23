# Setting up GitHub

This article covers what to set up on GitHub for the project, once its repository exists there: its labels, its repository settings, GitHub Pages for the documentation website, [% if publish_to_nuget %]the trusted publishing to NuGet, [% endif %]and, optionally, its branch protection. All of it is done with the [GitHub CLI](installing-the-tools.md#the-github-cli), as scripts to run from a clone of the repository, so that the repository gets them exactly as documented. Running a script again is safe, since every command sets a value rather than adding one.

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

[%- if publish_to_nuget %]

## NuGet Trusted Publishing

The release workflow publishes every release to nuget.org through NuGet's [trusted publishing](https://learn.microsoft.com/nuget/nuget-org/trusted-publishing) (see [continuous integration](../tooling/continuous-integration.md#release-workflow)). No API key is stored in the repository. Instead, the workflow's publish job exchanges a token that GitHub issues for the run for a temporary API key, which nuget.org only hands out to a workflow that a trusted publishing policy names, and which is valid for an hour.

First, check that the package ID, `[[ package_id ]]`, is still free: nuget.org reports that `https://www.nuget.org/packages/[[ package_id ]]` does not exist. Then sign in to nuget.org, choose **Trusted Publishing** from the menu under the user name, and add a policy:

- **Policy owner:** the user, or the nuget.org organization that will own the package. A policy owned by an organization stops working when the user who created it leaves the organization.
- **Scopes:** allow publishing new packages, so that the first release can create the package, and new versions of existing packages, limited to the package ID `[[ package_id ]]`.
- **Repository owner** and **repository:** the user or organization and the name of the repository at <[[ repository_url ]]>.
- **Workflow file:** `release.yml`, the file name only, without `.github/workflows/`. Renaming the workflow file breaks the policy.
- **Environment:** `nuget`, the GitHub environment the publish job runs in, so that no other job of the repository can publish.

For a private repository, nuget.org may activate the policy only temporarily, for seven days, until a publish confirms the repository. If no release happens in that time, the policy becomes inactive, and its seven days are restarted on nuget.org.

The workflow logs in with the nuget.org profile name of the user who created the policy, never an email address, which it reads from the `NUGET_USER` secret of the `nuget` environment. Create the environment and the secret, from a clone of the repository:

```shell
gh api --method PUT 'repos/{owner}/{repo}/environments/nuget'
gh secret set NUGET_USER --env nuget --body '<nuget.org profile name>'
```

Optionally, require a reviewer for the environment, under **Settings**, **Environments**, and **nuget**, so that every release waits for someone to approve its publishing before it reaches nuget.org. That needs a public repository, or a paid plan for a private one.

The first release creates the package on nuget.org. If nuget.org refuses it nonetheless, upload that first version by hand at <https://www.nuget.org/packages/manage/upload>, from the GitHub Release, and let the workflow publish every later one.

[%- endif %]

## Branch Protection

Branch protection is optional, and it is only available for a **public repository**, or for a private repository on a **paid GitHub plan**, such as GitHub Pro or GitHub Team. On a free plan, GitHub rejects the script below for a private repository, and nothing is protected. Without it, the rules of the [Git workflow](../conventions/git-workflow.md) and the [GitHub workflow](../conventions/github-workflow.md) still apply, they are just not enforced.

The script protects `[[ default_branch ]]` and `[[ integration_branch ]]` with two rulesets:

- **Protected Branches** forbids force pushes to either branch and deleting it, for everyone.
- **Pull Requests** only lets a change into either branch through a pull request, which is only merged with a merge commit, and only once the required checks have passed: `Run Linters` from the `Linters` workflow, `Run Tests` from the `Tests` workflow, and `Check Source Branch` from the `Pull Requests` workflow (see [continuous integration](../tooling/continuous-integration.md)). The last one fails a pull request into `[[ default_branch ]]` that does not come from `[[ integration_branch ]]`, which is what stops a pull request that was opened against `[[ default_branch ]]` by mistake, such as a Dependabot security update, from being merged there. Repository administrators may bypass this ruleset, because `[[ integration_branch ]]` is [brought back in step](../conventions/git-workflow.md#bringing-the-integration-branch-back-in-step) with `[[ default_branch ]]` by a direct push after every release.

A ruleset is identified by its name, so the script updates a ruleset that already exists instead of creating a second one:

```shell
apply_ruleset() {
    id=$(gh api 'repos/{owner}/{repo}/rulesets' --jq ".[] | select(.name == \"$1\") | .id")
    if [ -n "$id" ]; then
        gh api --method PUT "repos/{owner}/{repo}/rulesets/$id" --input - > /dev/null
    else
        gh api --method POST 'repos/{owner}/{repo}/rulesets' --input - > /dev/null
    fi
}

apply_ruleset 'Protected Branches' <<'EOF'
{
    "name": "Protected Branches",
    "target": "branch",
    "enforcement": "active",
    "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH", "refs/heads/[[ integration_branch ]]"], "exclude": [] } },
    "rules": [{ "type": "deletion" }, { "type": "non_fast_forward" }]
}
EOF

apply_ruleset 'Pull Requests' <<'EOF'
{
    "name": "Pull Requests",
    "target": "branch",
    "enforcement": "active",
    "bypass_actors": [{ "actor_type": "RepositoryRole", "actor_id": 5, "bypass_mode": "always" }],
    "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH", "refs/heads/[[ integration_branch ]]"], "exclude": [] } },
    "rules": [
        {
            "type": "pull_request",
            "parameters": {
                "required_approving_review_count": 0,
                "dismiss_stale_reviews_on_push": false,
                "require_code_owner_review": false,
                "require_last_push_approval": false,
                "required_review_thread_resolution": false,
                "allowed_merge_methods": ["merge"]
            }
        },
        {
            "type": "required_status_checks",
            "parameters": {
                "strict_required_status_checks_policy": false,
                "do_not_enforce_on_create": false,
                "required_status_checks": [
                    { "context": "Run Linters" },
                    { "context": "Run Tests" },
                    { "context": "Check Source Branch" }
                ]
            }
        }
    ]
}
EOF
```

The actor `5` in `bypass_actors` is GitHub's built-in repository role "Admin", and `~DEFAULT_BRANCH` stands for the default branch, whatever its name.

A required check is named after a job, not after its workflow, so renaming one of these jobs means changing the script and running it again, or every pull request waits for a check that never comes. The workflows never skip a job either, since GitHub counts a skipped job as a passed check. That is why the `Linters` and `Tests` workflows run on pull requests and on pushes to the two protected branches only, rather than on every push (see [continuous integration](../tooling/continuous-integration.md#when-the-linters-and-tests-workflows-run)).

## Related

- [Installing the tools](installing-the-tools.md) — installing and signing in to the GitHub CLI.
- [GitHub workflow](../conventions/github-workflow.md) — what the labels mean and how the settings are used.
- [Documentation website](../tooling/documentation-website.md) — what GitHub Pages publishes.
