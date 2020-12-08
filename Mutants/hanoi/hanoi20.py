def hanoi(height, start=1, end=3):
    steps = []
    if height > 0:
        steps.extend(hanoi(height - 1, start, ({1, 2, 3} - {start} - {end}).pop()))
        steps.append(start, end)
        steps.extend(hanoi(height - 1, ({1, 2, 3} - {start} - {end}).pop(), end))

    return steps