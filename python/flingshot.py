import gridgraph as gg
import printer as p
import random as rand
import util
from copy import deepcopy

def create(seed, level):
    return create_blocks(4, 3, seed)

def create_blocks(difficulty, complexity, seed):

    # Map constants
    height = 16
    width = 9

    difficulty = util.floor(difficulty)
    complexity = util.floor(complexity)

    grid = []
    #Default to a blocked play area
    for i in range(height):
        row = []
        for j in range(width):
            row.append("X")
        grid.append(row)

    top = ["X"] * width
    bottom = ["X"] * width
    top[width//2] = "O"

    G = blocks(height, width, difficulty, complexity, seed)

    for i in range(height):
        for j in range(width):
            if G.is_path[j][i]:
                grid[i][j] = "o" if G.is_unused_path[j][i] else "O"
            elif G.is_wall[j][i]:
                grid[i][j] = "w" if G.is_unused_wall[j][i] else "W"
            else:
                grid[i][j] = "X"

    grid.insert(0,top)
    grid.append(bottom)

    for i in range(len(grid)):
        grid[i].insert(0,"X")
        grid[i].append("X")
    return grid

#Reminder that our coordinate system is (x,y), starting from top left
def blocks(height, width, difficulty, complexity, seed):
    G = gg.GridGraph(width, height)
    R = rand.RandomSeed(seed)

    start_height = 14
    exit_height = 8
    exit = width // 2

    # G.define_start_location((4, start_height))
    # G.define_end_location((exit, exit_height))

    v = [(width // 2, height-1)]
    copy = util.MutableBool(False)
    valid = util.MutableBool(False)

    u = "U"
    d = "D"
    l = "L"
    r = "R"

    """ RESOURCES: RandomSeed (R), GridGraph (G), difficulty, complexity """

    """ RandomSeed USABLE AND USEFUL API
        G.generate(low, high)
    """

    """ GridGraph USABLE AND USEFUL API
        other = G.deep_copy()
        G.copy(other)

        G.build_path(f, dir, len)

        G.in_deg_p(p)
        G.out_deg_p(p) - useful for determining if we can screw up a vertex
        G.trap_vertices()
        G.can_get_stuck()
        G.fastest_path(), G.fastest_path_from_location(p)

        G.longest_path_no_wall(), G.longest_path_n_walls(n)
        G.longest_noninterfering_path() ?

        G.vertices_in_direction(p, dir)
        G.wall_of(w)
        G.depth(v)

        G.complexity()
        G.difficulty() #todo
        G.essential_vertices() #todo

        G.built_directions
        G.movable_directions

        G.possible(), G.possible_from_location(p)
    """

    def check(g):
        start = g.start
        left = g.is_wall[start[0]-1][start[1]]
        right = g.is_wall[start[0]+1][start[1]]
        up = g.is_wall[start[0]][start[1]-1]
        if not (left or right or up):
            return
        if(g.complexity() >= G.complexity()):
            valid.value = True
            copy.value = True

    # Given a vertex v in the graph g, expand on it
    def try_build(g, v):
        """
        Returns True if we sucessfully decide to expand on it,
        or False if we do not.
        """
        #TODO special case for (4,0) === (width//2, 0)
        #We should not treat it as a vertex for this case if movable is only "D"
        built = g.built_directions[v[0]][v[1]]
        movable = g.movable_directions[v[0]][v[1]]
        initial = g.initial_built_direction[v[0]][v[1]]
        #Special case for cell right above exit
        if v == (g.width//2, 0) and movable == ["D"]:
                return False
        good = g.potential_directions(v)
        if initial == u or initial == d:
            if u in good:
                good.remove(u)
            if d in good:
                good.remove(d)
        elif initial == l or initial == r:
            if l in good:
                good.remove(l)
            if r in good:
                good.remove(r)
        good = [x for x in good if x not in built]
        def weight_assignments(dir):
            weight = {
                u: 3,
                l: 2,
                r: 2,
                d: 1
            }
            return weight.get(dir, "Error - Invalid Direction")
        # If fail, try another direction before returning to parent function
        while len(good) > 0:
            ranges = util.tuple_ranges(weight_assignments, good)
            choice = R.choose_from(ranges)
            dir = good[choice]
             #TODO change 1 to some general function for n
            max_length = g.longest_path_n_walls(v, dir, 1)
            if dir == d:
                max_length = min(max_length, 4)
            else:
                max_length = min(max_length, 6)
            length = R.generate(1, max_length)
            # print "Building", v, dir, length
            g.build_path(v, dir, length)
            return True
            #TODO figure this out
        return False

    # Choose a vertex from our list and try to build on it
    def process(g):
        # print g.complexity()
        dists = g.distance
        valid.value = False
        while not valid.value:
            # Determine which vertex to use
            if len(dists) == 0:
                # print "ERROR - No good vertices."
                return
            #TODO Better probability function? Use some GG methods!
            probabilities = map(lambda x: 1 + 2*x[1]**2, dists)
            ranges = util.tuple_ranges((lambda x: 1+2*x[1]**2), dists)
            choice = R.choose_from(ranges)
            vertex = dists[choice][0]
            if not vertex == None:
                if try_build(g, vertex):
                    check(g)
                else:
                    dists = filter(lambda x: x[0] != vertex, dists)
            else:
                print "ERROR - Could not choose a vertex."
                return

    def iterate():
        loop_condition = False
        # while loop_condition:
        for _ in range(60):
            copy.value = False
            other = deepcopy(G)
            process(other)
            if copy.value:
                G.copy(other)

    iterate()

    # print G.possible()
    G.determine_extra_paths(R)

    # for j in range(len(G.built_directions[0])):
    #     for i in range(len(G.built_directions)):
    #         print "({},{})".format(i,j), G.initial_built_direction[i][j]

    return G
#--------------------------------------
public_seed = 11355
level = 1
b = create(public_seed, level)

p.print_player_view(b)


#--------------------------------------
# THINGS TO IMPLEMENT
#  Splitting of core data structure gridgraph features and additional utils into separate classes
#  Genrate more complex patterns from existing algorithms
#  - Path chaining method - arbitrary pattern
#  Test cases
#  Efficient way to report back good spots to build more paths
#  - Where to add new paths without interfering with any other paths in the graph
#
#  Good strategies for generating random patterns of paths (big idea algorithm)
#  Variability with difficulty, complexity, key, height, etc.
#
# Unreturnable paths - once you go down a path you can never return to
# another part of the maze, use trap_vertices?
