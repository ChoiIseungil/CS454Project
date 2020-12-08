def quicksort(arr):
    if not arr:
        return []

    pivot = arr[random.randrange(0,len(arr))]
    lesser = quicksort([x for x in arr[:] if x < pivot])
    greater = quicksort([x for x in arr[:] if x > pivot])
    return lesser + [pivot] + greater