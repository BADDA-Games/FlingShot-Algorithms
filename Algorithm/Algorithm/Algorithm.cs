using System;
using Pair = System.Tuple<int, int>;
using PairList = System.Collections.Generic.List<System.Tuple<int, int>>;
using Directions = System.Collections.Generic.List<System.Collections.Generic.List<System.Collections.Generic.List<char>>>;
using Bools = System.Collections.Generic.List<System.Collections.Generic.List<bool>>;

namespace Algorithm
{
    public class Algorithm
    {
        // Initial seed, not current seed!
        public int Seed { get; }
        public int Level { get; set; }

        private int height;
        private int width;
        private GridGraph gg;
        private Random rand;

        public Algorithm()
        {
            System.Random sysrand = new System.Random();
            Seed = sysrand.Next(1, 99999989);
            Initialize();
        }

        public Algorithm(int seed)
        {
            Seed = seed;
            Initialize();
        }

        private void Initialize()
        {
            height = 16;
            width = 9;
            Level = 1;
            rand = new Random(Seed);
        }

        public void Generate()
        {
            gg = new GridGraph(width, height);
            Build();
            Level++;
        }

        private void Build()
        {
            gg.DebugArray();
            //Printer.PrintGridGraph(gg);
        }
    }
}
