// See https://aka.ms/new-console-template for more information
// C# Hello World Program

using System;
using System.Text.Json;

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
        //Console.WriteLine(environment);
        //Console.WriteLine(garden_size);

        //Console.WriteLine("got it" + " " + environment + " , " + garden_size);
        //return;//("here {environment}, {garden_size}");
        //return("got it {environment}, {garden_size}");
        
        //call method to return list
        return_list(environment, garden_size);
        
    }

    static void return_list(string environment, string garden_size){
        
        //load list with what wants to be returned to python GUI
        string[] list = [environment, garden_size];
        
        //need to use serialize with json to send back information to GUI
        string list_to_return = JsonSerializer.Serialize(list);

        //this does not actually print to terminal this is picked up by python file 
        //this is basically a method call to python file sending an array to python file to parse
        Console.WriteLine(list_to_return);
    }
}