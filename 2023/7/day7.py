from collections import Counter
from enum import Enum
from typing import NamedTuple

CARD_STRENGTH = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OAK = 4
    FULL_HOUSE = 5
    FOUR_OAK = 6
    FIVE_OAK = 7


class Hand(NamedTuple):
    cards: str
    bid: int
    type: HandType


def read_hands(input_path: str) -> list[Hand]:
    with open(input_path) as f:
        return [
            Hand(cards, int(bid), hand_type(cards))
            for cards, bid in (line.strip().split() for line in f.readlines())
        ]


def hand_type(cards: str) -> HandType:
    match sorted(Counter(cards).values()):
        case [5]:
            return HandType.FIVE_OAK
        case [1, 4]:
            return HandType.FOUR_OAK
        case [2, 3]:
            return HandType.FULL_HOUSE
        case [1, 1, 3]:
            return HandType.THREE_OAK
        case [1, 2, 2]:
            return HandType.TWO_PAIR
        case [1, 1, 1, 2]:
            return HandType.ONE_PAIR
        case [1, 1, 1, 1, 1]:
            return HandType.HIGH_CARD
        case _:
            raise ValueError("Something's wrong")


def hand_strength(hand: Hand) -> list[int]:
    return [hand.type.value, *map(CARD_STRENGTH.index, hand.cards)]


def part1(hands: list[Hand]) -> None:
    ranked_hands = sorted(hands, key=hand_strength)
    winnings = (hand.bid * rank for rank, hand in enumerate(ranked_hands, start=1))
    print("Sum of winnings:", sum(winnings))


if __name__ == "__main__":
    hands = read_hands("input.txt")
    part1(hands)
