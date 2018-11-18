import gridgraph as gg
import printer as p
import random as rand

def blocks(entrance, exit, height, difficulty, complexity, key, seed):
    if height < 4:
        height = 4
    width = 9

    entrance = floor(entrance)
    exit = floor(exit)
    height = floor(height)
    difficulty = floor(difficulty)
    complexity = floor(complexity)

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

    #Reminder that our coordinate system is (x,y), starting from top left
    #---------------------------------------------------

    G = gg.GridGraph(width, height)
    R = rand.RandomSeed(seed)
    #Algorithm goes here
    start_var = R.generate(0,2)
    exit_var = R.generate(0,3)

    starting_height = height - height//4 - start_var
    G.define_start_location((entrance, starting_height))

    exit_height = height//8 + exit_var + 1
    G.define_end_location((exit, exit_height))

    G.build_path((entrance, starting_height), "R", 3)
    #End algorithm
    #---------------------------------------------------

    for i in range(height):
        for j in range(width):
            grid[i][j] = "O" if G.is_path[j][i] else "X"

    grid.insert(0,top)
    grid.append(bottom)

    for i in range(len(grid)):
        grid[i].insert(0,"X")
        grid[i].append("X")

    return grid
#--------------------------------------
def floor(n):
    return int(n//1)
#--------------------------------------
public_seed = 12
b = blocks(2, 5, 10, 4, 3, False, public_seed)
p.printB(b)

#--------------------------------------
# THINGS TO IMPLEMENT
#  Used Walls
#  - Removal/addition of unimportant walls algorithm
#  - Add Used Walls to pretty printer
#  Genrate more complex patterns from existing algorithms
#  - Path chaining method - arbitrary pattern
#  Test cases
#  Proper tracking of adj and rev
#  Efficient way to report back good spots to build more paths
#  - Where to add new paths without interfering with any other paths in the graph
#
#  Good strategies for generating random patterns of paths (big idea algorithm)
#  Variability with difficulty, complexity, key, height, etc.
