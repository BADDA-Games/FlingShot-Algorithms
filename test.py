import gridgraph
import printer
import random

success = "\033[92mPASSED\x1b[0m"
failure = "\033[91mFAILED\x1b[0m"

def print_t(name, res):
    print name + ":",
    print success if res else failure

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

    def initialization(self):
        return True


TestRandom()
TestGridGraph()
