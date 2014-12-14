__author__ = 'outao'
import LRU
import CLOCK
import LFU
import LIRS
import OPT
import RANDOM
import SkLRU
import kRANDOM_LRU
import ARC





l = {"LRU": LRU, "CLOCK": CLOCK, "LFU":LFU, "LIRS":LIRS, "OPT":OPT, "RANDOM":RANDOM, "SKLRU":SkLRU, "kRANDOM_LRU":kRANDOM_LRU, "ARC":ARC}


class staticCache:
    def __init__(self, c):
        self.c = c  # cachesize
        self.hitcount = 0
        self.stored = {}
        self.count = 0

    def get(self, key, warm=0):
        if not warm:
            self.count += 1
        if key in self.stored:
            if not warm:
                self.hitcount += 1
            return 1
        return 0

    def show(self):
        for k in self.stored:
            print k


def keyFunc(item):
    return item[1]


class sdCache:
    def __init__(self, c, f, logfile, algn, query_file, k=0,sort_query='sort.txt'):
        self.query_file = query_file  # test set
        self.count = 0  # query count
        self.filename = logfile  # train set
        self.table = {}
        self.trainset = []  # (query,frequency)
        self.sCache = staticCache(c * f)
        self.algn=algn
        alg_module = l[algn]
        self.c = c  # cache size
        self.alg = alg_module.alg(self.c - self.sCache.c, k=k)
        self.sort_query=sort_query

    def fill(self):
        logfile = open(self.sort_query)
        lines = logfile.readlines()
        i = 0
        while i < self.sCache.c:
            self.sCache.stored[int(lines[i])] = 1
            i += 1
        if self.algn == "OPT":
            set_line = []
            tf = open(self.filename)
            lines = tf.readlines()
            tf.close()
            for line in lines:
                query = int(line)
                ret = self.sCache.get(query, warm=1)
                if not ret:
                    set_line.append(line)
            qf = open(self.query_file)
            lines = qf.readlines()
            qf.close()
            for line in lines:
                query = int(line)
                ret = self.sCache.get(query, warm=1)
                if not ret:
                    set_line.append(line)
            self.alg.setup(set_line)

    def warm_up(self):
        tf = open(self.filename)
        lines = tf.readlines()
        tf.close()
        for line in lines:
            query = int(line)
            ret = self.sCache.get(query, warm=1)
            if not ret:
                dret=self.alg.get(query, warm=1)
                if not dret:
                    self.alg.put(query)


    def cache_test(self):
        qf = open(self.query_file)
        lines = qf.readlines()
        qf.close()
        for line in lines:
            query = int(line)
            self.count += 1
            if self.sCache.get(query):
                pass
            elif self.alg.get(query):
                pass
            else:
                self.alg.put(query)


    def print_statistics(self):
        print "query count:", self.count
        print "static cache hit:", self.sCache.hitcount
        print "dynamic cache try:", self.alg.count
        print "dynamic cache hit:", self.alg.hitcount
        print "hit rate:", 1.0 * (self.sCache.hitcount + self.alg.hitcount) / self.count

def pre_handler(filename,output):
        logfile = open(filename)
        line = logfile.readline()
        table = {}
        tops = []
        while line:
            query = int(line)
            if query in table:
                item = table[query]
                item[1] += 1
            else:
                item = [query, 1]
                table[query] = item
                tops.append(item)
            line = logfile.readline()
        logfile.close()
        tops.sort(key=keyFunc, reverse=True)
        text=""
        for item in tops:
            text += str(item[0])
            text += '\n'
        out_file=open(output,'w')
        out_file.write(text)
        out_file.close()

#pre_handler('training.txt','sort.txt')
test = sdCache(10, 0.4, 'training.txt', "OPT", "test.txt")
test.fill()
test.warm_up()
#test.sCache.show()
test.cache_test()
test.print_statistics()
#print test.trainset