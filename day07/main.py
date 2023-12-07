from enum import Enum
import fileinput
import functools
import itertools


RANK_ORDER = "123456789TJQKA"
RANKS = {rank: value for value, rank in zip(range(2, 2 + len(RANK_ORDER)), RANK_ORDER)}


@functools.total_ordering
class Hand:
    _HIGH_CARD = 1
    _ONE_PAIR = 2
    _TWO_PAIR = 3
    _THREE_OF_A_KIND = 4
    _FULL_HOUSE = 5
    _FOUR_OF_A_KIND = 6
    _FIVE_OF_A_KIND = 7

    def __init__(self, cards: str, bid: int):
        self._cards = cards
        self._bid = bid
        self._card_values = [RANKS[card] for card in cards]
        self._card_groups = sorted(
            [
                (len(list(g)), k)
                for k, g in itertools.groupby(sorted(self._card_values))
            ],
            reverse=True,
        )

    def bid(self):
        return self._bid

    def card_values(self):
        return self._card_values

    def rank(self):
        if self._card_groups[0][0] == 5:
            return self._FIVE_OF_A_KIND
        if self._card_groups[0][0] == 4:
            return self._FOUR_OF_A_KIND
        if self._card_groups[0][0] == 3 and self._card_groups[1][0] == 2:
            return self._FULL_HOUSE
        if self._card_groups[0][0] == 3:
            return self._THREE_OF_A_KIND
        if self._card_groups[0][0] == 2 and self._card_groups[1][0] == 2:
            return self._TWO_PAIR
        if self._card_groups[0][0] == 2:
            return self._ONE_PAIR

        return self._HIGH_CARD

    def _compare_to_hand(self, other):
        our_rank = (self.rank(), self.card_values())
        their_rank = (other.rank(), other.card_values())
        if our_rank > their_rank:
            return 1
        elif their_rank > our_rank:
            return -1
        else:
            return 0

    def __repr__(self):
        return str((self._cards, self._bid))

    def __eq__(self, other):
        return self._compare_to_hand(other) == 0

    def __lt__(self, other):
        return self._compare_to_hand(other) < 0


input = [i.strip() for i in fileinput.input()]
hands = [Hand(cards, int(bid)) for cards, bid in [i.split(" ") for i in input]]

total_value = sum(
    [pos * hand.bid() for pos, hand in zip(range(1, 1 + len(hands)), sorted(hands))]
)

print(total_value)
