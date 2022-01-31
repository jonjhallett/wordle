#!/usr/bin/env python3

from math import log
import os
import re
import string
import sys


def main():
    guesses = parse_arguments()

    next_guesses = generate_next_guesses(guesses)
    for word in next_guesses:
        print(word)


def generate_next_guesses(guesses):
    round = len(guesses) + 1
    (guess_pattern, all_seen_characters, must_haves) = guess(guesses)

    next_guesses = search_space_reduction_sorted_words(all_seen_characters)

    best_guesses = []
    for word in next_guesses:
        if re.search(f'^{guess_pattern}$', word):
            if includes_must_haves(word, must_haves):
                best_guesses.append(word)

    if len(best_guesses) == 1 or round > 2:
        return best_guesses
    else:
        return next_guesses


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


def includes_must_haves(word, must_haves):
    return all([ch in word for ch in must_haves])


def set_of_characters_in_list(list_of_strings):
    set_of_characters = set()
    for s in list_of_strings:
        set_of_characters.update([ch for ch in s])
    return set_of_characters


def guess(guesses):
    guess_words = [guess[0] for guess in guesses]
    all_seen_characters = set_of_characters_in_list(guess_words)

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
                include_characters.add(guess_character)
            elif match_character == 'Y':
                match_pattern_characters_exclude[i].add(guess_character)
                include_characters.add(guess_character)
            elif match_character == 'X':
                exclude_characters.add(guess_character)

    exclude_characters |= all_seen_characters - include_characters

    match_pattern_exclude_set = exclude_characters - set('.')
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

    return (match_pattern, all_seen_characters, include_characters)


search_space_reduction = {}


def total_search_space_reducation(word, all_seen_characters):
    average_search_space_reduction = sum([search_space_reduction[ch]
                                         for ch in word])
    number_of_unique_characters = len(set([ch for ch in word]))
    lack_of_diversity_penalty = (5 - number_of_unique_characters) * 200
    seen_before_penalty = sum([200 for ch in word if ch
                              in all_seen_characters])
    vowel_penalty = sum([100 for ch in word if ch
                         in ['a', 'e', 'i', 'o', 'u', 'y']])
    return average_search_space_reduction + lack_of_diversity_penalty + \
        seen_before_penalty + vowel_penalty


words = []


def word_list():
    global words
    if not words:
        read_words_file(words)

    return words


def search_space_reduction_sorted_words(all_seen_characters):
    words = word_list()

    global search_space_reduction
    if not search_space_reduction:
        search_space_reduction = calculate_search_space_reduction(words)
    return sorted(words,
                  key=lambda word: total_search_space_reducation(
                                     word,
                                     all_seen_characters))


def read_words_file(words):
    words_file = open('words.txt', 'r')
    for line in words_file:
        word = line.rstrip()
        words.append(word)


def calculate_search_space_reduction(words):
    words_with_character = {}
    character_total = {}
    total = 0
    for word in words:
        characters_in_word = [ch for ch in word]
        for ch in characters_in_word:
            character_total[ch] = character_total.get(ch, 0) + 1
            total += 1
        for ch in set(characters_in_word):
            words_with_character[ch] = words_with_character.get(ch, 0) + 1

    character_probability = {}
    for ch in character_total:
        character_probability[ch] = character_total[ch] / total

    search_space_reduction = {}
    for ch in words_with_character:
        search_space_reduction[ch] = words_with_character.get(ch, 0) \
                                        / len(words)

    average_search_space_reduction = {}
    for ch in words_with_character:
        average_search_space_reduction[ch] = \
                character_probability[ch] * search_space_reduction[ch] + \
                (1 - character_probability[ch]) * \
                (1 - search_space_reduction[ch])

    return average_search_space_reduction


if __name__ == '__main__':
    main()
