RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
PURPLE = [255, 0, 255]
CYAN = [0, 255, 255]
YELLOW = [255, 255, 0]
ORANGE = [255, 127, 0]


def increment_list(start_list, target_list, steps):
    """Turn one list of ints into another in a specified number of steps"""
    
    list_incremented = []

    list_length = (min([len(start_list), len(target_list)]))

    list_incremented.append(start_list)

    for i in range(1, steps):
        list_incremented.append([])

        for j in range(list_length):
            list_incremented[i].append(
                (list_incremented[i - 1][j] - (list_incremented[i - 1][j] - target_list[j]) / (steps - i))
            )

    for i in range(steps):
        for j in range(list_length):
            list_incremented[i][j] = round(list_incremented[i][j])

    return list_incremented


colour_sequence = [RED, GREEN, BLUE, YELLOW, CYAN, PURPLE, ORANGE, RED]

for x in range(len(colour_sequence) - 1):
    print(increment_list(colour_sequence[x], colour_sequence[x + 1], 5))
