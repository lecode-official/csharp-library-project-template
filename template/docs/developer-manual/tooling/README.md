# Tooling

This section gives an overview of the tools used for development:

1. [Developer Setup](developer-setup.md)
2. [Testing and Code Coverage](testing-and-code-coverage.md)

## The Tools

- **Compiling and testing:** the .NET SDK itself. There is no separate type-check step, because the compiler *is* the type check — `dotnet build` and `dotnet test` are what catch a type error (see [testing and code coverage](testing-and-code-coverage.md)).

## How to Run

```shell
dotnet build "source/[[ product_name ]].slnx"                                   # build the solution
dotnet test --solution "source/[[ product_name ]].slnx"                         # run the unit tests
dotnet run --project "source/sample-app/[[ product_name ]] Sample App.csproj"   # run the sample app
```

## Related

- [Conventions](../conventions/README.md) — what the reviewers enforce.
- [Architecture](../architecture.md) — the projects these tools run against.
