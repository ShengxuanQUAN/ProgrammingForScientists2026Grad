def recursive_sum(n: int):
    if n > 1:
        return n + recursive_sum(n - 1)
    else:
        return 1


print(recursive_sum(6))


def rec_fib(n: int):
    if n == 0 or n == 1:
        return 1
    else:
        return rec_fib(n - 1) + rec_fib(n - 2)


def fib(n):
    if n < 2:
        return 1
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


print([fib(i) for i in range(10)])
