# Getting Started

This article covers using [[ product_name ]] for the first time.

## The First Call

Replace this section with a walkthrough of the library's real entry point. The shape to aim for is a task-ordered narrative — what a consumer does first, then next — with a short fenced `csharp` block per step, rather than a reference listing of every type. The XML documentation comments, which a consumer sees in the editor, already cover the exhaustive surface, so this manual's job is to show the path through it.

The type a freshly generated project ships with is a placeholder that exists so the build and this documentation all run end to end:

```csharp
using [[ root_namespace ]];

Greeter greeter = new();

Console.WriteLine(greeter.Greet());          // Hello, world!
Console.WriteLine(greeter.Greet("Ada"));     // Hello, Ada!
```

A salutation can be supplied instead of the default:

```csharp
Greeter greeter = new("Good morning");

Console.WriteLine(greeter.Greet("Ada"));     // Good morning, Ada!
```

See [`source/sample-app/Program.cs`](../../source/sample-app/Program.cs) for the runnable version of the above, and run it with `dotnet run --project "source/sample-app/[[ product_name ]] Sample App.csproj"`.

## What's Missing Today

Keep an honest list here of what the library does not do yet, so that a reader evaluating it does not have to discover the gaps by trying them. Delete the section once there is nothing left to put in it.

## Related

- [Architecture](../developer-manual/architecture.md) — how the project and its packages are laid out.
- [Contributing](../developer-manual/contribution-guide.md) — how to propose a change.
