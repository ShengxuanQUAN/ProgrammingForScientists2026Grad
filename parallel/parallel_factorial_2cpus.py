#!/usr/bin/env python3
from math import ceil, factorial, prod
from multiprocessing import Pool


def perm(k: int, n: int) -> int:
    p = 1
    for i in range(k, n + 1):
        p *= i
    return p


def chunk_range(n: int, processes: int) -> list[tuple[int, int]]:
    chunk_size = ceil(n / processes)
    ranges = []
    for i in range(processes):
        ranges.append(((i * chunk_size + 1), min(n, (i + 1) * chunk_size)))
    return ranges


# def test_chunk_range():
#    n = 50
#    processes = 3
#    results = [(1, 17), (18, 34), (35, 50)]
#    assert chunk_range(n, processes) == results
#    assert chunk_range(50, 2) == [(1, 25), (26, 50)]

# test_chunk_range()


def parallel_factorial(n: int, processes: int) -> int:
    chunks = chunk_range(n, processes)
    print(chunks)
    with Pool(processes) as pool:
        results = pool.starmap(perm, chunks)
    return prod(results)


if __name__ == "__main__":
    print(factorial(10))
    print(parallel_factorial(10, 3))
