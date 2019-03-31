using System;
using System.Collections.Generic;
using Pair = System.Tuple<int, int>;
using PairList = System.Collections.Generic.List<System.Tuple<int, int>>;
using Directions = System.Collections.Generic.List<char>;

namespace Algorithm
{
    public class GridGraph
    {
        public int Width { get; }
        public int Height { get; }
        public Pair Start { get; }

        char[,] InitialBuiltDirections { get; }
        Directions[,] BuiltDirections { get; }
        Directions[,] MovableDirections { get; set; }

        PairList vertices;
        List<Tuple<Pair, int>> distance;
        PairList[,] adj;
        PairList[,] rev;
        bool[,] is_path;
        bool[,] is_unused_path;
        bool[,] is_wall;
        bool[,] is_unused_wall;

        /// <summary>
        /// Initializes a new instance of the <see cref="T:Algorithm.GridGraph"/> class.
        /// </summary>
        /// <param name="width">The width of the grid.</param>
        /// <param name="height">The height of the grid.</param>
        public GridGraph(int width, int height)
        {
            Width = width;
            Height = height;
            Start = Tuple.Create(Width / 2, Height - 1);
            InitialBuiltDirections = new char[width, height];
            MovableDirections = new Directions[width, height];
            BuiltDirections = new Directions[width, height];
            vertices = new PairList();
            distance = new List<Tuple<Pair, int>>();
            adj = new PairList[width, height];
            rev = new PairList[width, height];
            is_path = new bool[width, height];
            is_unused_path = new bool[width, height];
            is_wall = new bool[width, height];
            is_unused_wall = new bool[width, height];
            for (int i = 0; i < width; i++)
            {
                for(int j =0 ; j < height; j++)
                {
                    adj[i, j] = new PairList();
                    rev[i, j] = new PairList();
                    InitialBuiltDirections[i, j] = '\0';
                    BuiltDirections[i, j] = new List<char>();
                    MovableDirections[i, j] = new List<char>();
                    is_path[i,j] = false;
                    is_unused_path[i, j] = false;
                    is_wall[i, j] = false;
                    is_unused_wall[i, j] = false;
                }
            }
            Build(Start, Start);
            Build(new Pair(Width / 2, 0), new Pair(Width / 2, 0));
        }

        /// <summary>
        /// Constructor which copies information from another GridGraph.
        /// </summary>
        /// <param name="other">The other GridGraph instance</param>
        public GridGraph(GridGraph other)
        {
            Width = other.Width;
            Height = other.Height;
            Start = Tuple.Create(Width / 2, Height - 1);
            InitialBuiltDirections = new char[Width, Height];
            MovableDirections = new Directions[Width, Height];
            BuiltDirections = new Directions[Width, Height];
            vertices = new PairList();
            distance = new List<Tuple<Pair, int>>();
            adj = new PairList[Width, Height];
            rev = new PairList[Width, Height];
            is_path = new bool[Width, Height];
            is_unused_path = new bool[Width, Height];
            is_wall = new bool[Width, Height];
            is_unused_wall = new bool[Width, Height];
            for (int i = 0; i < Width; i++)
            {
                for (int j = 0; j < Height; j++)
                {
                    adj[i, j] = new PairList();
                    rev[i, j] = new PairList();
                    BuiltDirections[i, j] = new List<char>();
                    MovableDirections[i, j] = new List<char>();

                    InitialBuiltDirections[i, j] = other.InitialBuiltDirections[i, j];
                    is_path[i, j] = other.is_path[i, j];
                    is_unused_path[i, j] = other.is_unused_path[i, j];
                    is_wall[i, j] = other.is_wall[i, j];
                    is_unused_wall[i, j] = other.is_unused_wall[i, j];

                    foreach(char c in other.BuiltDirections[i, j])
                    {
                        BuiltDirections[i, j].Add(c);
                    }
                    foreach (char c in other.MovableDirections[i, j])
                    {
                        MovableDirections[i, j].Add(c);
                    }
                    foreach(Pair p in other.adj[i, j])
                    {
                        adj[i, j].Add(new Tuple<int, int>(p.Item1, p.Item2));
                    }
                    foreach (Pair p in other.rev[i, j])
                    {
                        rev[i, j].Add(new Tuple<int, int>(p.Item1, p.Item2));
                    }
                }
            }
        }

