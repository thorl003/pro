import threading
import time


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class BoundedQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.size_lock = threading.Lock()
        self.head = Node(None)
        self.tail = self.head
        self.enq_lock = threading.Lock()
        self.deq_lock = threading.Lock()
        self.not_full = threading.Condition(self.enq_lock)
        self.not_empty = threading.Condition(self.deq_lock)

    def get_and_add(self, delta):
        with self.size_lock:
            old = self.size
            self.size += delta
            return old

    def enqueue(self, value):
        wake_deq = False
        with self.enq_lock:
            while self.size == self.capacity:
                self.not_full.wait()
            node = Node(value)
            self.tail.next = node
            self.tail = node
            if self.get_and_add(1) == 0:
                wake_deq = True
        if wake_deq:
            with self.deq_lock:
                self.not_empty.notify_all()

    def dequeue(self):
        wake_enq = False
        with self.deq_lock:
            while self.size == 0:
                self.not_empty.wait()
            value = self.head.next.value
            self.head = self.head.next
            if self.get_and_add(-1) == self.capacity:
                wake_enq = True
        if wake_enq:
            with self.enq_lock:
                self.not_full.notify_all()
        return value


def producer(q):
    for k in range(250):
        q.enqueue(k)


def consumer(q):
    for k in range(250):
        q.dequeue()


q = BoundedQueue(10)
start = time.perf_counter()
threads = [threading.Thread(target=producer, args=(q,)) for i in range(4)]
threads += [threading.Thread(target=consumer, args=(q,)) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print("Enqueue + Dequeue (4 producers, 4 consumers):", round((time.perf_counter() - start) * 1000, 3), "ms")
print("Size at end:", q.size)
print("Time complexity: enqueue, dequeue = O(1), waits when full or empty")
