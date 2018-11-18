class RandomSeed:

    def __init__(self, seed):
        self.seed = seed
        self.initial_seed = seed

    def generate(self, low, high):
        mod = high - low + 1
        if self.seed < 1: # Either 0 or negative, out of bounds due to a bad initial seed probably
            self.seed =  ( (low + high - self.seed + 1999) * 1582307 ) % 55555333
        self.seed = (1103515245 * self.seed + 12345) % 99999989
        value = (self.seed % mod) + low
        return value

    def cycle_length(self):
        self.seed = self.initial_seed
        self.generate(self.generate(1,10),self.generate(11,25))
        count = 1
        while not self.seed == self.initial_seed:
            self.generate(self.generate(1,10),self.generate(11,25))
            count = count + 1
            if count % 100000 == 0:
                print count
        return count
