from queue import Empty
from queue import Full
from queue import Queue

# all timeouts in seconds
q = Queue(maxsize=10)
q.put("item0", block=True, timeout=0.1)
q.put("item1", block=True, timeout=0.1)
q.put("item2")
q.put("item3")
q.put("item4")
q.put("item5")
q.put("item6")
q.put("item7")
q.put("item8")
q.put("item9")
try:
    q.put("itemX", block=True, timeout=0.1)
except Full as exception:
    print("Exception ignored: Queue full")
print(q.qsize())
print(q.queue)

for i in range(0, 10):
    q.get()
try:
    q.get(block=True, timeout=0.1)
except Empty as exception:
    print("Exception ignored: Queue empty")
print(q.qsize())
print(q.queue)
