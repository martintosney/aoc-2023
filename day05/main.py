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
            maps.setdefault(map_from, {}).setdefault("mappings", []).update({
                source: target
                for source, target in zip(
                    range(source_start, source_start + range_length),
                    range(target_start, target_start + range_length),
                )
            })

    return (seeds, maps)


input = [i.strip() for i in fileinput.input()]

(seeds, maps) = parse_almanac(input)

print(maps)

locations = []
for seed in seeds:
    resource_type = 'seed'
    current_value = seed
    while resource_type != 'location':
        current_value = maps[resource_type]["mappings"].get(current_value ,current_value)
        resource_type = maps[resource_type]["target"]
        print(f"{resource_type}: {current_value}")
    locations.append(current_value)

#print(locations[2])
print(locations)
print(min(locations))