
namespace [[ root_namespace ]].UnitTests;

/// <summary>
/// Represents tests for the <see cref="Greeter"/> class.
/// </summary>
public sealed class GreeterTests
{
    #region Public Methods

    /// <summary>
    /// Tests that a greeter created without an explicit salutation falls back to <see cref="Greeter.DefaultSalutation"/>, so that the common case
    /// needs no configuration at all.
    /// </summary>
    [Fact]
    public void GreetNoSalutationUsesTheDefaultSalutation()
    {
        Greeter greeter = new();

        string greeting = greeter.Greet("Ada");

        Assert.Equal($"{Greeter.DefaultSalutation}, Ada!", greeting);
    }

    /// <summary>
    /// Tests that an explicitly specified salutation replaces the default one, which is the whole reason the constructor takes it.
    /// </summary>
    [Fact]
    public void GreetCustomSalutationUsesIt()
    {
        Greeter greeter = new("Good morning");

        string greeting = greeter.Greet("Ada");

        Assert.Equal("Good morning, Ada!", greeting);
    }

    /// <summary>
    /// Tests that omitting the name addresses the world, so that a caller with nothing to greet still gets a well-formed greeting rather than an
    /// exception or an empty name.
    /// </summary>
    [Fact]
    public void GreetNoNameGreetsTheWorld()
    {
        Greeter greeter = new();

        string greeting = greeter.Greet();

        Assert.Equal($"{Greeter.DefaultSalutation}, world!", greeting);
    }

    /// <summary>
    /// Tests that a salutation consisting only of white-space characters is rejected at construction time rather than silently producing a greeting
    /// that starts with blanks. The empty string and a blank string are both covered, because the guard treats them alike.
    /// </summary>
    /// <param name="salutation">The invalid salutation that is expected to be rejected.</param>
    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    public void ConstructorBlankSalutationThrows(string salutation)
    {
        ArgumentException exception = Assert.Throws<ArgumentException>(() => new Greeter(salutation));

        Assert.Equal("salutation", exception.ParamName);
    }

    #endregion
}
