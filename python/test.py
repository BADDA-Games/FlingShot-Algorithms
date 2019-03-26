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

    def cyclical(self):
        # TODO test if random generate creates cycles < 5000
        return True

class TestGridGraph:

    def __init__(self):
        print_t("GridGraph initialization is correct", self.initialization())
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
        assert len(G.vertices) == 1, "Vertices initialized with (width//2, height-1)"
        assert len(G.is_path) == width, "Path has incorrect width"
        assert len(G.is_unused_path) == width, "Path has incorrect width"
        assert len(G.is_wall) == width, "Wall has incorrect width"
        assert len(G.is_unused_wall) == width, "Unused wall has incorrect width"
        return True

    def define_locations(self):
        width = 9
        height = 16
        G = gridgraph.GridGraph(width, height)
        assert G.is_wall[4][14] == True
        assert G.is_wall[5][15] == True
        assert G.is_wall[3][15] == True
        assert G.is_path[4][15] == True
        assert G.is_path[4][14] == False
        assert G.is_path[5][15] == False
        assert G.is_path[3][15] == False
        assert G.is_wall[4][15] == False
        assert G.is_path[4][0] == True
        return True

TestRandom()
TestGridGraph()