        /// <summary>
        /// Prints out a debug version of the current Grid structure.
        /// </summary>
        public void DebugArray()
        {
            string[,] arr = new string[Width, Height];
            for(int i=0; i<Height; i++)
            {
                for(int j=0; j<Width; j++)
                {
                    string cur = is_path[j, i] ? "O" : "X";
                    if(cur == "O")
                    {
                        if(!is_unused_path[j, i])
                        {
                            Console.ForegroundColor = ConsoleColor.Green;
                        }
                        else
                        {
                            Console.ForegroundColor = ConsoleColor.DarkGray;
                        }
                    }
                    else if(cur == "X" && is_wall[j, i])
                    {
                        if(!is_unused_wall[j, i])
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                        }
                        else
                        {
                            Console.ForegroundColor = ConsoleColor.DarkGray;
                        }
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.White;
                    }

                    Console.Write(cur + " ");
                }
                Console.WriteLine();
            }
            Console.ForegroundColor = ConsoleColor.White;
        }

        /// <summary>
        /// Outputs the current grid structure, 0 = Wall, 1 = Path
        /// </summary>
        /// <returns>The cell array.</returns>
        public int[,] GetCellArray()
        {
            int[,] arr = new int[Width, Height];
            for(int i=0; i<Width; i++)
            {
                for(int j=0; j<Height; j++)
                {
                    arr[i, j] = is_path[i, j] == true ? 1 : 0;
                }
            }
            return arr;
        }

        /// <summary>
        /// Finds the in-degree of p, the number of vertices which can
        /// move to p in one move.
        /// </summary>
        /// <returns>The in-degree of p.</returns>
        /// <param name="p">A point in the GridGraph.</param>
        public int InDeg(Pair p)
        {
            return rev[p.Item1, p.Item2].Count;
        }

        /// <summary>
        /// Finds the out-degree of p, the number of vertices which can be
        /// reached from p in one move.
        /// </summary>
        /// <returns>The out-degree of p.</returns>
        /// <param name="p">A point in the GridGraph.</param>
        public int OutDeg(Pair p)
        {
            return adj[p.Item1, p.Item2].Count;
        }

        /// <summary>
        /// Finds the least number of moves from the start to reach a vertex v
        /// </summary>
        /// <returns>The depth of vertex v.</returns>
        /// <param name="v">A vertex in the grid.</param>
        public int Depth(Pair v)
        {
            return Util.Lookup(v, distance);
        }

        /// <summary>
        /// Builds a path from f in direction with for length cells.
        /// The length does not include the starting space; a path of length one
        /// occupies an additional cell.
        /// </summary>
        /// <param name="f">A cell to start at</param>
        /// <param name="direction">The direction to move in.</param>
        /// <param name="length">The length of the path.</param>
        public Pair BuildPath(Pair f, char direction, int length)
        {
            if(length > 0 && IsInGrid(f))
            {
                if(direction == 'R')
                {
                    if (f.Item1 + length >= Width)
                    {
                        return Build(f, new Pair(Width - 1, f.Item2));
                    }
                    return Build(f, new Pair(f.Item1 + length, f.Item2));
                }
                if (direction == 'L')
                {
                    if(f.Item1 - length < 0)
                    {
                        return Build(f, new Pair(0, f.Item2));
                    }
                    return Build(f, new Pair(f.Item1 - length, f.Item2));
                }
                if (direction == 'U')
                {
                    if(f.Item2 - length < 0)
                    {
                        return Build(f, new Pair(f.Item1, 0));
                    }
                    return Build(f, new Pair(f.Item1, f.Item2 - length));
                }
                if (direction == 'D')
                {
                    if(f.Item2 + length >= Height)
                    {
                        return Build(f, new Pair(f.Item1, Height - 1));
                    }
                    return Build(f, new Pair(f.Item1, f.Item2 + length));
                }
            }
            return f;
        }

        /// <summary>
        /// Determines if the puzzle is possible to solve, the exit can be
        /// reached if the player plays perfectly.
        /// </summary>
        /// <returns>True if possible, false otherwise</returns>
        public bool Possible()
        {
            return false;
        }

