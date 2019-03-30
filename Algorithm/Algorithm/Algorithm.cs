using System;
using Pair = System.Tuple<int, int>;
using PairList = System.Collections.Generic.List<System.Tuple<int, int>>;
using Directions = System.Collections.Generic.List<System.Collections.Generic.List<System.Collections.Generic.List<char>>>;
using Bools = System.Collections.Generic.List<System.Collections.Generic.List<bool>>;

namespace Algorithm
{
    public class Algorithm
    {
        private int height;
        private int width;
        Random rand;

        public Algorithm()
        {
            System.Random sysrand = new System.Random();
            int seed = sysrand.Next(1, 99999989);
            Initialize(seed);
        }

        public Algorithm(int seed)
        {
            Initialize(seed);
        }

        private void Initialize(int seed)
        {
            height = 16;
            width = 9;
            rand = new Random(seed);
        }
    }
}
