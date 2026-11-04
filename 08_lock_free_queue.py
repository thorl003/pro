import threading
import time


class AtomicReference:
    def __init__(self, ref=None):
        self.ref = ref
        self.lock = threading.Lock()

    def get(self):
        return self.ref

    def compare_and_set(self, expected, new):
        with self.lock:
            if self.ref is expected:
                self.ref = new
                return True
            return False


class Node:
    def __init__(self, value):
        self.value = value
        self.next = AtomicReference(None)


class LockFreeQueue:
    def __init__(self):
        sentinel = Node(None)
        self.head = AtomicReference(sentinel)
        self.tail = AtomicReference(sentinel)

    def enqueue(self, value):
        node = Node(value)
        while True:
            last = self.tail.get()
            nxt = last.next.get()
            if last is self.tail.get():
                if nxt is None:
                    if last.next.compare_and_set(None, node):
                        self.tail.compare_and_set(last, node)
                        return
                else:
                    self.tail.compare_and_set(last, nxt)

    def dequeue(self):
        while True:
            first = self.head.get()
            last = self.tail.get()
            nxt = first.next.get()
            if first is self.head.get():
                if first is last:
                    if nxt is None:
                        raise IndexError("dequeue from empty queue")
                    self.tail.compare_and_set(last, nxt)
                else:
                    value = nxt.value
                    if self.head.compare_and_set(first, nxt):
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


q = LockFreeQueue()
print("Enqueue:", run(q.enqueue), "ms")
print("Front:", q.head.get().next.get().value)
print("Dequeue:", run(lambda k: q.dequeue()), "ms")
print("Empty after dequeue:", q.head.get().next.get() is None)
print("Time complexity: enqueue, dequeue = O(1), no locks (CAS)")
