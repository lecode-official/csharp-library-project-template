# Tooling

This section gives an overview of the tools used for development:

1. [Developer Setup](developer-setup.md)

## The Tools

- **Compiling:** the .NET SDK itself. There is no separate type-check step, because the compiler *is* the type check — `dotnet build` is what catches a type error.

## How to Run

```shell
dotnet build "source/[[ product_name ]].slnx"                                   # build the solution
dotnet run --project "source/sample-app/[[ product_name ]] Sample App.csproj"   # run the sample app
```

## Related

- [Conventions](../conventions/README.md) — what the reviewers enforce.
- [Architecture](../architecture.md) — the projects these tools run against.
