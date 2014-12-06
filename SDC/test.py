__author__ = 'outao'
import heapq

item = [1, 2, 3]
myHeap = []
heapq.heappush(myHeap,item)
stored = {}
stored[1] = item
item[2]=100
print stored[1][2]
item=heapq.heappop(myHeap)
print item