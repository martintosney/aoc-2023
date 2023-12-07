import fileinput
import re

input = [i.strip() for i in fileinput.input()]


def direction_generator(directions):
    while True:
        for d in directions:
            yield d


directions = direction_generator(input[0])

routes = {
    m.group(1): {"L": m.group(2), "R": m.group(3)}
    for m in [re.match("^(.*) = \((.*), (.*)\)", i) for i in input[2::]]
}

locations = [r for r in routes.keys() if r.endswith("A")]
steps = 0
loop = True
while loop:
    next_direction = next(directions)
    steps += 1
    next_round = []
    loop = False
    for l in locations:
        new_location = routes[l][next_direction]
        next_round.append(new_location)
        if not new_location.endswith("Z"):
            loop = True
    locations = next_round



print(steps)
