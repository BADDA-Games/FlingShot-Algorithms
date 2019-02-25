import gridgraph as gg
import printer as p
import random as rand
import util

def create(seed):
    return create_blocks(4, 3, 4, 3, seed)

def create_blocks(entrance, exit, difficulty, complexity, seed):
    # TODO move the majority of this function somewhere else; the algorithm should be its own method
    height = 16
    width = 9

    entrance = util.floor(entrance)
    exit = util.floor(exit)
    height = util.floor(height)
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
    top[exit] = "O"
    bottom[entrance] = "O"

    G = blocks(entrance, exit, height, width, difficulty, complexity, seed)

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
def blocks(entrance, exit, height, width, difficulty, complexity, seed):
    G = gg.GridGraph(width, height)
    R = rand.RandomSeed(seed)

    start_height = 14
    exit_height = 8

    G.define_start_location((entrance, start_height))
    G.define_end_location((exit, exit_height))

    v = [(entrance, start_height)]

    u = "U"
    d = "D"
    l = "L"
    r = "R"

    def add(offset, direction, length):
        index = offset*-1
        v.append(G.build_path(v[index], direction, length))

    v.append(G.build_path((entrance, start_height), "R", 4))
    add(1, d, 1)
    add(1, l, 2)
    add(3, u, 1)
    add(1, l, 1)
    add(1, u, 2)
    add(1, r, 1)
    add(1, u, 7)
    add(1, l, 1)
    add(1, u, 4)
    add(1, l, 1)
    add(1, d, 1)
    add(1, r, 2)
    add(1, u, 1)
    add(6, d, 3)
    add(1, l, 1)
    add(1, d, 1)
    add(1, l, 6)
    add(1, d, 1)
    add(1, r, 1)
    add(1, d, 5)
    add(1, r, 1)
    add(1, u, 1)
    add(1, l, 2)
    add(3, d, 1)
    add(1, r, 2)
    add(9, u, 2)
    add(1, r, 1)
    add(1, d, 8)
    add(2, u, 3)
    add(1, l, 1)
    add(1, d, 1)
    add(2, u, 3)
    add(1, r, 4)
    add(1, d, 4)
    add(1, r, 1)
    add(1, u, 1)
    add(1, r, 2)
    add(2, l, 5)
    add(4, d, 2)
    add(1, r, 3)
    add(36, l, 3)
    add(1, d, 1)
    add(1, r, 3)
    add(3, u, 4)
    add(1, l, 4)
    add(31, u, 2)

    G.iterate(complexity, difficulty)

    # print G.distance

    # G.determine_extra_paths(R)

    return G
#--------------------------------------
public_seed = 1146
b = create(public_seed)
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
