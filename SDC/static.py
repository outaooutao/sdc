__author__ = 'outao'
import LRU
import CLOCK

l = {"LRU": LRU, "CLOCK": CLOCK}


class staticCache:
    def __init__(self, c):
        self.c = c  # cachesize
        self.hitcount = 0
        self.stored = {}
        self.count = 0

    def get(self, key):
        self.count += 1
        if key in self.stored:
            self.hitcount += 1
            return 1
        return 0

    def show(self):
        for k in self.stored:
            print k


def keyFunc(item):
    return item[1]


class sdCache:
    def __init__(self, c, f, logfile, algn, query_file):
        self.query_file = query_file  # test set
        self.count = 0  # query count
        self.filename = logfile  # train set
        self.table = {}
        self.trainset = []  # (query,frequency)
        self.sCache = staticCache(c * f)
        alg_module = l[algn]
        self.c = c  # cache size
        self.alg = alg_module.alg(self.c - self.sCache.c)


    def fill(self):
        logfile = open(self.filename)
        line = logfile.readline()
        while line:
            query = int(line)
            if query in self.table:
                item = self.table[query]
                item[1] += 1
            else:
                item = [query, 1]
                self.table[query] = item
                self.trainset.append(item)
            line = logfile.readline()

        logfile.close()
        self.trainset.sort(key=keyFunc, reverse=True)
        i = 0
        while i < self.sCache.c:
            self.sCache.stored[self.trainset[i][0]] = 1
            i += 1

        while i < self.c:
            self.alg.put(self.trainset[i][0])
            i += 1

    def warm_up(self):
        pass

    def cache_test(self):
        qf = open(self.query_file)
        line = qf.readline()
        while line:
            query = int(line)
            self.count += 1
            if self.sCache.get(query):
                pass
            elif self.alg.get(query):
                pass
            else:
                self.alg.put(query)
            line = qf.readline()

    def print_statistics(self):
        print "query count:", self.count
        print "static cache hit:", self.sCache.hitcount
        print "dynamic cache try:", self.alg.count
        print "dynamic cache hit:", self.alg.hitcount
        print "hit rate:", 1.0 * (self.sCache.hitcount + self.alg.hitcount) / self.count


test = sdCache(10, 0.4, 'training.txt', "LRU", "test.txt")
test.fill()
test.sCache.show()
test.cache_test()
test.print_statistics()
