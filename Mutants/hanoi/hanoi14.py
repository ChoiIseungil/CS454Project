def hanoi(height, start=1, end=3):
    steps = []
    steps.append((start, end))
    if height > 1:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.extend(hanoi(height - 1, helper, end))

    return steps