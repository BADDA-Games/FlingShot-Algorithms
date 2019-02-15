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

    v.append(G.build_path((entrance, start_height), "R", 4))
    v.append(G.build_path(v[-1], "D", 1))
    v.append(G.build_path(v[-1], "L", 2))
    v.append(G.build_path(v[-3], "U", 1))
    v.append(G.build_path(v[-1], "L", 1))
    v.append(G.build_path(v[-1], "U", 2))
    v.append(G.build_path(v[-1], "R", 1))
    v.append(G.build_path(v[-1], "U", 7))
    v.append(G.build_path(v[-1], "L", 1))
    v.append(G.build_path(v[-1], "U", 4))
    v.append(G.build_path(v[-1], "L", 1))
    v.append(G.build_path(v[-1], "D", 1))
    v.append(G.build_path(v[-1], "R", 2))
    v.append(G.build_path(v[-1], "U", 1))
    v.append(G.build_path(v[-6], "D", 3))
    v.append(G.build_path(v[-1], "L", 1))
    v.append(G.build_path(v[-1], "D", 1))
    v.append(G.build_path(v[-1], "L", 6))
    v.append(G.build_path(v[-1], "D", 1))
    v.append(G.build_path(v[-1], "R", 1))
    v.append(G.build_path(v[-1], "D", 5))
    v.append(G.build_path(v[-1], "R", 1))
    v.append(G.build_path(v[-1], "U", 1))
    v.append(G.build_path(v[-1], "L", 2))
    v.append(G.build_path(v[-3], "D", 1))
    v.append(G.build_path(v[-1], "R", 2))
    v.append(G.build_path(v[-9], "U", 2))
    v.append(G.build_path(v[-1], "R", 1))
    v.append(G.build_path(v[-1], "D", 8))
    v.append(G.build_path(v[-2], "U", 3))
    v.append(G.build_path(v[-1], "L", 1))
    v.append(G.build_path(v[-1], "D", 1))
    v.append(G.build_path(v[-2], "U", 3))
    v.append(G.build_path(v[-1], "R", 4))
    v.append(G.build_path(v[-1], "D", 4))
    v.append(G.build_path(v[-1], "R", 1))
    v.append(G.build_path(v[-1], "U", 1))
    v.append(G.build_path(v[-1], "R", 2))
    v.append(G.build_path(v[-2], "L", 5))
    v.append(G.build_path(v[-4], "D", 2))
    v.append(G.build_path(v[-1], "R", 3))
    v.append(G.build_path(v[-36], "L", 3))
    v.append(G.build_path(v[-1], "D", 1))
    v.append(G.build_path(v[-1], "R", 3))
    v.append(G.build_path(v[-3], "U", 4))
    v.append(G.build_path(v[-1], "L", 4))
    v.append(G.build_path(v[-31], "U", 2))

    print G.distance

    # G.determine_extra_paths(R)

    # p.print_gg(G)
    return G
#--------------------------------------
public_seed = 1146
b = create(public_seed)
# p.print_b(b)
p.print_player_view(b)
# R = rand.RandomSeed(public_seed)
# R.generate(0,100)
# print R.seed
# R.generate(0,100)
# print R.seed


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
