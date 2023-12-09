import fileinput


def get_universe_expansions(universe):
    empty_cols = []
    for x in range(len(universe[0])):
        if not [y[x] for y in universe if y[x] != "."]:
            empty_cols.append(x)

    empty_rows = []
    for y, row in enumerate(universe):
        if not [c for c in row if c != "."]:
            empty_rows.append(y)

    return (empty_cols, empty_rows)


def sum_lengths(universe, ratio=2):
    galaxies = [
        (x, y)
        for y, row in enumerate(universe)
        for x, symbol in enumerate(row)
        if symbol == "#"
    ]

    galaxies = [(x, y) for x, y in galaxies]

    (expand_cols, expand_rows) = get_universe_expansions(universe)

    total_length = 0
    for i, (x1, y1) in enumerate(galaxies):
        for x2, y2 in galaxies[i + 1 :]:
            delta_x = abs(x2 - x1) + (
                (ratio - 1)
                * len([x for x in expand_cols if min(x1, x2) < x < max(x1, x2)])
            )
            delta_y = abs(y2 - y1) + (
                (ratio - 1)
                * len([y for y in expand_rows if min(y1, y2) < y < max(y1, y2)])
            )
            total_length += delta_x + delta_y
    return total_length


input = [list(i.strip()) for i in fileinput.input()]


print(f"Part 1: {sum_lengths(input)}")

print(f"Part 2: {sum_lengths(input, 1000000)}")
