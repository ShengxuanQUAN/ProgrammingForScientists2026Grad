#!/usr/bin/env python3
from math import prod
from multiprocessing import Pool


def perm(k: int, n: int) -> int:
    p = 1
    for i in range(k, n + 1):
        p *= i
    return p


if __name__ == "__main__":
    n = 40
    l = [(1, 20), (21, 40), (41, 60)]
    with Pool(2) as pool:
        results = pool.starmap(perm, l)
    print(prod(results))
