class GridGraph:
    # A class to show how positions on the grid
    # direct to possible neighboring positions
    # This is a directed graph, we may have an edge without the reverse
    # Each vertex has an (x,y) position, with y=0 on top

    def __init__(self, width, height):
        """
        Implicitly called upon creation of a GridGraph object. Sets all of the
        variables to default and starter values. Defines every variable used
        in the data structure.
        """
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
        self.is_unused_path = []
        self.is_vertex = []
        self.is_wall = []
        self.is_unused_wall = []
        for i in range(width):
            self.adj.append(i)
            self.rev.append(i)
            self.is_path.append(i)
            self.is_unused_path.append(i)
            self.is_vertex.append(i)
            self.is_wall.append(i)
            self.is_unused_wall.append(i)
            self.adj[i] = []
            self.rev[i] = []
            self.is_path[i] = []
            self.is_unused_path[i] = []
            self.is_vertex[i] = []
            self.is_wall[i] = []
            self.is_unused_wall[i] = []
            for j in range(height):
                self.adj[i].append(j)
                self.rev[i].append(j)
                self.is_path[i].append(j)
                self.is_unused_path[i].append(j)
                self.is_vertex[i].append(j)
                self.is_wall[i].append(j)
                self.is_unused_wall[i].append(j)
                self.adj[i][j] = []
                self.rev[i][j] = []
                self.is_path[i][j] = False
                self.is_unused_path[i][j] = False
                self.is_vertex[i][j] = False
                self.is_wall[i][j] = False
                self.is_unused_wall[i][j] = False

    def deep_copy(self):
        """
        Creates a deep copy of the current GridGraph data structure
        """
        other = GridGraph(self.width, self.height)
        other.vertices = self.vertices
        other.start_location = self.start_location
        other.start_location_defined = self.start_location_defined
        other.end_location = self.end_location
        other.end_location_defined = self.end_location_defined
        other.adj = self.adj
        other.rev = self.rev
        other.is_path = self.is_path
        other.is_unused_path = self.is_unused_path
        other.is_vertex = self.is_vertex
        other.is_wall = self.is_wall
        other.is_unused_wall = self.is_unused_wall
        return other

    def define_start_location(self, p):
        """
        Sets the start location parameter of the GridGraph, or does nothing
        if it was already set. This method should be called soon after creation.
        """
        if not self.start_location_defined:
            self.start_location_defined = True
            self.start_location = p
            self.add_edge(p, p)
            for i in range(p[1], self.height):
                self.is_path[p[0]][i] = True
            if not p[1] == 0:
                self.is_wall[p[0]][p[1]-1] = True

    def define_end_location(self, p):
        """
        Sets the end location parameter of the GridGraph, or does nothing
        if it was already set. This method should be called soon after creation.
        """
        if not self.end_location_defined:
            self.end_location_defined = True
            self.end_location = p
            self.add_edge(p, p)
            for i in range(0, p[1]):
                self.is_path[p[0]][i] = True

    def add_edge(self, f, t):
        """
        Adds an edge between f and t to the grid, without updating any lists or
        meta variables, but simply changing all middle paths is_path flags to
        True. Does nothing if the path is not in a straight line.
        """
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
        """
        Returns the in-degree of a point (x,y), the number of vertices that can
        immediately move to (x,y)
        """
        return len(self.rev[x][y])

    def in_deg_p(self,xy):
        """
        Returns the in-degree of a point xy, the number of vertices that can
        immediately move to xy
        """
        return self.in_deg(xy[0],xy[1])

    def out_deg(self,x,y):
        """
        Returns the out-degree of a point (x,y), the number of vertices it can
        immediately move to
        """
        return len(self.adj[x][y])

    def out_deg_p(self,xy):
        """
        Returns the out-degree of a point xy, the number of vertices it can
        immediately move to
        """
        return self.out_deg(xy[0],xy[1])

    def is_in_grid(self, p):
        """
        Returns true if point p is in the grid space, false if it is not
        """
        x = p[0]
        y = p[1]
        return 0 <= x < self.width and 0 <= y < self.height

    # TODO use update_path sides to update the grid without
    # doing a whole traversal
    def build(self, f, t):
        """
        Adds an edge from point f to point t, then traverses the graph and
        sets all variables properly to accomodate for the new edge.
        """
        self.add_edge(f,t)
        self.traverse() #inefficient, but works
        # self.update_path_sides(f, t)

    #TODO
    def update_path_sides(self, f, t):
        """
        As of right now, this method is unfinished and deprecated.
        If completed, it should properly update all variables in the graph
        to represent a new edge added properly, including new constructions of
        walls, and all changes in the adjacency and reverse listed, even
        changes affecting other neighboring paths which get changed as a
        result of the new edge. As of right now, we consider this by simply
        re-traversing the entire graph every time an edge is added.
        """
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
        """
        Given two points f and t, return P if they are the same point, V
        if they form a vertical line in the grid, H if they form a horizontal
        line in the grid, or N if they form neither
        """
        if f[0] == t[0]: # Same x values
            return "P" if f[1] == t[1] else "V"
        else: # Same y values
            return "H" if f[1] == t[1] else "N"

    def update_vertex_neighbors(self, p):
        """
        The complete process for setting relevant parameters for every vertex,
        usually called in the traversal pipeline
        """
        self.mark_walls_p(p)

    def build_path(self, f, direction, length):
        """
        Builds a path starting from a point f, in the direction specified,
        until it reaches the edge of the graph or we have built it length
        squares out from the start. It's important to note the length does not
        include the starting space, a path which spans length one occupies two
        grid spaces.
        """
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
                if f[1] - length < 0:
                    self.build(f, (f[0], 0))
                else:
                    self.build(f, (f[0], f[1]-length))
            if direction == "D":
                if f[1] + length >= self.height:
                    self.build(f, (f[0], self.height-1))
                else:
                    self.build(f, (f[0], f[1]+length))

    def traverse(self):
        """
        Traversal method for determining the structure of the graph, including
        vertices, edges, walls, and their positions. May be called frequently
        to ensure that the graph is built correctly
        """
        if not self.start_location == None:
            self.reset_lists()
            self.bfs(self.start_location)
            self.mark_walls()

    def reset_lists(self):
        """
        Removes all elements from self.adj and self.rev and defaults them to
        empty twice-indicied lists.
        """
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
        """
        Sets up a recursive call to compute the bfs of the graph starting from
        the start point, usually self.start_location
        """
        self.bfs_recursive([start], [])

    def bfs_recursive(self, queue, visited):
        """
        Computes the breadth first search of the graph, taking the first element
        from the queue, moving in all directions with it, and if it discovers
        a vertex not in the queue and not visited, adds it to the back of the
        queue. After traversing all directions, that first element is added to
        visited. If the queue is empty, we have visited every vertex, and
        visited now holds a list of all vertices. Therefore we assign to the
        vertices field the visited list.
        """
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

    def fastest_path(self):
        """
        Computes the length of the fastest path to get from the start
        location to any valid ending location, including those above
        the specified end_location.
        """
        x = self.end_location[0]
        y = self.end_location[1]
        v = self.vertices_x(x)
        list = []
        for i in v:
            if i[1] <= y:
                list.append(i)
        return self.shortest_paths(self.start_location, list )

    def shortest_path(self, start, end):
        """
        Returns the fewest number of moves required to get from start to end
        by using a bfs strategy.
        """
        if start in self.vertices and end in self.vertices:
            if start == end:
                return 0
            distance = 1
            visited = [start]
            queue = [start]
            while len(queue) > 0:
                next = []
                for i in queue:
                    neighbors = self.adj[i[0]][i[1]]
                    for j in neighbors:
                        if not j in visited:
                            if j == end:
                                return distance
                            if not i == j:
                                next.append(j)
                            visited.append(j)
                queue = next
                distance = distance + 1
            return None
        else:
            return None

    def shortest_paths(self, start, ends):
        """
        Returns the fewest number of moves required to get from start to
        any of the vertices in ends by using a bfs strategy.
        """
        if start in self.vertices:
            if start in ends:
                return 0
            distance = 1
            visited = [start]
            queue = [start]
            while len(queue) > 0:
                next = []
                for i in queue:
                    neighbors = self.adj[i[0]][i[1]]
                    for j in neighbors:
                        if not j in visited:
                            if j in ends:
                                return distance
                            if not i == j:
                                next.append(j)
                            visited.append(j)
                queue = next
                distance = distance + 1
            return None
        else:
            return None

    def vertices_x(self, x):
        """
        Returns all points in the vertices list which
        have the corresponding x value passed in
        """
        list = []
        for v in self.vertices:
            if x == v[0]:
                list.append(v)
        return list

    def vertices_y(self, y):
        """
        Returns all points in the vertices list which
        have the corresponding y value passed in
        """
        list = []
        for v in self.vertices:
            if y == v[1]:
                list.append(v)
        return list

    def add_to_lists(self, f, t):
        """
        Given a from point and a to point, adds them to the adjacency list
        and reverse list. Ideally this will get called when creating a new
        path and connecting the two vertices in the graph.
        """
        adj = self.adj[f[0]][f[1]]
        new_adj = add_if_missing(t, adj)
        self.adj[f[0]][f[1]] = new_adj
        rev = self.rev[t[0]][t[1]]
        new_rev = add_if_missing(f, rev)
        self.rev[t[0]][t[1]] = new_rev

    def move(self, f, direction):
        """
        Starting at a point f, this algorithm will iteratively move in
        a cardinal direction until it reaches the edge of the grid or
        interferes with a wall. It returns the stopping point
        (may potentially) also be the same as f.
        """
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

    def mark_walls(self):
        """
        Sets up walls adjacent all vertices, ensuring that no paths outside our
        graph can be traversed, preserving many essential properties of the
        procedurally generating algorithm.
        """
        for p in self.vertices:
            self.mark_walls_p(p)

    def mark_walls_p(self, p):
        """
        Marks walls adjacent to point p (not including diagonals), as walls, if
        they are not already paths. This method usually gets called on a new
        vertex to set up the surrounding blocking walls.
        """
        l = (p[0]-1, p[1])
        r = (p[0]+1, p[1])
        u = (p[0], p[1]-1)
        d = (p[0], p[1]+1)
        # To be modified with other elements potentially later
        if self.is_in_grid(l) and not self.is_path[l[0]][l[1]]:
            self.is_wall[l[0]][l[1]] = True
        if self.is_in_grid(r) and not self.is_path[r[0]][r[1]]:
            self.is_wall[r[0]][r[1]] = True
        if self.is_in_grid(u) and not self.is_path[u[0]][u[1]]:
            self.is_wall[u[0]][u[1]] = True
        if self.is_in_grid(d) and not self.is_path[d[0]][d[1]]:
            self.is_wall[d[0]][d[1]] = True

    def determine_extra_paths(self, rand):
        """
        Pseudorandomly determines which pattern to build additional paths in
        """
        pattern = rand.generate(1,20)
        ranges = []
        if 1 <= pattern < 9:
            ranges = self.tight_range()
            self.keep_walls_row(ranges, rand)
            self.row_interval_assignment(ranges)
        elif 9 <= pattern < 13:
            ranges = self.top_down_range()
            self.keep_walls_row(ranges, rand)
            self.row_interval_assignment(ranges)
        elif 13 <= pattern < 17:
            ranges = self.down_up_range()
            self.keep_walls_row(ranges, rand)
            self.row_interval_assignment(ranges)
        elif 17 <= pattern < 19:
            ranges = self.left_right_range()
            self.keep_walls_column(ranges, rand)
            self.column_interval_assignment(ranges)
        else:
            ranges = self.right_left_range()
            self.keep_walls_column(ranges, rand)
            self.column_interval_assignment(ranges)

    def top_down_range(self):
        """
        Creates a non-shrinking list of ranges that encapsulate the walls and
        paths at each height, starting at the top and fitting it in the
        tightest range possible but never decreasing the bounds of the range
        """
        min = self.width - 1
        max = 0
        ranges = []
        for i in range(self.height):
            for j in range(self.width):
                if self.is_path[j][i] or self.is_wall[j][i]:
                    min = j if j < min else min
                    max = j if j > max else max
            ranges.append((min,max))
        return ranges

    def down_up_range(self):
        """
        Creates a non-growing list of ranges that encapsulates the walls and
        paths at each height, starting from the bottom, fitting it in the
        tightest range possible, then working its way to the top but never
        decreasing the bounds of the range. Subsequent ranges are inserted
        at the start of the list to preserve order.
        """
        min = self.width - 1
        max = 0
        ranges = []
        for i in range(self.height-1, -1, -1):
            for j in range(self.width):
                if self.is_path[j][i] or self.is_wall[j][i]:
                    min = j if j < min else min
                    max = j if j > max else max
            ranges.insert(0, (min,max))
        return ranges

    def tight_range(self):
        """
        Creates a list of ranges at each height which enclose all walls and paths
        in the tightest manner possible.
        """
        ranges = []
        for i in range(self.height):
            min = self.width - 1
            max = 0
            for j in range(self.width):
                if self.is_path[j][i] or self.is_wall[j][i]:
                    min = j if j < min else min
                    max = j if j > max else max
            ranges.append((min,max))
        return ranges

    def left_right_range(self):
        """
        Creates a non-shrinking list of ranges by starting on the left, finding
        the tightest range enclosing all walls and paths, and computing iteratively
        to increase the bounds of the next range or to repeat the previous ones.
        """
        min = self.height - 1
        max = 0
        ranges = []
        for i in range(self.width):
            for j in range(self.height):
                if self.is_path[i][j] or self.is_wall[i][j]:
                    min = j if j < min else min
                    max = j if j > max else max
            ranges.append((min, max))
        return ranges

    def right_left_range(self):
        """
        Creates a non-growing list of ranges by taking the smallest range
        enclosing the right-most column, and only expanding it as it computes
        the smallest ranges leftward, and inserting the maxima of the previous
        result and the new result at the start of the range list.
        """
        min = self.height - 1
        max = 0
        ranges = []
        for i in range(self.width-1, -1, -1):
            for j in range(self.height):
                if self.is_path[i][j] or self.is_wall[i][j]:
                    min = j if j < min else min
                    max = j if j > max else max
            ranges.insert(0, (min, max))
        return ranges

    def column_interval_assignment(self, ranges):
        """
        Given a list of self.width tuples, converts all non-determined
        grid spaces on the ith height in the range of the ith tuple to paths,
        and converts the remainder (outside the range) to walls.
        """
        for i in range(self.width):
            for j in range(0, ranges[i][0]):
                if not self.is_wall[i][j]:
                    self.is_wall[i][j] = True
                    self.is_unused_wall[i][j] = True
            for j in range(ranges[i][0], ranges[i][1]+1):
                if not self.is_wall[i][j]:
                    if not self.is_path[i][j]:
                        self.is_path[i][j] = True
                        self.is_unused_path[i][j] = True
            for j in range(ranges[i][1]+1, self.width):
                if not self.is_wall[i][j]:
                    self.is_wall[i][j] = True
                    self.is_unused_wall[j][i] = True

    def row_interval_assignment(self, ranges):
        """
        Given a list of self.height tuples, converts all non-determined
        grid spaces on the ith height in the range of the ith tuple to paths,
        and converts the remainder (outside the range) to walls.
        """
        for i in range(self.height):
            for j in range(0, ranges[i][0]):
                if not self.is_wall[j][i]:
                    self.is_wall[j][i] = True
                    self.is_unused_wall[j][i] = True
            for j in range(ranges[i][0], ranges[i][1]+1):
                if not self.is_wall[j][i]:
                    if not self.is_path[j][i]:
                        self.is_path[j][i] = True
                        self.is_unused_path[j][i] = True
            for j in range(ranges[i][1]+1, self.width):
                if not self.is_wall[j][i]:
                    self.is_wall[j][i] = True
                    self.is_unused_wall[j][i] = True

    def keep_walls_row(self, ranges, rand):
        for i in range(self.height):
            for j in range(ranges[i][0], ranges[i][1]+1):
                if not self.is_wall[j][i] and not self.is_path[j][i]:
                    if rand.generate(0, 1) == 1:
                        self.is_wall[j][i] = True

    def keep_walls_column(self, ranges, rand):
        for i in range(self.width):
            for j in range(ranges[i][0], ranges[i][1]+1):
                if not self.is_wall[i][j] and not self.is_path[i][j]:
                    if rand.generate(0,1) == 1:
                        self.is_wall[i][j] = True

    def longest_noninterfering_path(self, f, direction):
        """
        Determines the length of the longest path from, ideally
        another vertex in place, in a direction, without consideration
        of the rest of the part of the graph connecting it, only
        stopping if it will interfere with another vertex as it grows
        outward. That is, if there is already a path going in the exact
        opposite way out of the vertex then this algorithm does not care.
        """
        if self.is_in_grid(f):
            x = f[0]
            y = f[1]
            if not self.is_path[x][y]:
                neighbors = [(x,y+1), (x,y-1), (x+1, y), (x-1, y)]
                for i in neighbors:
                    if i in self.vertices:
                        return None
            if direction == "R":
                length = 0
                while True:
                    if self.is_in_grid((x+1, y)):
                        # If neighbors of the next part of the path are vertices, stop.
                        if self.is_path[x+1][y]:
                            x = x + 1
                            length = length + 1
                            continue
                        elif self.is_in_grid((x+1, y+1)) and (x+1, y+1) in self.vertices:
                            return length
                        elif self.is_in_grid((x+1, y-1)) and (x+1, y-1) in self.vertices:
                            return length
                        elif self.is_in_grid((x+2, y)) and (x+2, y) in self.vertices:
                            return length
                        else:
                            x = x + 1
                            length = length + 1
                    else:
                        return length
            if direction == "L":
                length = 0
                while True:
                    if self.is_in_grid((x-1, y)):
                        # If neighbors of the next part of the path are vertices, stop.
                        if self.is_path[x-1][y]:
                            x = x - 1
                            length = length + 1
                            continue
                        elif self.is_in_grid((x-1, y+1)) and (x-1, y+1) in self.vertices:
                            return length
                        elif self.is_in_grid((x-1, y-1)) and (x-1, y-1) in self.vertices:
                            return length
                        elif self.is_in_grid((x-2, y)) and (x-2, y) in self.vertices:
                            return length
                        else:
                            x = x - 1
                            length = length + 1
                    else:
                        return length
            if direction == "U":
                length = 0
                while True:
                    if self.is_in_grid((x, y-1)):
                        # If neighbors of the next part of the path are vertices, stop.
                        if self.is_path[x][y-1]:
                            y = y - 1
                            length = length + 1
                            continue
                        elif self.is_in_grid((x+1, y-1)) and (x+1, y-1) in self.vertices:
                            return length
                        elif self.is_in_grid((x-1, y-1)) and (x-1, y-1) in self.vertices:
                            return length
                        elif self.is_in_grid((x, y-2)) and (x, y-2) in self.vertices:
                            return length
                        else:
                            y = y - 1
                            length = length + 1
                    else:
                        return length
            if direction == "D":
                length = 0
                while True:
                    if self.is_in_grid((x, y+1)):
                        # If neighbors of the next part of the path are vertices, stop.
                        if self.is_path[x][y+1]:
                            y = y + 1
                            length = length + 1
                            continue
                        elif self.is_in_grid((x+1, y+1)) and (x+1, y+1) in self.vertices:
                            return length
                        elif self.is_in_grid((x-1, y+1)) and (x-1, y+1) in self.vertices:
                            return length
                        elif self.is_in_grid((x, y+2)) and (x, y+2) in self.vertices:
                            return length
                        else:
                            y = y + 1
                            length = length + 1
                    else:
                        return length
        else:
            return None

    #TODO
    def longest_nonintrusive_path(self, f, direction):
        return None

def add_if_missing(element, list):
    """
    Appends an item to a list if it does not exist in the list already
    """
    if not element in list:
        list.append(element)
    return list

def minmax(n1, n2):
    """
    Helper function which returns the min and max of two numbers with one call
    """
    smaller = min(n1, n2)
    larger = max(n1, n2)
    return smaller, larger

def sort_tuples_x(list):
    """
    Sorts a lists of tuples by the value of their first index
    """
    list.sort(key = lambda x: x[0])
    return list

def sort_tuples_y(list):
    """
    Sorts a lists of tuples by the value of their second index
    """
    list.sort(key = lambda x: x[1])
    return list
