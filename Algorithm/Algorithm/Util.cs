using System;
using System.Collections.Generic;
using Pair = System.Tuple<int, int>;
using PairList = System.Collections.Generic.List<System.Tuple<int, int>>;
using Directions = System.Collections.Generic.List<System.Collections.Generic.List<System.Collections.Generic.List<char>>>;
using Bools = System.Collections.Generic.List<System.Collections.Generic.List<bool>>;

namespace Algorithm
{
    static public class Util
    {
        public static List<T> AddIfMissing<T>(T element, List<T> list)
        {
            foreach(T i in list)
            {
                if (element.Equals(i))
                {
                    return list;
                }
            }
            list.Add(element);
            return list;
        }

        public static Pair MinMax(int v1, int v2)
        {
            int smaller, larger;
            if (v1 <= v2)
            {
                smaller = v1;
                larger = v2;
            }
            else
            {
                smaller = v2;
                larger = v1;
            }
            return Tuple.Create(smaller, larger);
        }

        public static Pair MinMax(Pair t)
        {
            int smaller, larger;
            if (t.Item1 <= t.Item2)
            {
                smaller = t.Item1;
                larger = t.Item2;
            }
            else
            {
                smaller = t.Item2;
                larger = t.Item1;
            }
            return Tuple.Create(smaller, larger);
        }

        public static PairList SortTuplesX(PairList list)
        {
            list.Sort((t1, t2) => t1.Item1.CompareTo(t2.Item1));
            return list;
        }

        public static PairList SortTuplesY(PairList list)
        {
            list.Sort((t1, t2) => t1.Item2.CompareTo(t2.Item2));
            return list;
        }

        public static int Floor(double n)
        {
            return (int) n;
        }

        public static bool Between(int n, Pair tuple)
        {
            Pair sorted = MinMax(tuple);
            int smaller = sorted.Item1;
            int larger = sorted.Item2;
            return (smaller <= n) && (n <= larger);
        }

        public static T2 Lookup<T1, T2>(T1 search, List<Tuple<T1, T2>> dict)
        {
            foreach(Tuple<T1, T2> t in dict)
            {
                if (search.Equals(t.Item1))
                {
                    return t.Item2;
                }
            }
            return default(T2);
        }
    }
}
