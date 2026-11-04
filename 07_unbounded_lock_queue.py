import threading
import time


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class UnboundedQueue:
    def __init__(self):
        self.head = Node(None)
        self.tail = self.head
        self.enq_lock = threading.Lock()
        self.deq_lock = threading.Lock()

    def enqueue(self, value):
        with self.enq_lock:
            node = Node(value)
            self.tail.next = node
            self.tail = node

    def dequeue(self):
        with self.deq_lock:
            if self.head.next is None:
                raise IndexError("dequeue from empty queue")
            value = self.head.next.value
            self.head = self.head.next
            return value


def work(op, start):
    for k in range(start, start + 250):
        op(k)


def run(op):
    start = time.perf_counter()
    threads = [threading.Thread(target=work, args=(op, i * 250)) for i in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    return round((time.perf_counter() - start) * 1000, 3)


q = UnboundedQueue()
print("Enqueue:", run(q.enqueue), "ms")
print("Front:", q.head.next.value)
print("Dequeue:", run(lambda k: q.dequeue()), "ms")
print("Empty after dequeue:", q.head.next is None)
print("Time complexity: enqueue, dequeue = O(1)")
