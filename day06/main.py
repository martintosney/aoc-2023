import fileinput
import math
import re


input = [i.strip() for i in fileinput.input()]

race_results = [
    (int(time), int(distance))
    for time, distance in zip(
        re.findall("\d+", input[0]),
        re.findall("\d+", input[1]),
    )
]

# Quadratic equation time!
#
# c = charge time
# t = total time
# d = distance
#
# The distance we travel is equal to:
#   (t-c)*c = tc - c^2
#
# We want to find where that quadratic equation intersects our horizontal line, representing
# the best-known distance:
#        _
#       / \
# -----/---\-----
#     /     \
#    /       \
#   /         \
#
# So:
#
#   d = tc - c^2
#
# Rearrange to solve for =0:
#
#   c^2 -tc + d = 0
#
# Sub into quadratic formula:
#
#       t ± sqrt(t^2 - 4d)
#   c = ------------------
#              2

product_better_times = 1

for result in race_results:
    t, d = result

    root_part = math.sqrt((t**2) - (4 * d))
    intersection1 = (t + root_part) / 2
    intersection2 = (t - root_part) / 2

    number_better_times = (
        math.floor(intersection1 - 0.00000000001)
        - math.ceil(intersection2 + 0.00000000001)
        + 1
    )
    product_better_times *= number_better_times

print(product_better_times)