        /// <summary>
        /// Finds all trap vertices, locations which a player can reach from
        /// which they cannot reach the exit ever.
        /// </summary>
        /// <returns>The vertices.</returns>
        public PairList TrapVertices()
        {
            return null;
        }

        /// <summary>
        /// Determines if trap vertices exist, which are locations which a
        /// player can get to where reaching the exit becomes impossible.
        /// </summary>
        /// <returns><c>true</c>true if trap vertices exist, false otherwise.<c>false</c> otherwise.</returns>
        public bool CanGetStuck()
        {
            return false;
        }

        /// <summary>
        /// Computes the length of the fastest path to get from the start
        /// location to any valid ending location, those which can reach the
        /// exit in just one move.
        /// </summary>
        /// <returns>The length of the path.</returns>
        public int FastestPath()
        {
            int x = Width / 2;
            int y = 0;
            for(int i = 0; i < Height; i++)
            {
                if(!is_path[x, i])
                {
                    y = i - 1;
                    break;
                }
            }
            PairList v = VerticesX(x);
            PairList list = new PairList();
            foreach(Pair p in v)
            {
                if(p.Item2 <= y)
                {
                    list.Add(p);
                }
            }
            return ShortestPaths(Start, list);
        }

        /// <summary>
        /// Computes the length of the fastest path to get from vertex p to any
        /// valid ending location, including those above the
        /// specified end_location
        /// </summary>
        /// <returns>The length of the fastest path from p to the end</returns>
        /// <param name="p">A vertex in the GridGraph.</param>
        public int FastestPathFrom(Pair p)
        {
            return -1;
        }

        /// <summary>
        /// Finds all vertices adjacent to a wall <paramref name="p"/>.
        /// </summary>
        /// <returns>A PairList adjacent to <paramref name="p"/>. If
        /// <paramref name="p"/> is not a wall, returns null.</returns>
        /// <param name="p">P.</param>
        public PairList WallOf(Pair p)
        {
            return null;
        }

        /// <summary>
        /// Pseudorandomly determines which pattern to build additional paths in.
        /// </summary>
        /// <param name="r">The random number generator</param>
        public void DetermineExtraPaths(Random r)
        {

        }

        /// <summary>
        /// Determines the longest path from a cell f in <paramref name="direction"/>,
        /// without encountering a defined wall. Will walk through undefined
        /// cells completely unhindered.
        /// </summary>
        /// <returns>The path.</returns>
        /// <param name="f">The vertex to move from.</param>
        /// <param name="direction">The direction to move in.</param>
        /// <param name="walls">Number of walls to walk through.</param>
        public int LongestPath(Pair f, char direction, uint walls)
        {
            return -1;
        }

        /// <summary>
        /// The complexity of the adjacency list, based on the definition 
        /// derived by Neel and Orrison in their 2006 paper "The Linear 
        /// Complexity of a Graph"
        /// </summary>
        /// <returns>A floating point approximation of the complexity.</returns>
        public float Complexity()
        {
            return (float) -1.0;
        }

        /// <summary>
        /// The difficulty of the GridGraph's adjacency list, based somehow...
        /// </summary>
        /// <returns>A floating point approximation of the difficulty.</returns>
        public float Difficulty()
        {
            return (float) -1.0;
        }

        /// <summary>
        /// From a cell p in a direction, returns a list of all vertex cells
        /// which are in that direction in the order they would be reached by
        /// moving in that direction, ignoring walls.
        /// </summary>
        /// <returns>The in direction.</returns>
        /// <param name="p">A point in the GridGraph.</param>
        /// <param name="direction">A direction character from [U, D, L, R].</param>
        public PairList VerticesInDirection(Pair p, char direction)
        {
            return null;
        }

