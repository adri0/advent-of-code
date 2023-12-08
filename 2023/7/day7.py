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


def read_hands(input_path: str, joker: bool = False) -> list[Hand]:
    with open(input_path) as f:
        return [
            Hand(cards, int(bid), hand_type(cards, joker))
            for cards, bid in (line.strip().split() for line in f.readlines())
        ]


def hand_type(cards: str, joker: bool = False) -> HandType:
    counter = Counter(cards)
    if joker and "J" in counter and len(counter) > 1:
        sorted_counter = sorted(counter.items(), key=lambda i: i[1], reverse=True)
        most_freq = sorted_counter[0][0]
        card_transfer = most_freq if most_freq != "J" else sorted_counter[1][0]
        counter[card_transfer] += counter["J"]
        del counter["J"]
    match sorted(counter.values()):
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


def hand_strength(hand: Hand, strengths=CARD_STRENGTH) -> list[int]:
    return [hand.type.value, *map(strengths.index, hand.cards)]


def part1(input_path: str) -> None:
    hands = read_hands(input_path)
    ranked_hands = sorted(hands, key=hand_strength)
    winnings = (hand.bid * rank for rank, hand in enumerate(ranked_hands, start=1))
    print("Sum of winnings (Part 1):", sum(winnings))


def part2(input_path: str) -> None:
    card_strength = list(CARD_STRENGTH)
    card_strength.remove("J")
    card_strength.insert(0, "J")

    hands = read_hands(input_path, joker=True)
    ranked_hands = sorted(hands, key=lambda hand: hand_strength(hand, card_strength))
    winnings = (hand.bid * rank for rank, hand in enumerate(ranked_hands, start=1))
    print("Sum of winnings (Part 2):", sum(winnings))


if __name__ == "__main__":
    input_path = "input.txt"
    part1(input_path)
    part2(input_path)
