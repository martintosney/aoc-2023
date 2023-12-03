import fileinput
import re

part_numbers = []
symbols = []

x = 0
for input in fileinput.input():
    schematic_line = input.strip()

    for match in re.finditer("\d+", schematic_line):
        part_numbers.append(
            {
                "part_number": int(match.group()),
                "positions": {(x, y) for y in range(match.start(), match.end())},
            }
        )

    for match in re.finditer("[^\d\.]", schematic_line):
        symbols.append(
            {
                "symbol": match.group(),
                "position": (x, match.start()),
            }
        )

    x += 1


def generate_adjacancies(x, y):
    return [(a_x, a_y) for a_x in range(x - 1, x + 2) for a_y in range(y - 1, y + 2)]


adjacancies = {
    (x, y)
    for symbol in symbols
    for (x, y) in generate_adjacancies(symbol["position"][0], symbol["position"][1])
}

true_part_numbers = [
    part_number["part_number"]
    for part_number in part_numbers
    if len(part_number["positions"].intersection(adjacancies)) > 0
]

print(sum(true_part_numbers))


gear_ratio_total = 0
for symbol in symbols:
    if symbol["symbol"] == "*":
        adj = generate_adjacancies(symbol["position"][0], symbol["position"][1])
        adjacent_parts = []
        for part_number in part_numbers:
            if len(part_number["positions"].intersection(adj)) > 0:
                adjacent_parts.append(part_number["part_number"])
        if len(adjacent_parts) == 2:
            gear_ratio_total += adjacent_parts[0] * adjacent_parts[1]

print(gear_ratio_total)
