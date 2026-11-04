import threading
import time


class Node:
    def __init__(self, key):
        self.key = key
        self.next = None
        self.lock = threading.Lock()


class FineList:
    def __init__(self):
        self.head = Node(float('-inf'))
        self.head.next = Node(float('inf'))

    def find(self, key):
        pred = self.head
        pred.lock.acquire()
        curr = pred.next
        curr.lock.acquire()
        while curr.key < key:
            pred.lock.release()
            pred = curr
            curr = curr.next
            curr.lock.acquire()
        return pred, curr

    def add(self, key):
        pred, curr = self.find(key)
        result = False
        if curr.key != key:
            node = Node(key)
            node.next = curr
            pred.next = node
            result = True
        curr.lock.release()
        pred.lock.release()
        return result

    def remove(self, key):
        pred, curr = self.find(key)
        result = False
        if curr.key == key:
            pred.next = curr.next
            result = True
        curr.lock.release()
        pred.lock.release()
        return result

    def contains(self, key):
        pred, curr = self.find(key)
        result = curr.key == key
        curr.lock.release()
        pred.lock.release()
        return result

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


s = FineList()
print("Insert:", run(s.add), "ms")
print("Size after insert:", len(s.display()))
print("Search:", run(s.contains), "ms")
print(s.contains(500), s.contains(5000))
print("Delete:", run(s.remove), "ms")
print("Size after delete:", len(s.display()))
print("Time complexity: add, remove, contains = O(n)")
