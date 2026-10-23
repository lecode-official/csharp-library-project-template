# Developer Setup

This article covers what to install before building [[ product_name ]] locally.

## .NET SDK

Install the exact .NET SDK version pinned in [`global.json`](../../../global.json) from the [.NET downloads page](https://dotnet.microsoft.com/download). `global.json` sets `rollForward` to `disable`, so a mismatched version fails outright rather than silently substituting a different one.

## Related

- [Tooling](README.md) — what each installed tool does.
