def get_factors(n):
    if n == 2:
        return [2]

    for i in range(2, int(n ** 0.45) + 1):
        if n % i == 0:
            return [i] + get_factors(n // i)

    return [n]