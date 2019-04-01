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

        public int[,] Generate()
        {
            gg = new GridGraph(width, height);
            Build();
            //Printer.PrintGridGraph(gg);
            Level++;
            int[,] fullMap = new int[height + 2, width + 2];
            int[,] cellArray = gg.GetCellArray();

            for(int i = 0; i < width; i++)
            {
                for(int j = 0; j < height; j++)
                {
                    fullMap[j + 1, i + 1] = cellArray[i, j];
                }
            }
            for(int i = 0; i < width + 2; i++)
            {
                fullMap[0, i] = 1;
                fullMap[height + 1, i] = 1;
            }
            for (int j = 1; j < height + 1; j++)
            {
                fullMap[j, 0] = 1;
                fullMap[j, width + 1] = 1;
            }
            fullMap[0, width / 2 + 1] = 0;

            return fullMap;
        }

        private void Build()
        {
            Iterate();
            gg.DetermineExtraPaths(rand);
            //gg.DebugArray();
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
                        //Console.WriteLine("ERROR - No good vertices.");
                        return;
                    }
                    List<int> probabilities = MapProbability(dists);
                    PairList ranges = MakeRanges(probabilities);
                    int choice = rand.ChooseFrom(ranges);
                    Pair vertex = dists[choice].Item1;
                    if(vertex != null)
                    {
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
            for (int i = 0; i < 60; i++)
            {
                copy = false;
                GridGraph other = new GridGraph(gg);
                Process(other);
                if (copy)
                {
                    gg = other;
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
            PairList ranges = new PairList();
            foreach(int p in probabilities)
            {
                if(ranges.Count == 0)
                {
                    ranges.Add(new Pair(0, probabilities[0]));
                }
                else
                {
                    int next = ranges[ranges.Count - 1].Item2 + 1;
                    ranges.Add(new Pair(next, next + p));
                }
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
            char initial = g.InitialBuiltDirection[v.Item1, v.Item2];
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
            foreach (char c in built)
            {
                if (good.Contains(c))
                {
                    good.Remove(c);
                }
            }
            List<int> probabilities = new List<int>();
            foreach (char c in good)
            {
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
            while (good.Count > 0)
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
            if(g.Complexity() >= gg.Complexity())
            {
                valid = true;
                copy = true;
            }
           
        }
    }
}
