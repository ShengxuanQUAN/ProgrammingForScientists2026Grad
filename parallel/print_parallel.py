#!/usr/bin/env python3
from multiprocessing import Lock, Pool
from random import random

lock = Lock()


def print_square(i: int):
    sq = i**2
    with lock:
        print(lock)
        print(f"{i} ** 2 = {sq}")


def main():
    numbers = [random() for _ in range(1000)]
    with Pool(8) as pool:
        pool.map(print_square, numbers)


if __name__ == "__main__":
    main()
