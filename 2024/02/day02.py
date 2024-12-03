def part1(input_path: str) -> None:
    with open(input_path, "r") as f:
        safe = 0
        for i, line in enumerate(f, start=1):
            report = [int(e) for e in line.split()]
            cur = report[0]
            diffs = []
            for level in report[1:]:
                prev = cur
                cur = level
                diff = cur - prev
                diffs.append(diff)
            if (sum(1 <= d <= 3 for d in diffs) > len(diffs) - 1) or (
                sum(-3 <= d <= -1 for d in diffs) > len(diffs) - 1
            ):
                safe += 1

    print(f"safe: {safe}")


if __name__ == "__main__":
    part1("02/sample_input.txt")
