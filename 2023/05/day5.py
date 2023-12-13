from itertools import chain
from typing import NamedTuple


class Map(NamedTuple):
    name: str
    source_ranges: list[range]
    dest_offsets: list[int]  # Offset for destination


def read_almanac(path_input: str) -> tuple[list[int], list[Map]]:
    with open(path_input, "r") as f:
        lines = f.readlines()

    seeds = list(map(int, lines[0][lines[0].find(":") + 1 :].strip().split()))

    maps = []
    block_start = 2
    while block_start < len(lines):
        block_end = (
            lines.index("\n", block_start)
            if "\n" in lines[block_start:]
            else len(lines)
        )

        source_ranges = []
        dest_offsets = []
        name = lines[block_start].split(" ")[0]
        for line in lines[block_start + 1 : block_end]:
            dest_start, source_start, length = map(int, line.strip().split())
            source_ranges.append(range(source_start, source_start + length))
            dest_offsets.append(dest_start - source_start)

        map_ = Map(name, source_ranges, dest_offsets)
        maps.append(map_)
        block_start = block_end + 1

    return seeds, maps


def find_seed_location(seed: int, maps: list[Map]) -> int:
    source = seed
    for map_ in maps:
        for i, range_ in enumerate(map_.source_ranges):
            if source in range_:
                dest = source + map_.dest_offsets[i]
                break
        else:
            dest = source
        source = dest
    return dest


def map_ranges(in_ranges: list[range], map_: Map) -> list[range]:
    """Pass a list of ranges through a map, outputs a list of ranges"""
    out_ranges: list[range] = []

    for i, map_range in enumerate(map_.source_ranges):
        offset = map_.dest_offsets[i]
        ranges_left = []
        for in_range in in_ranges:
            if in_range.start in map_range and (in_range.stop - 1) in map_range:
                out_ranges.append(
                    range(in_range.start + offset, in_range.stop + offset)
                )

            elif map_range.start in in_range and (map_range.stop - 1) in in_range:
                out_start = map_range.start + offset
                out_stop = map_range.stop + offset
                out_ranges.append(range(out_start, out_stop))
                ranges_left.append(range(in_range.start, map_range.start))
                ranges_left.append(range(map_range.stop, in_range.stop))

            elif in_range.start in map_range:
                out_start = in_range.start + offset
                out_stop = map_range.stop + offset
                out_ranges.append(range(out_start, out_stop))
                ranges_left.append(range(map_range.stop, in_range.stop))

            elif (in_range.stop - 1) in map_range:
                out_start = map_range.start + offset
                out_stop = in_range.stop + offset
                out_ranges.append(range(out_start, out_stop))
                ranges_left.append(range(in_range.start, map_range.start))

            else:
                ranges_left.append(in_range)

        in_ranges = ranges_left

    out_ranges.extend(in_ranges)
    return out_ranges


def find_seed_range_locations(seed_range: range, maps: list[Map]) -> list[range]:
    out_ranges = [seed_range]
    for map_ in maps:
        out_ranges = map_ranges(out_ranges, map_)
    return out_ranges


def part1(seeds: list[int], maps: list[Map]) -> None:
    min_loc = min(find_seed_location(seed, maps) for seed in seeds)
    print("Min location (part 1)", min_loc)


def part2(seeds: list[int], maps: list[Map]) -> None:
    seed_ranges = [
        range(seeds[n], seeds[n] + seeds[n + 1]) for n in range(0, len(seeds), 2)
    ]
    location_ranges = chain.from_iterable(
        find_seed_range_locations(s, maps) for s in seed_ranges
    )
    min_loc = min(range_.start for range_ in location_ranges)
    print("Min location (part 2)", min_loc)


if __name__ == "__main__":
    seeds, maps = read_almanac("input.txt")
    part1(seeds, maps)
    part2(seeds, maps)
