class GridGraph:
    # A class to show how positions on the grid
    # direct to possible neighboring positions
    # This is a directed graph, we may have an edge without the reverse
    # Each vertex has an (x,y) position, with y=0 on top

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.vertices = []

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
                self.is_used_wall[i].append(j)
                self.adj[i][j] = []
                self.rev[i][j] = []
                self.is_path[i][j] = False
                self.is_vertex[i][j] = False
                self.is_used_wall[i][j] = False

    def define_start_location(self, p):
        if not self.start_location_defined:
            self.start_location_defined = True
            self.start_location = p
            self.add_edge(p, p)
            for i in range(p[1], self.height):
                self.is_path[p[0]][i] = True
            if not p[1] == 0:
                self.is_used_wall[p[0]][p[1]-1] = True

    def define_end_location(self, p):
        if not self.end_location_defined:
            self.end_location_defined = True
            self.end_location = p
            self.add_edge(p, p)
            for i in range(0, p[1]):
                self.is_path[p[0]][i] = True

    def add_edge(self, f, t):
        if not self.path_orientation(f, t) == "N":
            if self.path_orientation(f, t) == "V" or self.path_orientation(f, t) == "P":
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

    def is_in_grid(self, p):
        x = p[0]
        y = p[1]
        return 0 <= x < self.width and 0 <= y < self.height

    # TODO modify to check for removed vertices and paths
    # Iterate through each non-stop part of the path, if it interferes
    # with another path, determine if adj or rev need to be modified or cleared
    # also need to check sides to see if paths are joining by being
    # next to each other but just at the tip
    def build(self, f, t):
        self.add_edge(f,t)
        self.traverse() #inefficient, but works
        # self.update_path_sides(f, t) TODO get this working in the future

    #TODO
    def update_path_sides(self, f, t):
        self.update_vertex_neighbors(f)
        self.update_vertex_neighbors(t)
        if self.path_orientation(f, t) == "V":
            min, max = minmax(f[1], t[1])
            for i in range(min, max+1):
                print (f[0], i),
            print ""
        elif self.path_orientation(f, t) == "H":
            min, max = minmax(f[0], t[0])
            for i in range(min, max+1):
                print (i, f[1]),
            print ""


    def path_orientation(self, f, t):
        if f[0] == t[0]: # Same x values
            return "P" if f[1] == t[1] else "V"
        else: # Same y values
            return "H" if f[1] == t[1] else "N"


    def update_vertex_neighbors(self, p):
        self.mark_used_walls_p(p)

    # Special note about build_path - The length of it does not include the
    # starting point f; the length is the number out from f it goes.
    # f will also be converted to a path if it is not - the idea is
    # that you build paths from other paths
    def build_path(self, f, direction, length):
        if length > 0 and self.is_in_grid(f):
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

    def traverse(self):
        if not self.start_location == None:
            self.reset_lists()
            self.bfs(self.start_location)
            self.mark_used_walls()

    def reset_lists(self):
        self.adj = []
        self.rev = []
        for i in range(self.width):
            self.adj.append(i)
            self.rev.append(i)
            self.adj[i] = []
            self.rev[i] = []
            for j in range(self.height):
                self.adj[i].append(j)
                self.rev[i].append(j)
                self.adj[i][j] = []
                self.rev[i][j] = []

    def bfs(self, start):
        self.bfs_recursive([start], [])

    def bfs_recursive(self, queue, visited):
        if len(queue) > 0:
            curr = queue[0]
            l = self.move(curr, "L")
            r = self.move(curr, "R")
            u = self.move(curr, "U")
            d = self.move(curr, "D")
            if not l == None:
                self.add_to_lists(curr, l)
                if not l in visited:
                    add_if_missing(l, queue)
            if not r == None:
                self.add_to_lists(curr, r)
                if not r in visited:
                    add_if_missing(r, queue)
            if not u == None:
                self.add_to_lists(curr, u)
                if not u in visited:
                    add_if_missing(u, queue)
            if not d == None:
                self.add_to_lists(curr, d)
                if not d in visited:
                    add_if_missing(d, queue)
            visited.append(curr)
            self.bfs_recursive(queue[1:], visited)
        else: # Now we have visited every vertex
            self.vertices = visited

    def add_to_lists(self, f, t):
        adj = self.adj[f[0]][f[1]]
        new_adj = add_if_missing(t, adj)
        self.adj[f[0]][f[1]] = new_adj
        rev = self.rev[t[0]][t[1]]
        new_rev = add_if_missing(f, rev)
        self.rev[t[0]][t[1]] = new_rev

    def move(self, f, direction):
        if self.is_in_grid(f):
            if not self.is_path[f[0]][f[1]]:
                return None
            elif direction == "R":
                x = f[0]
                y = f[1]
                while x + 1 < self.width and self.is_path[x + 1][y]:
                    x = x + 1
                return (x,y)
            elif direction == "L":
                x = f[0]
                y = f[1]
                while x - 1 >= 0 and self.is_path[x - 1][y]:
                    x = x - 1
                return (x,y)
            elif direction == "U":
                x = f[0]
                y = f[1]
                while y - 1 >= 0 and self.is_path[x][y - 1]:
                    y = y - 1
                if x == self.end_location[0] and y == 0:
                    return None # Going up here will advance to next grid
                return (x,y)
            elif direction == "D":
                x = f[0]
                y = f[1]
                while y + 1 < self.height and self.is_path[x][y + 1]:
                    y = y + 1
                if x == self.start_location[0] and y == self.height - 1:
                    return None # Going down here will go to the previous grid
                return (x,y)
            return None #bad direction
        else:
            return None

    def mark_used_walls(self):
        for p in self.vertices:
            self.mark_used_walls_p(p)

    def mark_used_walls_p(self, p):
        l = (p[0]-1, p[1])
        r = (p[0]+1, p[1])
        u = (p[0], p[1]-1)
        d = (p[0], p[1]+1)
        # To be modified with other elements potentially later
        if self.is_in_grid(l) and not self.is_path[l[0]][l[1]]:
            self.is_used_wall[l[0]][l[1]] = True
        if self.is_in_grid(r) and not self.is_path[r[0]][r[1]]:
            self.is_used_wall[r[0]][r[1]] = True
        if self.is_in_grid(u) and not self.is_path[u[0]][u[1]]:
            self.is_used_wall[u[0]][u[1]] = True
        if self.is_in_grid(d) and not self.is_path[d[0]][d[1]]:
            self.is_used_wall[d[0]][d[1]] = True



def add_if_missing(element, list):
    if not element in list:
        list.append(element)
    return list

def minmax(n1, n2):
    smaller = min(n1, n2)
    larger = max(n1, n2)
    return smaller, larger
