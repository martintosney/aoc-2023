import fileinput
import math

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

NEXT_DIRECTION = {
    NORTH: {
        '|': NORTH,
        '7': WEST,
        'F': EAST,
    },
    SOUTH: {
        '|': SOUTH,
        'L': EAST,
        'J': WEST,
    },
    EAST: {
        'J': NORTH,
        '-': EAST,
        '7': SOUTH,
    },
    WEST: {
        '-': WEST,
        'L': NORTH,
        'F': SOUTH, 
    },
}

START = 'S'

map = [list(i.strip()) for i in fileinput.input()]

map_height = len(map)
map_width = len(map)

start = [
    (x, y)
    for x, line in enumerate(map)
    for y, symbol in enumerate(line)
    if symbol == START
][0]

if start[0] > 0 and map[start[0]-1][start[1]] in NEXT_DIRECTION[NORTH].keys():
    direction = NORTH
elif start[0] < map_height-1 and map[start[0]+1][start[1]] in NEXT_DIRECTION[SOUTH].keys():
    direction = SOUTH
elif start[1] > 0 and map[start[0]][start[1]-1] in NEXT_DIRECTION[WEST].keys():
    direction = WEST    
elif start[1] < map_width-1 and map[start[0]][start[1]+1] in NEXT_DIRECTION[EAST].keys():
    direction = EAST

position = start
pipe = []
while True:
    position = (position[0] + direction[0], position[1] + direction[1])
    symbol = map[position[0]][position[1]]
    if symbol == START:
        break
    pipe.append(position)
    direction = NEXT_DIRECTION[direction][symbol]

print(math.ceil(len(pipe)/2))