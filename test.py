import gridgraph
import printer
import random

success = "\033[92mPASSED\x1b[0m"
failure = "\033[91mFAILED\x1b[0m"

def random_tests():
    print "Random generation algorithm returns uniform results:",
    for i in range(12345678, 12346678):
        r = random.RandomSeed(i)
        arr = [0,0,0,0,0,0,0,0,0,0]
        for _ in range(10000):
            val = r.generate(0,9)
            arr[val] = arr[val] + 1
        for k in range(len(arr)):
            n = arr[k]
            if not 850 <= n <= 1150:
                print failure
                return
    print success

random_tests()
