
namespace [[ root_namespace ]];

/// <summary>
/// Represents a greeter, which composes a greeting for a name. This type exists so that a freshly generated project builds, tests, and documents
/// itself end to end. Replace it with the library's real entry point, and take the shape of this file as the pattern to follow (see C# Style).
/// </summary>
public sealed class Greeter
{
    #region Constructors

    /// <summary>
    /// Initializes a new instance of the <see cref="Greeter"/> class.
    /// </summary>
    /// <param name="salutation">
    /// The salutation that every greeting starts with, for example <c>Hello</c>. When it is <see langword="null"/>, the default salutation is used.
    /// </param>
    /// <exception cref="ArgumentException">
    /// Thrown when <paramref name="salutation"/> is empty or consists only of white-space characters.
    /// </exception>
    public Greeter(string? salutation = null)
    {
        if (salutation is not null && string.IsNullOrWhiteSpace(salutation))
            throw new ArgumentException("The salutation must not be empty.", nameof(salutation));

        this.salutation = salutation ?? DefaultSalutation;
    }

    #endregion

    #region Public Constants

    /// <summary>
    /// Contains the salutation that is used when no other salutation was specified.
    /// </summary>
    public const string DefaultSalutation = "Hello";

    #endregion

    #region Private Fields

    /// <summary>
    /// Contains the salutation that every greeting produced by this instance starts with.
    /// </summary>
    private readonly string salutation;

    #endregion

    #region Public Methods

    /// <summary>
    /// Composes a greeting for the specified name.
    /// </summary>
    /// <param name="name">The name to greet. When it is <see langword="null"/>, the greeting addresses the world instead.</param>
    /// <returns>Returns the composed greeting, for example <c>Hello, world!</c>.</returns>
    public string Greet(string? name = null) => $"{this.salutation}, {name ?? "world"}!";

    #endregion
}
