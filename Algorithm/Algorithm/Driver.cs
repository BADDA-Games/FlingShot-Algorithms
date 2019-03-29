using System;

namespace Algorithm
{
    class Driver
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            //Console.WriteLine("Press any key to exit.");
            //List<int> list = new List<int>();
            //Util.AddIfMissing(null, null);
            Tuple<int, int> x = Util.MinMax(3, 4);
            Console.WriteLine(x.Item1+x.Item2);
            Console.ReadKey();
        }
    }
}
