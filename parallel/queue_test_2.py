#!/usr/bin/env python3
from multiprocessing import Process, Queue
from os import getpid
from queue import Empty


def f(q: Queue):
    while True:
        try:
            value = q.get(timeout=1)
            print(getpid(), "Got value", value)
        except Empty:
            print(getpid(), "Empty queue; returning")
            return
        new_value = value - 1
        if new_value >= 0:
            print(getpid(), "Adding new value", new_value)
            q.put(new_value)


if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=f, args=(q,))
    p2 = Process(target=f, args=(q,))
    p1.start()
    p2.start()
    print("Parent PID:", getpid())
    for i in range(100):
        q.put(i)
    p1.join()
    p2.join()
