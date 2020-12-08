def quicksort(arr):
    if not arr:
        return []

    i = random.randrange(0,len(arr))
    pivot = arr[i]
    arr2 = arr[:i] + arr[i+1:]
    lesser = quicksort([x for x in arr2[:] if x < pivot])
    greater = quicksort([x for x in arr2[:] if x >= pivot])
    return lesser + [pivot] + greater