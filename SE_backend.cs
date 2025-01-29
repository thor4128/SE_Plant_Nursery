// See https://aka.ms/new-console-template for more information
// C# Hello World Program
using System;

class Backend {

    // Main Method
    static void Main(string[] args)
    {

        // "printing Hello World"
        //Console.WriteLine("Hello, World!");

        if(args.Length < 2 || args.Length > 2){
            Console.WriteLine("You didnt provide the nessecary information");
            return;
        }
        

        string environment = args[0];
        string garden_size = args[1];
        Console.WriteLine(environment);
        Console.WriteLine(garden_size);

        Console.WriteLine("got it" + " " + environment + " , " + garden_size);
        //return;//("here {environment}, {garden_size}");
        //return("got it {environment}, {garden_size}");
        
    }
}