import fileinput
from enum import Enum
import re

MODES = Enum("MODES", ["SEEDS", "NEW_MAP", "MAP_RANGES"])


def parse_almanac(almanac_text):
    seeds = []
    parse_mode = MODES.SEEDS
    map_from = ""
    map_to = ""
    maps = {}

    for almanac_line in almanac_text:
        if not almanac_line:
            parse_mode = MODES.NEW_MAP
        elif parse_mode == MODES.SEEDS:
            seeds = [int(seed.group()) for seed in re.finditer("\d+", almanac_line)]
        elif parse_mode == MODES.NEW_MAP:
            match = re.match("^(.*)-to-(.*) map:", almanac_line)
            map_from = match.group(1)
            map_to = match.group(2)
            parse_mode = MODES.MAP_RANGES
            maps.setdefault(map_from, {})["target"] = map_to
        elif parse_mode == MODES.MAP_RANGES:
            (target_start, source_start, range_length) = [
                int(seed.group()) for seed in re.finditer("\d+", almanac_line)
            ]
            maps.setdefault(map_from, {}).setdefault("mappings", []).append(
                (
                    source_start,  # Start
                    source_start + range_length - 1,  # End
                    target_start - source_start,  # Delta to apply
                )
            )

    return (seeds, maps)


input = [i.strip() for i in fileinput.input()]

(seeds, maps) = parse_almanac(input)

locations = []
for seed in seeds:
    resource_type = "seed"
    current_value = seed
    while resource_type != "location":
        resource_map = [
            m
            for m in maps[resource_type]["mappings"]
            if m[0] <= current_value and m[1] >= current_value
        ]
        current_value += resource_map[0][2] if resource_map else 0
        resource_type = maps[resource_type]["target"]
    locations.append(current_value)

print(f"Part 1: {min(locations)}")


resource_type = "seed"
resource_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]

while resource_type != "location":
    unmodified_ranges = resource_ranges
    modified_ranges = []

    for m in maps[resource_type]["mappings"]:
        next_batch = []
        for r in unmodified_ranges:
            if r[0] < m[0]:
                next_batch.append((r[0], min(r[1], m[0] - 1)))
            if r[1] >= m[0] and r[0] <= m[1]:
                modified_ranges.append((max(r[0], m[0]) + m[2], min(r[1], m[1]) + m[2]))
            if r[1] > m[1]:
                next_batch.append((max(r[0], m[1] + 1), r[1]))
        unmodified_ranges = next_batch

    resource_ranges = unmodified_ranges + modified_ranges
    resource_type = maps[resource_type]["target"]


min_location = min([r[0] for r in resource_ranges])

print(f"Part 2: {min_location}")
