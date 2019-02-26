import gridgraph as gg
import printer as p
import random as rand
import util

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

    u = "U"
    d = "D"
    l = "L"
    r = "R"

    def add(offset, direction, length):
        index = offset*-1
        v.append(G.build_path(v[index], direction, length))

    #TODO if a vertex is missing, it is offset somehow by a path which destroyed
    #it. It needs to be accounted before, or ensure it can never happen
    add(1, r, 4)
    add(1, u, 3)
    add(1, l, 2)
    add(1, u, 6)
    add(1, l, 4)
    add(1, d, 1)
    add(1, r, 2)
    add(1, u, 3)
    add(1, r, 2)
    add(1, u, 1)
    add(1, r, 1)
    add(1, u, 2)
    add(1, l, 3)
    add(14, u, 5)
    add(1, l, 4)
    add(1, u, 8)
    add(1, r, 5)

    G.iterate(complexity, difficulty)

    # print G.distance
    print G.can_get_stuck()
    print G.trap_vertices()

    # G.determine_extra_paths(R)

    return G
#--------------------------------------
public_seed = 1149
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
