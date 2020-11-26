def get_mutScore():
    with open("mutScore.txt", "r") as f:
        lines = f.readlines()
    if len(lines) == 0:
        print("error")
        return 0

    s = lines[0].strip()

    with open("mutScore.txt", "w") as f:
        for i in range(1, len(lines)):
            f.write(lines[i])

    mutationSocre = float(s)
    print(mutationSocre)
    return mutationSocre

if __name__== "__main__":
    get_mutScore()