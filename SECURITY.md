# Security Policy

## What a Vulnerability in a Template Looks Like

The template is never run as a program of its own. A vulnerability in it is something it hands to every project generated from it: a workflow that grants more permissions than it needs, an action or a dependency with a known vulnerability, an unsafe Copier feature that would force consumers to render with `--trust`, or a configuration that leaks a secret. A vulnerability in a project generated from the template is reported to that project instead, unless the template is its cause.

## Supported Versions

The template has a single maintained line of development. Only the most recent release receives security fixes, and a generated project picks them up with `copier update` (see [rendering and updating](docs/project-template/rendering-and-updating.md)). There is no long-term-support version to backport to.

## Reporting a Vulnerability

**Do not open a public issue for a security vulnerability.** Instead, use the repository host's private vulnerability reporting: on GitHub, go to the **Security** tab and choose **Report a vulnerability**. If that is not available to you, contact the owner of the repository directly, through the contact details on the [lecode-official](https://github.com/lecode-official) GitHub profile, rather than filing a public issue.

Please include as much of the following as you can:

- The affected template version, or the commit hash.
- The answers used to render the project, or the steps to reproduce the issue.
- The impact you believe the vulnerability has on a generated project.

There is no formal Service Level Agreement on response times, but reports are taken seriously and handled as promptly as possible. A fix, once available, is released and noted in [`CHANGELOG.md`](CHANGELOG.md). Credit is given to the reporter there unless anonymity is requested.

## Related

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to contribute a fix once a vulnerability is disclosed.
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — community standards for all interactions, including security reports.
