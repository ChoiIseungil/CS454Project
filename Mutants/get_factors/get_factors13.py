def get_factors(n):
    if n == 1:
        return []

    for i in range(2, int(n ** 0.8)):
        if n % i == 0:
            return [i] + get_factors(n // i)

    return [n]