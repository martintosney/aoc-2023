import fileinput
import re

# run from command line as:
#   python3 main.py < sample.txt

NUM_CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def parse_game_number(game_number_text: str):
    return int(game_number_text.split(' ')[1])

def parse_games(games_text: str):
    cube_results = [
        cube_text.split(' ')
        for game in games_text.split('; ')
        for cube_text in game.split(', ')
    ]

    max_results = {}

    for result in cube_results:
        if len(result) == 2:
            (cube_count, cube_colour) = result
            if cube_colour not in max_results.keys():
                max_results[cube_colour] = int(cube_count)
            elif max_results[cube_colour] < int(cube_count):
                max_results[cube_colour] = int(cube_count)

    return max_results

def parse_game(game_string: str):
    game_number_text, game_results_text = game_string.split(': ')

    return {
        "game_number": parse_game_number(game_number_text),
        "totals": parse_games(game_results_text)
    }

def is_valid_game(game_result, available_cubes):
    for (colour, count) in game_result["totals"].items():
        if available_cubes.get(colour, 0) < count:
            return False

    return True

def sum_possible_games(game_strings):
    possible_games = [
        g["game_number"]
        for g in [parse_game(game_string) for game_string in game_strings]
        if is_valid_game(g, NUM_CUBES)
    ]

    return sum(possible_games)

input = [i.strip() for i in fileinput.input()]
print(sum_possible_games(input))