using System;
using Pair = System.Tuple<int, int>;
using PairList = System.Collections.Generic.List<System.Tuple<int, int>>;
using Directions = System.Collections.Generic.List<System.Collections.Generic.List<System.Collections.Generic.List<char>>>;
using Bools = System.Collections.Generic.List<System.Collections.Generic.List<bool>>;

namespace Algorithm
{
    public class Printer
    {
        public static void PrintGridGraph(GridGraph gg)
        {
            int[,] nums = gg.GetCellArray();
            for(int i=0; i<gg.Height; i++)
            {
                for(int j=0; j<gg.Width; j++)
                {
                    if(nums[j, i] == 1)
                    {
                        Console.ForegroundColor = ConsoleColor.DarkGray;
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                    }
                    Console.Write(nums[j, i]+" ");
                }
                Console.WriteLine();
                Console.ForegroundColor = ConsoleColor.White;
            }
        }
    }
}
