#!/usr/bin/env python3
from multiprocessing import Pool, shared_memory

import numpy as np


def square_row(array_shape: tuple[int, int], shm_name: str, i: int):
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    c = np.ndarray(array_shape, dtype=np.int64, buffer=existing_shm.buf)
    print("Squaring row", i)
    c[i] **= 2
    existing_shm.close()


def main():
    a = np.arange(100).reshape((10, 10))
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
    b[:] = a[:]

    print(type(b))
    print(type(a))

    print(shm.name)

    vals = [(a.shape, shm.name, i) for i in range(10)]
    with Pool(8) as pool:
        pool.starmap(square_row, vals)
    print(b)

    shm.close()
    shm.unlink()


if __name__ == "__main__":
    main()
