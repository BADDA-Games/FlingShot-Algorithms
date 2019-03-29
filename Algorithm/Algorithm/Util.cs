using System;
using System.Collections.Generic;

namespace Algorithm
{
    static public class Util
    {
        public static List<T> AddIfMissing<T>(ref T element, ref List<T> list)
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

        public static Tuple<int, int> MinMax(int v1, int v2)
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

        public static Tuple<int, int> MinMax(Tuple<int, int> t)
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

        public static List<Tuple<int, int>> SortTuplesX(List<Tuple<int, int>> list)
        {
            list.Sort((t1, t2) => t1.Item1.CompareTo(t2.Item1));
            return list;
        }

        public static List<Tuple<int, int>> SortTuplesY(List<Tuple<int, int>> list)
        {
            list.Sort((t1, t2) => t1.Item2.CompareTo(t2.Item2));
            return list;
        }

        public static int Floor(double n)
        {
            return (int) n;
        }

        public static bool Between(int n, Tuple<int, int> tuple)
        {
            Tuple<int, int> sorted = MinMax(tuple);
            int smaller = sorted.Item1;
            int larger = sorted.Item2;
            return (smaller <= n) && (n <= larger);
        }

        //TODO please
        //public static List<Tuple<int, int>> TupleRanges()
    }
}