        /// <summary>
        /// Based solely on p's location in the grid, determines the directions
        /// it could ever possibly move in. Essentially, if it's next to a wall.
        /// </summary>
        /// <returns>A list of character directions from U, D, L, R.</returns>
        /// <param name="p">A point in the GridGraph.</param>
        public List<char> PotentialDirections(Pair p)
        {
            List<char> dirs = new List<char>{ 'U', 'D', 'L', 'R' };
            if (p.Item1 == 0)
            {
                dirs.Remove('L');
            }
            else if(p.Item1 == Width - 1)
            {
                dirs.Remove('R');
            }
            if(p.Item2 == 0)
            {
                dirs.Remove('U');
            }
            else if(p.Item2 == Height - 1)
            {
                dirs.Remove('D');
            }
            return dirs;
        }

        private bool IsInGrid(Pair p)
        {
            return IsInGrid(p.Item1, p.Item2);
        }

        private bool IsInGrid(int x, int y)
        {
            return 0 <= x && x < Width && 0 <= y && y < Height;
        }

        private Pair Build(Pair f, Pair t)
        {
            AddEdge(f, t);
            char dir = PathOrientation(f, t);
            if (dir == 'H')
            {
                if(f.Item1 > t.Item1) // Going left
                {
                    BuiltDirections[f.Item1, f.Item2] = Util.AddIfMissing('L', BuiltDirections[f.Item1, f.Item2]);
                    BuiltDirections[t.Item1, t.Item2] = Util.AddIfMissing('R', BuiltDirections[f.Item1, f.Item2]);
                    for(int i = t.Item1 + 1; i < f.Item1; i++)
                    {
                        BuiltDirections[i, f.Item2] = Util.AddIfMissing('L', BuiltDirections[i, f.Item2]);
                        BuiltDirections[i, f.Item2] = Util.AddIfMissing('R', BuiltDirections[i, f.Item2]);
                    }
                    InitialBuiltDirections[t.Item1, t.Item2] = 'R';
                }
                else // Right
                {
                    BuiltDirections[f.Item1, f.Item2] = Util.AddIfMissing('R', BuiltDirections[f.Item1, f.Item2]);
                    BuiltDirections[t.Item1, t.Item2] = Util.AddIfMissing('L', BuiltDirections[f.Item1, f.Item2]);
                    for (int i = f.Item1 + 1; i < t.Item1; i++)
                    {
                        BuiltDirections[i, f.Item2] = Util.AddIfMissing('L', BuiltDirections[i, f.Item2]);
                        BuiltDirections[i, f.Item2] = Util.AddIfMissing('R', BuiltDirections[i, f.Item2]);
                    }
                    InitialBuiltDirections[t.Item1, t.Item2] = 'L';
                }
            }
            else
            {
                if(f.Item2 > t.Item2) // Down
                {
                    BuiltDirections[f.Item1, f.Item2] = Util.AddIfMissing('U', BuiltDirections[f.Item1, f.Item2]);
                    BuiltDirections[t.Item1, t.Item2] = Util.AddIfMissing('D', BuiltDirections[f.Item1, f.Item2]);
                    for(int i = t.Item2 + 1; i < f.Item2; i++)
                    {
                        BuiltDirections[f.Item1, i] = Util.AddIfMissing('U', BuiltDirections[f.Item1, i]);
                        BuiltDirections[f.Item1, i] = Util.AddIfMissing('D', BuiltDirections[f.Item1, i]);
                    }
                    InitialBuiltDirections[t.Item1, t.Item2] = 'D';
                }
                else
                {
                    BuiltDirections[f.Item1, f.Item2] = Util.AddIfMissing('D', BuiltDirections[f.Item1, f.Item2]);
                    BuiltDirections[t.Item1, t.Item2] = Util.AddIfMissing('U', BuiltDirections[f.Item1, f.Item2]);
                    for (int i = f.Item2 + 1; i < t.Item2; i++)
                    {
                        BuiltDirections[f.Item1, i] = Util.AddIfMissing('U', BuiltDirections[f.Item1, i]);
                        BuiltDirections[f.Item1, i] = Util.AddIfMissing('D', BuiltDirections[f.Item1, i]);
                    }
                    InitialBuiltDirections[t.Item1, t.Item2] = 'U';
                }

            }
            Traverse();
            return t;
        }

