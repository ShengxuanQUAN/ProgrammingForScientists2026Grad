#!/usr/bin/env python3
from multiprocessing import Pool
from random import random
from time import monotonic, sleep


def f(x):
    sleep(random() * 5)
    return x, x * x


if __name__ == "__main__":
    # start = monotonic()
    # print(list(map(f, range(10))))
    # end = monotonic()
    # print('Elapsed:', end - start)

    # with Pool(5) as pool:
    #    start = monotonic()
    #    print(pool.map(f, range(10)))
    #    end = monotonic()
    #    print('Elapsed:', end - start)

    with Pool(5) as pool:
        start = monotonic()
        for result in pool.imap_unordered(f, range(10)):
            print(result)
        end = monotonic()
        print("Elapsed:", end - start)
