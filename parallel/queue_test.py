#!/usr/bin/env python3
from multiprocessing import Process, Queue
from random import randint


def f(q):
    q.put([randint(0, 10) for _ in range(1_000_000)])


if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=f, args=(q,))
    p2 = Process(target=f, args=(q,))
    p1.start()
    p2.start()
    # print(len(q.get()))
    # print(len(q.get()))
    p1.join()
    p2.join()
