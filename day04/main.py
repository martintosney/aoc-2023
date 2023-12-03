import fileinput
import re


def calc_score(card_text):
    match = re.match("Card +\d+:(( +\d+)+) \|(( +\d+)+)", card_text)
    winning_numbers = set([int(i) for i in match.group(1).split(" ") if i != ""])
    card_numbers = set([int(i) for i in match.group(3).split(" ") if i != ""])
    matching_nums = len(card_numbers.intersection(winning_numbers))
    return 0 if matching_nums == 0 else 2 ** (matching_nums - 1)


input = [i.strip() for i in fileinput.input()]

print(sum([calc_score(i) for i in input]))
