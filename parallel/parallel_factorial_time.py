#!/usr/bin/env python3
import os
import time
from math import ceil, prod
from multiprocessing import Pool


def chunk_range(n: int, processes: int) -> list[tuple[int, int]]:
    chunk_size = ceil(n / processes)
    chunks = [
        (i * chunk_size + 1, min(n, (i + 1) * chunk_size)) for i in range(processes)
    ]
    return chunks


def perm(k: int, n: int) -> int:
    p = 1
    for i in range(k, n + 1):
        p *= i
    return p


def parallel_factorial(n: int, processes: int) -> int:
    chunks = chunk_range(n, processes)
    with Pool(processes) as pool:
        result_pieces = pool.starmap(perm, chunks)
    return prod(result_pieces)


if __name__ == "__main__":
    n = 10000
    procs = os.cpu_count()
    start = time.monotonic()
    x1 = parallel_factorial(n, 1)
    end = time.monotonic()
    print("Serial execution:", end - start)
    start = time.monotonic()
    x2 = parallel_factorial(n, procs)
    end = time.monotonic()
    print("Parallel across", procs, "CPUs:", end - start)
