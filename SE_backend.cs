//Author Kody Ryant, Hunter Lathan
//Software Engineering
//backend to handle algorithm to find plants that fit in given dimensions

using System;
using System.Xml;
using System.Text.Json;
using System.Linq;
using System.Xml.Linq;


class Backend {

    // Main Method
    static void Main(string[] args)
    {

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
        //string[] list = [environment, garden_size]
        //string[] list = new string[] {environment, garden_size};

        //parse string for garden size
        //fix case sensitivity
        garden_size.ToLower();
        string[] sizes = garden_size.Split('x'); //make sure this stays lower case x
        

        //should have error detection in the GUI for this 
        if (sizes.Length != 3){
            Console.WriteLine(JsonSerializer.Serialize(new List<string> {"Improper garden dimensions"}));
            return;
        }

        //double length = double.Parse(sizes[0]);
        //double depth = double.Parse(sizes[1]);
        double height = double.Parse(sizes[2]);

        // we can determine size based off of volume?
        //probably not

//these sizes are in meters (for now)

        if(height >= 1.0){//dont think depth matters here really since its already over the previous depth
            //large
            //length lets us know how much space we have or how many plants can fit in a given area
            //want to grab collections from large then from medium then from small then display message saying thats all our options
            xml_helper(environment, "large");

        }
        else if(height >= 0.4 && height < 1.0){//medium
            //length lets us know how much space we have or how many plants can fit in a given area
            //want to grab collections from medium then small then display message saying thats all our options
            xml_helper(environment, "medium");

        }
        else{
            //small
            //length lets us know how much space we have or how many plants can fit in a given area
            //want to grab collections from small then display message saying thats all options we have

            //helper function
            xml_helper(environment, "small");

        }
    }

    static void xml_helper(string environment, string size){

        string list_return = "";
        int collection = -1;

        // Assign collection value range based on size
        if (size == "small") collection = 4;
        if (size == "medium") collection = 9;
        if (size == "large") collection = 14;


        //Load XML document
        XDocument xmlDoc = null;

        if (environment == "Indoor")
        {
        xmlDoc = XDocument.Load("Indoor.xml");
        }

        else
        {
        xmlDoc = XDocument.Load("Outdoor.xml");
        }

        while (collection >= 0) // Loop through collections from the assigned value down to 0
        {
        // Console.WriteLine($"Searching for collection {collection}..."); // Output which collection is being searched

            foreach (var coll in xmlDoc.Descendants("collection"))
            {
                int? collNumber = (int?)coll.Attribute("number");
                if (collNumber == collection) // If collection matches, retrieve names
                {
                    //Console.WriteLine($"Found Collection: {collection}");
    
                    // Output contents of the collection
                    var careElement = coll.Element("care")?.Value ?? "Unknown";     //default value for the rare case that the XML
                    var lengthElement = coll.Element("length")?.Value ?? "Unknown"; //doesnt contain the values requested.
                    var imageElement = coll.Element("image")?.Value.Replace("\u0022", "") ?? "Unknown"; //replacing unicode"
                    foreach (var name in coll.Elements("name"))
                    {
                        //Console.WriteLine($"Name: {name.Value}");
                        list_return += "name: " +  name.Value  + " length: " + lengthElement + 
                         " care: " + careElement + " image: " + imageElement + " ";
                    }


                }
            }
            collection--; // Move to the next lower collection number
        }

            //Console.WriteLine(list_return);
            string list_to_return = JsonSerializer.Serialize(list_return);

            //this does not actually print to terminal this is picked up by python file 
            //this is basically a method call to python file sending an array to python file to parse
            Console.WriteLine(list_to_return);

            //return list_return.TrimEnd(',', ' '); // Remove trailing comma and space
    }

}