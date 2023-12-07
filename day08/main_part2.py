import fileinput
import itertools
import re

input = [i.strip() for i in fileinput.input()]
directions_text = input[0]


def direction_generator(directions):
    while True:
        for d in directions:
            yield d


routes = {
    m.group(1): {"L": m.group(2), "R": m.group(3)}
    for m in [re.match("^(.*) = \((.*), (.*)\)", i) for i in input[2::]]
}


def find_route(start_location, routes, directions_text):
    directions = direction_generator(directions_text)
    location = start_location
    route = []
    while not location.endswith("Z"):
        location = routes[location][next(directions)]
        route.append(location)
    location = routes[location][next(directions)]
    initial_offset = route.index(location)
    loop_length = len(route) - initial_offset
    return (initial_offset, loop_length)


def generate_termination_states(initial_offset, loop_length):
    position = initial_offset
    while True:
        position += loop_length
        yield position


route_props = [
    find_route(location, routes, directions_text)
    for location in routes.keys()
    if location.endswith("A")
]


def find_common_route_length(route_props):
    highest_loop_length_index = max(enumerate(route_props), key=lambda x: x[1][1])[0]
    route_iter = route_props.pop(highest_loop_length_index)

    for route_length in generate_termination_states(*route_iter):
        routes_match = True
        for other_route_offset, other_route_loop_length in route_props:
            if (route_length - other_route_offset) % other_route_loop_length != 0:
                routes_match = False
                break

        if routes_match:
            return route_length


print(find_common_route_length(route_props))
