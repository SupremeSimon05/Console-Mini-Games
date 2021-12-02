using System;

class main
{
    static void print(string str, string end = "\n"){
        Console.Write(str+end);
    }
    static void mvcr(int x, int y){
        print("\033["+y+";"+x+"H");
    }
    static void Main()
    {
        
        
    }
}

