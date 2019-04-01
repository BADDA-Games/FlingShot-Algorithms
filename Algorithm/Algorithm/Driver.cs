using System;
using Pair = System.Tuple<int, int>;
using PairList = System.Collections.Generic.List<System.Tuple<int, int>>;
using Directions = System.Collections.Generic.List<System.Collections.Generic.List<System.Collections.Generic.List<char>>>;
using Bools = System.Collections.Generic.List<System.Collections.Generic.List<bool>>;

namespace Algorithm
{
    class Driver
    {
        public static void Main(string[] args)
        {
            Algorithm generator = new Algorithm(1345);
            int[,] maze = generator.Generate();
            for(int i = 0; i < 18; i++)
            {
                for(int j = 0; j < 11; j++)
                {
                    Console.Write(maze[i, j] + " ");
                }
                Console.WriteLine("");
            }
        }
    }
}
