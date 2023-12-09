import fileinput


def expand_universe(starting_universe):
    empty_cols = []
    for x in reversed(range(len(starting_universe[0]))):
        if not [y[x] for y in starting_universe if y[x] != "."]:
            empty_cols.append(x)

    expanded_universe = []
    for row in starting_universe:
        new_row = row.copy()
        for col in empty_cols:
            new_row.insert(col, ".")
        expanded_universe.append(new_row)

    for y, row in reversed(list(enumerate(expanded_universe))):
        if not [c for c in row if c != "."]:
            expanded_universe.insert(y, row)

    return expanded_universe


input = [list(i.strip()) for i in fileinput.input()]

uni = expand_universe(input)

galaxies = [
    (x, y) for y, row in enumerate(uni) for x, symbol in enumerate(row) if symbol == "#"
]

total_length = 0
for i, (x1, y1) in enumerate(galaxies):
    for x2, y2 in galaxies[i + 1 :]:
        total_length += abs(x2 - x1) + abs(y2 - y1)

for u in uni:
    print("".join(u))


print(total_length)
