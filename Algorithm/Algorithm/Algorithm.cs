using System;
using System.Collections.Generic;
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

        bool valid;
        bool copy;

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
            Iterate();
            //gg.DetermineExtraPaths(rand);
            gg.DebugArray();
        }

        private void Iterate()
        {
            void Process(GridGraph g)
            {
                valid = false;
                List<Tuple<Pair, int>> dists = g.Distance;
                while (!valid)
                {
                    if(dists.Count == 0)
                    {
                        Console.WriteLine("ERROR - No good vertices.");
                        return;
                    }
                    List<int> probabilities = MapProbability(dists);
                    PairList ranges = MakeRanges(probabilities);
                    int choice = rand.ChooseFrom(ranges);
                    Pair vertex = dists[choice].Item1;
                    if(vertex != null)
                    {
                        //Console.WriteLine(vertex.Item1 + " " + vertex.Item2);
                        if(TryBuild(g, vertex))
                        {
                            Check(g);
                        }
                        else
                        {
                            dists.RemoveAt(choice);
                        }
                    }
                    else
                    {
                        Console.WriteLine("ERROR - Could not choose a vertex.");
                        return;
                    }
                }
            }

            //TODO change to another looping condition
            for (int i = 0; i < 3; i++)
            {
                copy = false;
                GridGraph other = new GridGraph(gg);
                Process(other);
                if (copy)
                {
                    gg = other;
                    //TODO remove below lines
                    //gg.DebugArray();
                    //Console.WriteLine("");
                }
            }
        }

        private List<int> MapProbability(List<Tuple<Pair, int>> dists)
        {
            List<int> probabilities = new List<int>();
            foreach(Tuple<Pair, int> d in dists)
            {
                int l = d.Item2;
                probabilities.Add(1 + 2 * l * l);
            }
            return probabilities;
        }

        private PairList MakeRanges(List<int> probabilities)
        {
            int cur = 0;
            PairList ranges = new PairList();
            foreach(int p in probabilities)
            {
                ranges.Add(new Pair(cur, cur+p-1));
                cur += p;
            }
            return ranges;
        }

        private bool TryBuild(GridGraph g, Pair v)
        {
            List<char> built = new List<char>();
            foreach(char c in g.BuiltDirections[v.Item1, v.Item2])
            {
                built.Add(c);
            }
            List<char> movable = new List<char>();
            foreach(char c in g.MovableDirections[v.Item1, v.Item2])
            {
                movable.Add(c);
            }
            char initial = g.InitialBuiltDirections[v.Item1, v.Item2];
            // Special case for cell right below exit
            if(v.Equals(new Pair(g.Width / 2, 0)) && movable.Count == 1 && movable[0] == 'D')
            {
                return false;
            }
            List<char> good = new List<char>();
            foreach(char c in g.PotentialDirections(v))
            {
                good.Add(c);
            }
            if (initial == 'U' || initial == 'D')
            {
                if (good.Contains('U'))
                {
                    good.Remove('U');
                }
                if (good.Contains('D'))
                {
                    good.Remove('D');
                }
            }
            else if(initial == 'L' || initial == 'R')
            {
                if (good.Contains('L'))
                {
                    good.Remove('L');
                }
                if (good.Contains('R'))
                {
                    good.Remove('R');
                }
            }
            foreach(char c in built)
            {
                if (good.Contains(c))
                {
                    good.Remove(c);
                }
            }
            List<int> probabilities = new List<int>();
            foreach (char c in good)
            {
                //Console.WriteLine(c);
                switch (c)
                {
                    case 'U':
                        probabilities.Add(3);
                        break;
                    case 'L':
                        probabilities.Add(2);
                        break;
                    case 'R':
                        probabilities.Add(2);
                        break;
                    case 'D':
                        probabilities.Add(1);
                        break;
                }
            }
            while(good.Count > 0)
            {
                PairList ranges = MakeRanges(probabilities);
                int choice = rand.ChooseFrom(ranges);
                char dir = good[choice]; // Ha!
                // TODO change 1 to some general function for n
                int max_length = g.LongestPath(v, dir, 1);
                if (dir == 'D')
                {
                    max_length = Math.Min(max_length, 4);
                }
                else
                {
                    max_length = Math.Min(max_length, 6);
                }
                int length = rand.Generate(1, max_length);
                g.BuildPath(v, dir, length);
                return true;
                //TODO we want to try all directions, not just the one we first select
            }
            return false;

        }

        private void Check(GridGraph g)
        {
            Pair start = g.Start;
            int x = start.Item1;
            int y = start.Item2;
            bool left = g.is_wall[x - 1, y];
            bool right = g.is_wall[x + 1, y];
            bool up = g.is_wall[x, y - 1];
            if(!(left || right || up))
            {
                return;
            }
            //Console.WriteLine("New: " + g.Complexity());
            //Console.WriteLine("Old: " + gg.Complexity());
            //TODO proper looping condition?
            if(g.vertices.Count < 8 || g.Complexity() >= gg.Complexity())
            {
                valid = true;
                copy = true;
            }
           
        }
    }
}
