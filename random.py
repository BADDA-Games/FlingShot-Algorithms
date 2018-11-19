class RandomSeed:

    def __init__(self, seed):
        self.seed = seed
        self.initial_seed = seed

    def generate(self, low, high):
        mod = high - low + 1
        if self.seed < 1: # Either 0 or negative, out of bounds due to a bad initial seed probably
            self.seed =  ( (low + high - self.seed + 1999) * 1582307 ) % 55555333
        self.seed = (3515366 * self.seed + 12345) % 99999989
        value = (self.seed % mod) + low
        return value
