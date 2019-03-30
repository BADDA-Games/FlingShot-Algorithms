using System;
using System.Collections.Generic;
using Pair = System.Tuple<int, int>;
using PairList = System.Collections.Generic.List<System.Tuple<int, int>>;
using Directions = System.Collections.Generic.List<System.Collections.Generic.List<System.Collections.Generic.List<char>>>;
using Bools = System.Collections.Generic.List<System.Collections.Generic.List<bool>>;

namespace Algorithm
{
    public class GridGraph
    {
        public int Width { get; }
        public int Height { get; }

        Directions InitialBuiltDirections { get; }
        Directions MovableDirections { get; }

        PairList vertices;
        List<Tuple<Pair, int>> distance;
        Pair start;
        List<List<PairList>> adj;
        List<List<PairList>> rev;
        Bools is_path;
        Bools is_unused_path;
        Bools is_wall;
        Bools is_unused_wall;

        public GridGraph(int width, int height)
        {
            //TODO initialize!
            Width = width;
            Height = height;
            start = Tuple.Create(width/2, height-1);
            InitialBuiltDirections = new Directions();
            MovableDirections = new Directions();
            vertices = new PairList();
            distance = new List<Tuple<Pair, int>>();
            adj = new List<List<PairList>>();
            rev = new List<List<PairList>>();
            is_path = new Bools();
            is_unused_path = new Bools();
            is_wall = new Bools();
            is_unused_wall = new Bools();
            for(int i=0; i<width; i++)
            {
                for(int j=0; j<height; j++)
                {

                }
            }
        }

        /// <summary>
        /// Copies information from another GridGraph information.
        /// </summary>
        /// <param name="other">Other.</param>
        public void Copy(GridGraph other)
        {

        }

        /// <summary>
        /// Finds the in-degree of p, the number of vertices which can
        /// move to p in one move.
        /// </summary>
        /// <returns>The in-degree of p.</returns>
        /// <param name="p">A point in the GridGraph.</param>
        public int InDeg(Pair p)
        {
            return -1;
        }

        /// <summary>
        /// Finds the out-degree of p, the number of vertices which can be
        /// reached from p in one move.
        /// </summary>
        /// <returns>The out-degree of p.</returns>
        /// <param name="p">A point in the GridGraph.</param>
        public int OutDeg(Pair p)
        {
            return -1;
        }

        /// <summary>
        /// Finds the least number of moves from the start to reach a vertex v
        /// </summary>
        /// <returns>The depth of vertex v.</returns>
        /// <param name="v">A vertex in the grid.</param>
        public int Depth(Pair v)
        {
            return -1;
        }

        /// <summary>
        /// Builds a path from f in direction with for length cells.
        /// The length does not include the starting space; a path of length one
        /// occupies an additional cell.
        /// </summary>
        /// <param name="f">A cell to start at</param>
        /// <param name="direction">The direction to move in.</param>
        /// <param name="length">The length of the path.</param>
        public void BuildPath(Pair f, char direction, int length)
        {

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
            return -1;
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
            return null;
        }
    }
}