        private void AddEdge(Pair f, Pair t)
        {
            char type = PathOrientation(f, t);
            if(type != 'N')
            {
                if(type == 'V' || type == 'P')
                {
                    int current = Math.Min(f.Item2, t.Item2);
                    while(current - 1 < f.Item2 || current - 1 < t.Item2)
                    {
                        is_path[f.Item1, current] = true;
                        current++;
                    }
                }
                else
                {
                    int current = Math.Min(f.Item1, t.Item1);
                    while (current - 1 < f.Item1 || current - 1 < t.Item1)
                    {
                        is_path[current, f.Item2] = true;
                        current++;
                    }
                }
            }
        }

        private char PathOrientation(Pair f, Pair t)
        {
            if(f.Item1 == t.Item1) // Same x values
            {
                return f.Item2 == t.Item2 ? 'P' : 'V';
            }
            return f.Item2 == t.Item2 ? 'H' : 'N';
        }

        private void Traverse()
        {
            ResetLists();
            BFS(Start);
            MarkWalls();
            UpdateMovableDirections();
        }

        private void ResetLists()
        {
            adj = new PairList[Width, Height];
            rev = new PairList[Width, Height];
            is_wall = new bool[Width, Height];
            vertices = new PairList();
            distance = new List<Tuple<Pair, int>>();
            MovableDirections = new Directions[Width, Height];
            for(int i = 0; i < Width; i++)
            {
                for(int j = 0; j < Height; j++)
                {
                    adj[i, j] = new PairList();
                    rev[i, j] = new PairList();
                    is_wall[i, j] = false;
                    MovableDirections[i, j] = new List<char>();
                }
            }
        }

        private void BFS(Pair s)
        {
            distance.Add(Tuple.Create(Start, 0));
            PairList queue = new PairList { Start };
            PairList seen = new PairList { Start };
            PairList visited = new PairList();
            BFSRecursive(queue, seen, visited);
        }

        private void BFSRecursive(PairList queue, PairList seen, PairList visited)
        {
            PairList q = new PairList();
            PairList s = new PairList();
            PairList v = new PairList();
            foreach(Pair p in queue){
                q.Add(p);
            }
            foreach(Pair p in seen){
                s.Add(p);
            }
            foreach(Pair p in visited){
                v.Add(p);
            }
            if(q.Count > 0)
            {
                Pair curr = q[0];
                int dist = Util.Lookup(curr, distance);
                Pair l = Move(curr, 'L');
                Pair r = Move(curr, 'R');
                Pair u = Move(curr, 'U');
                Pair d = Move(curr, 'D');
                if(l != null)
                {
                    if(!v.Contains(l))
                    {
                        q = Util.AddIfMissing(l, q);
                    }
                    if (!s.Contains(l)){
                        s.Add(l);
                        distance.Add(Tuple.Create(l, dist + 1));
                    }
                }
                if(r != null)
                {
                    if (!v.Contains(r))
                    {
                        q = Util.AddIfMissing(r, q);
                    }
                    if (!s.Contains(r))
                    {
                        s.Add(r);
                        distance.Add(Tuple.Create(r, dist + 1));
                    }
                }
                if(u != null)
                {
                    if (!v.Contains(u))
                    {
                        q = Util.AddIfMissing(u, q);
                    }
                    if (!s.Contains(u))
                    {
                        s.Add(u);
                        distance.Add(Tuple.Create(u, dist + 1));
                    }
                }
                if(d != null)
                {
                    if (!v.Contains(d))
                    {
                        q = Util.AddIfMissing(d, q);
                    }
                    if (!s.Contains(d))
                    {
                        s.Add(d);
                        distance.Add(Tuple.Create(d, dist + 1));
                    }
                }
                v.Add(curr);
                q.RemoveAt(0);
                BFSRecursive(q, s, v);
            }
            else{
                vertices = visited;
            }
        }

        private Pair Move(Pair f, char direction)
        {
            if (IsInGrid(f))
            {
                int x = f.Item1;
                int y = f.Item2;
                if(!is_path[x, y])
                {
                    return null;
                }
                if(direction == 'R')
                {
                    while(x+1 < Width && is_path[x + 1, y])
                    {
                        x++;
                    }
                    return new Pair(x, y);
                }
                if(direction == 'L')
                {
                    while(x-1 >= 0 && is_path[x - 1, y])
                    {
                        x--;
                    }
                    return new Pair(x, y);
                }
                if(direction == 'U')
                {
                    while(y-1 >=0 && is_path[x, y - 1])
                    {
                        y--;
                    }
                    return new Pair(x, y);
                }
                if(direction == 'D')
                {
                    while(y+1 < Height && is_path[x, y + 1])
                    {
                        y++;
                    }
                    return new Pair(x, y);
                }
                return null; // bad direction
            }
            return null;
        }

