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

location = "AAA"
steps = 0
while location != "ZZZ":
    location = routes[location][next(directions)]
    steps += 1

print(steps)
