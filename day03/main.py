import fileinput
import re

part_numbers = []
symbols = []
set({})

x = 0
for input in fileinput.input():
    schematic_line = input.strip()

    for match in re.finditer("\d+", schematic_line):
        part_numbers.append(
            {
                "part_number": match.group(),
                "positions": {(x, y) for y in range(match.start(), match.end())},
            }
        )

    for match in re.finditer("[^\d\.]", schematic_line):
        symbols.append((x, match.start()))

    x += 1

adjancies = {
    (x, y)
    for symbol in symbols
    for x in range(symbol[0] - 1, symbol[0] + 2)
    for y in range(symbol[1] - 1, symbol[1] + 2)
}

true_part_numbers = [
    int(part_number["part_number"])
    for part_number in part_numbers
    if len(part_number["positions"].intersection(adjancies)) > 0
]

print(part_numbers)
print(symbols)
print(adjancies)
print(true_part_numbers)
print(sum(true_part_numbers))
