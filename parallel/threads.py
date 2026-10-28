#!/usr/bin/env python3
import multiprocessing
import threading

a = 1

# True to use multiprocessing, False to use threading
use_multiprocessing = True
if use_multiprocessing:
    cls = multiprocessing.Process
else:
    cls = threading.Thread


def add(n: int):
    global a
    a += n


if __name__ == "__main__":
    t1 = cls(target=add, args=(2,))
    t2 = cls(target=add, args=(3,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(a)
