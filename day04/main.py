import fileinput
import re


def determine_matches(card_text):
    match = re.match("Card +\d+:(( +\d+)+) \|(( +\d+)+)", card_text)
    winning_numbers = set([int(i) for i in match.group(1).split(" ") if i != ""])
    card_numbers = set([int(i) for i in match.group(3).split(" ") if i != ""])
    return len(card_numbers.intersection(winning_numbers))


def calc_score(card_text):
    matching_nums = determine_matches(card_text)
    return 0 if matching_nums == 0 else 2 ** (matching_nums - 1)


input = [i.strip() for i in fileinput.input()]

print(sum([calc_score(i) for i in input]))

max_card = len(input)

card_copies = {i: 1 for i in range(1, max_card + 1)}

for card_num in range(1, max_card + 1):
    num_matches = determine_matches(input[card_num - 1])

    for card_won in range(card_num + 1, min(card_num + num_matches, max_card) + 1):
        card_copies[card_won] += card_copies[card_num]

print(sum(card_copies.values()))
