import threading
import time


class Node:
    def __init__(self, key):
        self.key = key
        self.next = None


class CoarseList:
    def __init__(self):
        self.head = Node(float('-inf'))
        self.head.next = Node(float('inf'))
        self.lock = threading.Lock()

    def find(self, key):
        pred = self.head
        curr = pred.next
        while curr.key < key:
            pred = curr
            curr = curr.next
        return pred, curr

    def add(self, key):
        with self.lock:
            pred, curr = self.find(key)
            if curr.key == key:
                return False
            node = Node(key)
            node.next = curr
            pred.next = node
            return True

    def remove(self, key):
        with self.lock:
            pred, curr = self.find(key)
            if curr.key != key:
                return False
            pred.next = curr.next
            return True

    def contains(self, key):
        with self.lock:
            pred, curr = self.find(key)
            return curr.key == key

    def display(self):
        result = []
        curr = self.head.next
        while curr.key != float('inf'):
            result.append(curr.key)
            curr = curr.next
        return result


def work(op, start):
    for k in range(start, start + 250):
        op(k)


def run(op):
    start = time.perf_counter()
    threads = [threading.Thread(target=work, args=(op, i * 250)) for i in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    return round((time.perf_counter() - start) * 1000, 3)


s = CoarseList()
print("Insert:", run(s.add), "ms")
print("Size after insert:", len(s.display()))
print("Search:", run(s.contains), "ms")
print(s.contains(500), s.contains(5000))
print("Delete:", run(s.remove), "ms")
print("Size after delete:", len(s.display()))
print("Time complexity: add, remove, contains = O(n)")
