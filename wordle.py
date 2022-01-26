#!/usr/bin/env python3

import os
import re
import string
import sys


def main():
    guesses = parse_arguments()

    if not guesses:
        print('arose')
    elif len(guesses) == 1 and guesses[0][1] == 'GGGGG':
        print(guesses[0][0])
    elif len(guesses) == 1 and guesses[0][1] == 'XXXXX':
        print('until')
    elif len(guesses) == 2 and guesses[0][1] == 'XXXXX' \
            and guesses[1][1] == 'XXXXX':
        print('psych')
    else:
        guess(guesses)


def parse_arguments():
    if len(sys.argv) % 2 != 1:
        raise ValueError('Guesses need to be paired with responses')

    guesses = []

    arguments = iter(sys.argv[1:])
    for guess in arguments:
        matches = next(arguments)
        if not re.search(r'^[a-z]{5}$', guess):
            raise ValueError('Guesses should be five letter words')
        if not re.search(r'^[XYG]{5}$', matches):
            raise ValueError('Matches should be five letters of X, Y or G')
        guesses.append((guess, matches))

    return guesses


def set_of_characters_in_list(list_of_strings):
    set_of_characters = set()
    for s in list_of_strings:
        set_of_characters.update([ch for ch in s])
    return set_of_characters


def guess(guesses):
    words = [guess[0] for guess in guesses]
    all_characters_seen = set_of_characters_in_list(words)

    match_pattern_characters = ['.', '.', '.', '.', '.']
    include_characters = set()
    exclude_characters = set()
    for guess in guesses:
        word = guess[0]
        matches = guess[1]
        for (i, guess_character, match_character) in zip(range(0, 5),
                                                         word,
                                                         matches):
            if match_character == 'G':
                match_pattern_characters[i] = guess_character
            elif match_character == 'Y':
                include_characters.add(guess_character)
            elif match_character == 'X':
                exclude_characters.add(guess_character)

    exclude_characters |= all_characters_seen - include_characters

    match_pattern_exclude_set = exclude_characters \
        | set(match_pattern_characters) \
        - set('.')
    alphabet_set = set([ch for ch in string.ascii_lowercase])
    match_pattern_include_set = alphabet_set - match_pattern_exclude_set

    match_pattern_include_string = ''.join(sorted(match_pattern_include_set))
    match_pattern_include_re = f'[{match_pattern_include_string}]'

    match_pattern = ''.join([match_pattern_include_re if ch == '.' else ch
                             for ch in match_pattern_characters])

    include_greps = ''.join([f" | grep '{ch}'" for ch in include_characters])

    command_string = f"grep '^{match_pattern}$' /usr/share/dict/words" \
                     f"{include_greps}"

    print(command_string)


main()
