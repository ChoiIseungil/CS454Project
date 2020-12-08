def get_factors(n):
    if n == 0:
        return []

    for i in range(1, int(n ** 0.45) + 1):
        if n % (i + 1) == 0:
            return [i + 1] + get_factors(n // (i + 1))

    return [n]