        private void AddToLists(Pair f, Pair t)
        {
            int f0 = f.Item1;
            int f1 = f.Item2;
            int t0 = t.Item1;
            int t1 = t.Item2;
            adj[f0, f1] = Util.AddIfMissing(t, adj[f0, f1]);
            rev[t0, t1] = Util.AddIfMissing(f, rev[t0, t1]);
        }

        private void MarkWalls()
        {
            foreach(Pair p in vertices)
            {
                MarkWalls(p);
            }
        }

        private void MarkWalls(Pair p)
        {
            int x = p.Item1;
            int y = p.Item2;
            Pair l = new Pair(x - 1, y);
            Pair r = new Pair(x + 1, y);
            Pair u = new Pair(x, y - 1);
            Pair d = new Pair(x, y + 1);
            if(IsInGrid(l) && !is_path[l.Item1, l.Item2])
            {
                is_wall[l.Item1, l.Item2] = true;
            }
            if (IsInGrid(r) && !is_path[r.Item1, r.Item2])
            {
                is_wall[r.Item1, r.Item2] = true;
            }
            if (IsInGrid(u) && !is_path[u.Item1, u.Item2])
            {
                is_wall[u.Item1, u.Item2] = true;
            }
            if (IsInGrid(d) && !is_path[d.Item1, d.Item2])
            {
                is_wall[d.Item1, d.Item2] = true;
            }
        }

        private void UpdateMovableDirections()
        {
            foreach(Pair v in vertices)
            {
                int x = v.Item1;
                int y = v.Item2;
                Pair up = new Pair(x, y - 1);
                Pair down = new Pair(x, y - 1);
                Pair left = new Pair(x, y - 1);
                Pair right = new Pair(x, y - 1); 
                if (IsInGrid(up) && is_path[up.Item1, up.Item2])
                {
                    is_wall[up.Item1, up.Item2] = true;
                }
                if (IsInGrid(down) && is_path[down.Item1, down.Item2])
                {
                    is_wall[down.Item1, down.Item2] = true;
                }
                if (IsInGrid(left) && is_path[left.Item1, left.Item2])
                {
                    is_wall[left.Item1, left.Item2] = true;
                }
                if (IsInGrid(right) && is_path[right.Item1, right.Item2])
                {
                    is_wall[right.Item1, right.Item2] = true;
                }
            }
        }

        private PairList VerticesX(int x)
        {
            PairList list = new PairList();
            foreach(Pair v in vertices)
            {
                if(x == v.Item1)
                {
                    list.Add(v);
                }
            }
            return list;
        }

        private PairList VerticesY(int y)
        {
            PairList list = new PairList();
            foreach (Pair v in vertices)
            {
                if (y == v.Item2)
                {
                    list.Add(v);
                }
            }
            return list;
        }

        private int ShortestPaths(Pair start, PairList ends)
        {
            if (vertices.Contains(start))
            {
                if (ends.Contains(start))
                {
                    return 0;
                }
                int dist = 1;
                PairList visited = new PairList();
                PairList queue = new PairList();
                visited.Add(start);
                queue.Add(start);
                while(queue.Count > 0)
                {
                    PairList next = new PairList();
                    foreach(Pair i in queue)
                    {
                        PairList neighbors = adj[i.Item1, i.Item2];
                        foreach(Pair j in neighbors)
                        {
                            if (!visited.Contains(j))
                            {
                                if (ends.Contains(j))
                                {
                                    return dist;
                                }
                                if (!i.Equals(j))
                                {
                                    next.Add(j);
                                }
                                visited.Add(j);
                            }
                        }
                    }
                    queue = next;
                    dist++;
                }
                return -1;
            }
            return -1;
        }
    }
}
