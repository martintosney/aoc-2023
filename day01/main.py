import fileinput
import re

# run from command line as:
#   python3 main.py < sample.txt

words_replaced = [
    i.replace("one", "o1e")
    .replace("two", "t2o")
    .replace("three", "th3ee")
    .replace("four", "f4ur")
    .replace("five", "f5ve")
    .replace("six", "s6x")
    .replace("seven", "se7en")
    .replace("eight", "ei8ht")
    .replace("nine", "n9ne")
    .replace("zero", "z0ro")
    for i in fileinput.input()
]

digit_lists = [re.findall("\d", w) for w in words_replaced]
calibrations = [int("".join(d[0:1] + d[-1::])) for d in digit_lists]
print(sum(calibrations))
