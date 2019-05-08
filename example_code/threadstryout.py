from queue import Empty
from queue import Full
from queue import Queue
from threading import Thread

# all timeouts in seconds
q = Queue(maxsize=10)


class ProducerThread(Thread):

    def run(self):
        for i in range(0, 100):
            try:
                q.put("item{}".format(i), block=True, timeout=0.1)
                print(q.qsize())
                print(q.queue)
            except Full as exception:
                print("Exception ignored: Queue full")


class ConsumerThread(Thread):
    def run(self):
        for i in range(0, 100):
            try:
                q.get(block=True, timeout=0.1)
                print(q.qsize())
                print(q.queue)
            except Empty as exception:
                print("Exception ignored: Queue empty")


print(q.qsize())
print(q.queue)

consumer_thread = ConsumerThread()
producer_thread = ProducerThread()

producer_thread.start()
consumer_thread.start()

print(q.qsize())
print(q.queue)

producer_thread.join()
consumer_thread.join()

print(q.qsize())
print(q.queue)
