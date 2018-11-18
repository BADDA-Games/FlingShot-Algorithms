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
        self.is_path = []
        self.is_vertex = []
        self.is_used_wall = []
        for i in range(width):
            self.adj.append(i)
            self.rev.append(i)
            self.is_path.append(i)
            self.is_vertex.append(i)
            self.is_used_wall.append(i)
            self.adj[i] = []
            self.rev[i] = []
            self.is_path[i] = []
            self.is_vertex[i] = []
            self.is_used_wall[i] = []
            for j in range(height):
                self.adj[i].append(j)
                self.rev[i].append(j)
                self.is_path[i].append(j)
                self.is_vertex[i].append(j)
                self.adj[i][j] = []
                self.rev[i][j] = []
                self.is_path[i][j] = False
                self.is_vertex[i][j] = False
                self.is_vertex[i][j] = False

    def define_start_location(self, p):
        if not self.start_location_defined:
            self.start_location_defined = True
            self.start_location = p
            self.add_edge(p, p)
            for i in range(p[1], self.height):
                self.is_path[p[0]][i] = True
            # if not p[1] == 0:
            #     self.is_used_wall[p[0]][p[1]-1] = True

    def define_end_location(self, p):
        if not self.end_location_defined:
            self.end_location_defined = True
            self.end_location = p
            self.add_edge(p, p)
            for i in range(0, p[1]):
                self.is_path[p[0]][i] = True

    def add_edge(self, f, t):
        if f[0] == t[0] or f[1] == t[1]:
            # Currently choosing not to add edges to adjacency list immediately
            # self.adj[f[0]][f[1]].append(t)
            # self.rev[t[0]][t[1]].append(f)
            if f[0] == t[0]:
                current = min(f[1], t[1])
                while current-1 < f[1] or current-1 < t[1]:
                    self.is_path[f[0]][current] = True
                    current = current + 1
            else:
                current = min(f[0], t[0])
                while current-1 < f[0] or current-1 < t[0]:
                    self.is_path[current][f[1]] = True
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
