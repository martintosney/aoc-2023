import fileinput
import re

# run from command line a:
#   python3 main.py < sample.txt

digit_lists = [
    re.findall("\d", i)
    for i in fileinput.input()
]

calibrations = [
    int(''.join(d[0:1] + d[-1::]))
    for d in digit_lists
]

print(sum(calibrations))