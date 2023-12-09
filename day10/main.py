import fileinput
import math
import re

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

NEXT_DIRECTION = {
    NORTH: {
        "|": NORTH,
        "7": WEST,
        "F": EAST,
    },
    SOUTH: {
        "|": SOUTH,
        "L": EAST,
        "J": WEST,
    },
    EAST: {
        "J": NORTH,
        "-": EAST,
        "7": SOUTH,
    },
    WEST: {
        "-": WEST,
        "L": NORTH,
        "F": SOUTH,
    },
}

START = "S"

map = [list(i.strip()) for i in fileinput.input()]

map_height = len(map)
map_width = len(map[0])

start = [
    (y, x)
    for y, line in enumerate(map)
    for x, symbol in enumerate(line)
    if symbol == START
][0]

if start[0] > 0 and map[start[0] - 1][start[1]] in NEXT_DIRECTION[NORTH].keys():
    start_direction = NORTH
elif (
    start[0] < map_height - 1
    and map[start[0] + 1][start[1]] in NEXT_DIRECTION[SOUTH].keys()
):
    start_direction = SOUTH
elif start[1] > 0 and map[start[0]][start[1] - 1] in NEXT_DIRECTION[WEST].keys():
    start_direction = WEST
elif (
    start[1] < map_width - 1
    and map[start[0]][start[1] + 1] in NEXT_DIRECTION[EAST].keys()
):
    start_direction = EAST

position = start
direction = start_direction
pipe = []
while True:
    position = (position[0] + direction[0], position[1] + direction[1])
    symbol = map[position[0]][position[1]]
    if symbol == START:
        break
    pipe.append(position)
    direction = NEXT_DIRECTION[direction][symbol]

end_direction = direction

print(f"Part 1: {math.ceil(len(pipe)/2)}")


# For part 2, we will scan each line and track when we've crossed a "boundary" to
# determine if we have started to enclose a space.
#
# To start with, clean up our map by removing any rubbish characters that aren't
# related to our pipe loop. Also replace the S with a more appropriate character.

full_pipe = [start] + pipe

if start_direction in [NORTH, SOUTH] and start_direction == end_direction:
    s_character = "|"
elif start_direction in [EAST, WEST] and start_direction == end_direction:
    s_character = "-"
elif start_direction in [NORTH, EAST] and end_direction in [NORTH, EAST]:
    s_character = "F"
elif start_direction in [SOUTH, WEST] and end_direction in [SOUTH, WEST]:
    s_character = "J"
elif start_direction in [SOUTH, EAST] and end_direction in [SOUTH, EAST]:
    s_character = "L"
elif start_direction in [NORTH, WEST] and end_direction in [NORTH, WEST]:
    s_character = "7"

for y, line in enumerate(map):
    for x, symbol in enumerate(line):
        if (y, x) not in full_pipe:
            map[y][x] = "."
        elif symbol == "S":
            map[y][x] = s_character

# Next, identify sequences that represent crossing a boundary. This could be
# a simple vertical line:
#
#                 |
#  ...............|..................
#   <outside>     |   <now inside>
#
# Or a Z-shaped line:
#             |
#  ...........L----7...............
#   <outside>      |  <now inside>
#
# A U-shape, however, is not considered crossing a boundary:
#
#             |                                  |
#  ...........|...........F----7.................|...........
#   <outside> | <inside>  |    | <still inside>  |  <outside>

enclosed_spaces = []

for y, line in enumerate(map):
    matches = re.finditer("(L-*7|F-*J|\|)", "".join(line))
    inside_pipe = False
    last_pipe_pos = 0
    for m in matches:
        if not inside_pipe:
            last_pipe_pos = m.end() - 1
        else:
            for x in range(last_pipe_pos + 1, m.start()):
                if map[y][x] == ".":
                    enclosed_spaces.append((y, x))
        inside_pipe = not inside_pipe

print(f"Part 2: {len(enclosed_spaces)}")
