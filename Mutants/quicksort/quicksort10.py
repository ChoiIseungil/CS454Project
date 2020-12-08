def quicksort(arr):
    if not arr:
        return []

    pivot = arr[-1]
    lesser = quicksort([x for x in arr[:] if x < pivot])
    greater = quicksort([x for x in arr[:] if x >= pivot])
    return lesser + [pivot] + greater