import threading
import time


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LockStack:
    def __init__(self):
        self.top = None
        self.lock = threading.Lock()

    def push(self, value):
        node = Node(value)
        with self.lock:
            node.next = self.top
            self.top = node

    def pop(self):
        with self.lock:
            if self.top is None:
                raise IndexError("pop from empty stack")
            value = self.top.value
            self.top = self.top.next
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


st = LockStack()
print("Push:", run(st.push), "ms")
print("Top:", st.top.value)
print("Pop:", run(lambda k: st.pop()), "ms")
print("Empty after pop:", st.top is None)
print("Time complexity: push, pop = O(1)")
