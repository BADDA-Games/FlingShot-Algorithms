import gridgraph
import printer
import random

success = "\033[92mPASSED\x1b[0m"
failure = "\033[91mFAILED\x1b[0m"

def print_t(name, res):
    print success if res else failure,
    print name

class TestRandom:

    def __init__(self):
        print_t("Random generation algorithm returns uniform results", self.uniformity())

    def uniformity(self):
        for i in range(12345678, 12345778):
            r = random.RandomSeed(i)
            arr = [0,0,0,0,0,0,0,0,0,0]
            for _ in range(10000):
                val = r.generate(0,9)
                arr[val] = arr[val] + 1
            for k in range(len(arr)):
                n = arr[k]
                if not 850 <= n <= 1150:
                    return False
        return True

class TestGridGraph:

    def __init__(self):
        print_t("GridGraph initialization is correct", self.initialization())
        print_t("GridGraph copying is correct", self.copy())
        print_t("Defining beginning and end locations works as intended", self.define_locations())

    def initialization(self):
        width = 5
        height = 10
        G = gridgraph.GridGraph(width, height)
        assert width == G.width, "Width does not match input width"
        assert height == G.height, "Height does not match input height"
        assert len(G.adj) == width, "Adjacency list has incorrect width"
        assert len(G.rev) == width, "Reverse list has incorrect width"
        assert len(G.adj[0]) == height, "Adjacency list has incorrect height"
        assert len(G.rev[0]) == height, "Reverse list has incorrect height"
        assert G.vertices == [], "Vertices is not an empty list"
        assert G.start_location == None, "Start location already defined"
        assert G.start_location_defined == False, "Start location already defined"
        assert G.end_location == None, "End location already defined"
        assert G.end_location_defined == False, "End location already defined"
        assert len(G.is_path) == width, "Path has incorrect width"
        assert len(G.is_unused_path) == width, "Path has incorrect width"
        assert len(G.is_vertex) == width, "Vertex has incorrect width"
        assert len(G.is_wall) == width, "Wall has incorrect width"
        assert len(G.is_unused_wall) == width, "Unused wall has incorrect width"
        return True

    def copy(self):
        width = 7
        height = 9
        G = gridgraph.GridGraph(width, height)
        G.define_start_location((3,3))
        O = G.deep_copy()
        assert G.width == O.width, "Widths are not equal"
        assert G.height == O.height, "Heights are not equal"
        assert G.start_location == O.start_location, "Start locations are not equal"
        assert G.start_location_defined == O.start_location_defined, "Start locations defined are not equal"
        assert G.end_location == O.end_location, "End locations are not equal"
        assert G.end_location_defined == O.end_location_defined, "End locations defined are not equal"
        assert G.adj == O.adj, "Adjacency lists are not equal"
        assert G.rev == O.rev, "Reverse lists are not equal"
        assert G.is_path == O.is_path, "is_path lists are not equal"
        assert G.is_unused_path == O.is_unused_path, "Unused path lists are not equal"
        assert G.is_vertex == O.is_vertex, "is_vertex lists are not equal"
        assert G.is_wall == O.is_wall, "is_wall lists are not equal"
        assert G.is_unused_wall == O.is_unused_wall, "is_unused_wall lists are not equal"
        return True

    def define_locations(self):
        width = 7
        height = 9
        G = gridgraph.GridGraph(width, height)
        G.define_start_location((10,10))
        assert G.start_location == None, "Start location should not be defined out of bounds"
        assert G.start_location_defined == False, "Should not flag start defined out of bounds"
        G.define_end_location((-1,4))
        assert G.end_location == None, "End location should not be defined out of bounds"
        assert G.end_location_defined == False, "Should not flag end defined out of bounds"
        G.define_start_location((4,6))
        G.define_end_location((6,1))
        assert G.is_path[4][6] == True
        assert G.is_path[4][5] == False
        assert G.is_path[4][8] == True
        assert G.is_wall[4][5] == True
        assert G.is_wall[5][6] == True
        assert G.is_path[6][1] == True
        assert G.is_path[6][0] == True
        assert G.is_wall[6][2] == True
        return True

TestRandom()
TestGridGraph()
