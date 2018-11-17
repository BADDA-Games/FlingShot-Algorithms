class GridGraph:
    # A class to show how positions on the grid
    # direct to possible neighboring positions
    # This is a directed graph, we may have an edge without the reverse
    # Each vertex has an (x,y) position, with y=0 on top

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.start_location = None
        self.start_location_defined = False

        self.end_location = None
        self.end_location_defined = False

        self.adj = []
        self.rev = []
        self.isPath = []
        self.isVertex = []
        self.isUsedWall = []
        for i in range(width):
            self.adj.append(i)
            self.rev.append(i)
            self.isPath.append(i)
            self.isVertex.append(i)
            self.isUsedWall.append(i)
            self.adj[i] = []
            self.rev[i] = []
            self.isPath[i] = []
            self.isVertex[i] = []
            self.isUsedWall[i] = []
            for j in range(height):
                self.adj[i].append(j)
                self.rev[i].append(j)
                self.isPath[i].append(j)
                self.isVertex[i].append(j)
                self.adj[i][j] = []
                self.rev[i][j] = []
                self.isPath[i][j] = False
                self.isVertex[i][j] = False
                self.isVertex[i][j] = False

    def define_start_location(self, p):
        if not self.start_location_defined:
            self.start_location_defined = True
            self.start_location = p
            self.add_edge(p, p)
            for i in range(p[1], self.height):
                self.isPath[p[0]][i] = True
            if not p[1] == 0
            self.isUsedWall[p[0]][p[1]-1] = True

    def define_end_location(self, p):
        if not self.end_location_defined:
            self.end_location_defined = True
            self.end_location = p
            self.add_edge(p, p)
            for i in range(0, p[1]):
                self.isPath[p[0]][i] = True

    def add_edge(self, f, t):
        if f[0] == t[0] or f[1] == t[1]:
            # Currently choosing not to add edges to adjacency list immediately
            # self.adj[f[0]][f[1]].append(t)
            # self.rev[t[0]][t[1]].append(f)
            if f[0] == t[0]:
                current = min(f[1], t[1])
                while current-1 < f[1] or current-1 < t[1]:
                    self.isPath[f[0]][current] = True
                    current = current + 1
            else:
                current = min(f[0], t[0])
                while current-1 < f[0] or current-1 < t[0]:
                    self.isPath[current][f[1]] = True
                    current = current + 1

    def in_deg(self,x,y):
        return len(self.rev[x][y])

    def in_deg_p(self,xy):
        return self.in_deg(xy[0],xy[1])

    # Max out degree can be 3, min 0
    def out_deg(self,x,y):
        return len(self.adj[x][y])

    def out_deg_p(self,xy):
        return self.out_deg(xy[0],xy[1])

    # TODO modify to check for removed vertices and paths
    def build(self, f, t):
        self.add_edge(f,t)

    def build_path(self, f, direction, length):
        if length > 0 and 0 <= f[0] < self.width and 0 <= f[1] < self.height:
            if direction == "R":
                if f[0] + length >= self.width:
                    self.build(f, (self.width-1, f[1]))
                else:
                    self.build(f, (f[0]+length, f[1]))
            if direction == "L":
                if f[0] - length < 0:
                    self.build(f, (0, f[1]))
                else:
                    self.build(f, (f[0]-length, f[1]))
            if direction == "U":
                if f[0] - length < 0:
                    self.build(f, (f[0], 0))
                else:
                    self.build(f, (f[0], f[1]-length))
            if direction == "D":
                if f[0] + length >= self.height:
                    self.build(f, (f[0], self.height-1))
                else:
                    self.build(f, (f[0], f[1]+length))
            print f

    def traverse():
        if not self.start_location == None:
            #BFS
            print "Hello"

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

    G = GridGraph(width, height)
    #Algorithm goes here
    start_var, seed = generate(0,2,seed)
    exit_var, seed = generate(0,3,seed)

    starting_height = height - height//4 - start_var
    G.define_start_location((entrance, starting_height))

    exit_height = height//8 + exit_var + 1
    G.define_end_location((exit, exit_height))

    G.build_path((entrance, starting_height), "R", 3)
    #End algorithm
    #---------------------------------------------------

    for i in range(height):
        for j in range(width):
            grid[i][j] = "O" if G.isPath[j][i] else "X"

    grid.insert(0,top)
    grid.append(bottom)

    for i in range(len(grid)):
        grid[i].insert(0,"X")
        grid[i].append("X")

    return grid
#--------------------------------------
def printB(blocks):
    for i in range(len(blocks)):
        for j in range(len(blocks[0])):
            print blocks[i][j],
        print ""

def printGG(gg):
    for j in range(len(gg.isPath[0])):
        for i in range(len(gg.isPath)):
            print "O" if gg.isPath[i][j] else "X",
            # Add U for used wall
        print ""
#--------------------------------------
def floor(n):
    return int(n//1)
#--------------------------------------
def generate(low, high, seed):
    mod = high - low + 1
    if seed < 1: # Either 0 or negative, out of bounds due to a bad initial seed probably
        seed =  ( (low + high - seed + 1999) * 1582307 ) % 55555333
    seed = (seed * 22028423 * (seed % 3877) + ( (seed % 101) * (seed % 499999) ) ) % 99999989
    value = (seed % mod) + low
    return value, seed
#--------------------------------------

public_seed = 12
b = blocks(2, 5, 10, 4, 3, False, public_seed)
printB(b)

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
#  Add github repo
#  Split methods into different files for ease
#
#  Good strategies for generating random patterns of paths (big idea algorithm)
#  Variability with difficulty, complexity, key, height, etc.
