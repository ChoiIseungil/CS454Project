def quicksort(arr):
    if not arr:
        return []

    pivot = arr[0]
    lesser = quicksort([x for x in arr[:] if x <= pivot])
    greater = quicksort([x for x in arr[:] if x > pivot])
    return lesser + greater