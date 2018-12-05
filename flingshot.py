import gridgraph as gg
import printer as p
import random as rand
import util

def create_blocks(entrance, exit, height, difficulty, complexity, key, seed):
    # TODO move the majority of this function somewhere else; the algorithm should be its own method
    if height < 4:
        height = 4
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

    G = blocks(entrance, exit, height, width, difficulty, complexity, key, seed)

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
def blocks(entrance, exit, height, width, difficulty, complexity, key, seed):
    G = gg.GridGraph(width, height)
    R = rand.RandomSeed(seed)

    start_var = R.generate(0,2)
    starting_height = height - height//4 - start_var
    exit_var = R.generate(0,3)
    exit_height = height//8 + exit_var + 1

    G.define_start_location((entrance, starting_height))
    G.define_end_location((exit, exit_height))

    G.build_path((entrance, starting_height), "R", 2)
    # print G.vertices

    G.build_path((4,2), "D", 10)
    # print G.vertices

    print G.adj[4][6]

    print G.rev[4][6]

    # G.build_path((4,9), "L", 10)
    # G.build_path((6,1), "D", 8)

    # G.build_path((6,9), "R", 1)
    # G.build_path((7,9), "U", 2)
    # G.build_path((7,7), "L", 7)
    # G.build_path((0,7), "U", 4)
    # G.build_path((0,3), "R", 4)

    # G.determine_extra_paths(R)
    # print G.fastest_path()

    # o = G.deep_copy()
    return G
#--------------------------------------
public_seed = 1145
b = create_blocks(2, 5, 10, 4, 3, False, public_seed)
# p.print_b(b)
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
