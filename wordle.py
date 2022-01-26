#!/usr/bin/env python3

from math import log
import os
import re
import string
import sys


def main():
    guesses = parse_arguments()

    (guess_pattern, all_seen_characters) = guess(guesses)

    words = entropy_sorted_words_file(all_seen_characters)
    for word in words:
        if re.search(f'^{guess_pattern}$', word):
            print(word)


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
    all_seen_characters = set_of_characters_in_list(words)

    match_pattern_characters = ['.', '.', '.', '.', '.']
    match_pattern_characters_exclude = [set(), set(), set(), set(), set()]
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
                match_pattern_characters_exclude[i] |= set(guess_character)
                include_characters.add(guess_character)
            elif match_character == 'X':
                exclude_characters.add(guess_character)

    exclude_characters |= all_seen_characters - include_characters

    match_pattern_exclude_set = exclude_characters \
        | set(match_pattern_characters) \
        - set('.')
    alphabet_set = set([ch for ch in string.ascii_lowercase])
    match_pattern_include_set = alphabet_set - match_pattern_exclude_set


    match_pattern = ''
    for i in range(0, 5):
        position_include_set = match_pattern_include_set - \
                               match_pattern_characters_exclude[i]
        match_pattern_include_string = ''.join(sorted(position_include_set))
        match_pattern_include_re = f'[{match_pattern_include_string}]'
        if match_pattern_characters[i] == '.':
            match_pattern += match_pattern_include_re
        else:
            match_pattern += match_pattern_characters[i]

    return (match_pattern, all_seen_characters)


character_entropy = {}


def total_character_entropy(word, all_seen_characters):
    entropy = sum([character_entropy[ch] for ch in word])
    number_of_unique_characters = len(set([ch for ch in word]))
    lack_of_diversity_penalty = (5 - number_of_unique_characters) * 100
    seen_before_penalty = sum([100 for ch in word if ch in all_seen_characters])
    return entropy + lack_of_diversity_penalty + seen_before_penalty


def entropy_sorted_words_file(all_seen_characters):
    words = []
    read_words_file(words)
    character_entropy = calculate_character_entropy(words)
    return sorted(words, key=lambda word: total_character_entropy(word,
                                            all_seen_characters))


def read_words_file(words):
    words_file = open('words.txt', 'r')
    for line in words_file:
        word = line.rstrip()
        words.append(word)


def calculate_character_entropy(words):
    character_frequency = {}
    total = 0
    for word in words:
        for ch in [ch for ch in word]:
            character_frequency[ch] = character_frequency.get(ch, 0) + 1
            total += 1

    for ch in character_frequency:
        character_entropy[ch] = -log(character_frequency[ch] / total) / log(2)

    return character_entropy


main()
