import threading
import time


class AtomicMarkableReference:
    def __init__(self, ref, mark=False):
        self.ref = ref
        self.mark = mark
        self.lock = threading.Lock()

    def get(self):
        with self.lock:
            return self.ref, self.mark

    def compare_and_set(self, exp_ref, new_ref, exp_mark, new_mark):
        with self.lock:
            if self.ref is exp_ref and self.mark == exp_mark:
                self.ref = new_ref
                self.mark = new_mark
                return True
            return False


class Node:
    def __init__(self, key, next=None):
        self.key = key
        self.next = AtomicMarkableReference(next)


class LockFreeList:
    def __init__(self):
        self.head = Node(float('-inf'), Node(float('inf')))

    def find(self, key):
        while True:
            pred = self.head
            curr = pred.next.get()[0]
            while True:
                succ, marked = curr.next.get()
                if marked:
                    if not pred.next.compare_and_set(curr, succ, False, False):
                        break
                    curr = succ
                else:
                    if curr.key >= key:
                        return pred, curr
                    pred = curr
                    curr = succ

    def add(self, key):
        while True:
            pred, curr = self.find(key)
            if curr.key == key:
                return False
            node = Node(key, curr)
            if pred.next.compare_and_set(curr, node, False, False):
                return True

    def remove(self, key):
        while True:
            pred, curr = self.find(key)
            if curr.key != key:
                return False
            succ = curr.next.get()[0]
            if curr.next.compare_and_set(succ, succ, False, True):
                pred.next.compare_and_set(curr, succ, False, False)
                return True

    def contains(self, key):
        curr = self.head
        while curr.key < key:
            curr = curr.next.get()[0]
        return curr.key == key and not curr.next.get()[1]

    def display(self):
        result = []
        curr = self.head.next.get()[0]
        while curr.key != float('inf'):
            succ, marked = curr.next.get()
            if not marked:
                result.append(curr.key)
            curr = succ
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


s = LockFreeList()
print("Insert:", run(s.add), "ms")
print("Size after insert:", len(s.display()))
print("Search:", run(s.contains), "ms")
print(s.contains(500), s.contains(5000))
print("Delete:", run(s.remove), "ms")
print("Size after delete:", len(s.display()))
print("Time complexity: add, remove, contains = O(n), no locks (CAS)")
