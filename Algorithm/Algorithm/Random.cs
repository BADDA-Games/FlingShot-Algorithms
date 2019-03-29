using System;
using System.Collections.Generic;

namespace Algorithm
{
    public class Random
    {
        int seed;
        int InitialSeed { get; }

        public Random(int seed)
        {
            this.seed = seed;
        }

        public int Generate(int low, int high)
        {
            int mod = high - low + 1;
            if(seed < 1)
            {
                seed = ((low + high - seed + 1999) * 1582307) % 55555333;
            }
            seed = (3515366 * seed + 12345) % 99999989;
            int value = (seed % mod) + low;
            return value;
        }
        Tuple<int, int> ChooseFrom(List<Tuple<int, int>> ranges)
        {
            int choice = Generate(ranges[0].Item1, ranges[ranges.Count-1].Item2);
            foreach(Tuple<int, int> t in ranges)
            {
                if(Util.Between(choice, t))
                {
                    return t;
                }
            }
            return null;
        }
    }
}
