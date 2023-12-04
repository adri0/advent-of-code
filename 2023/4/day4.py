def read_card_matches(input_path: str) -> list[int]:
    cards = []
    with open(input_path, "r") as f:
        for line in f:
            winning = set(
                map(int, line[line.find(":") + 1 : line.find("|")].strip().split())
            )
            have = set(map(int, line[line.find("|") + 1 :].strip().split()))
            cards.append(len(have & winning))
    return cards


def part1(card_matches: list[int]) -> None:
    points = sum(2 ** (n_matches - 1) for n_matches in card_matches if n_matches > 0)
    print("Points part1:", points)


def part2(card_matches: list[int]) -> None:
    n = len(card_matches)
    card_counts = [1] * n

    for card, n_matches in enumerate(card_matches):
        for i in range(card + 1, card + min(n_matches, n) + 1):
            card_counts[i] += card_counts[card]

    print("Total cards part2:", sum(card_counts))


if __name__ == "__main__":
    card_matches = read_card_matches("input.txt")
    part1(card_matches)
    part2(card_matches)
