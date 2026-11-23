
#region Using Directives

using [[ root_namespace ]];

#endregion

Greeter greeter = new();

Console.WriteLine(greeter.Greet());
Console.WriteLine(greeter.Greet("[[ product_name ]]"));
