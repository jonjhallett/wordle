#!/usr/bin/env python3

import random
import sys
from wordle import generate_next_guesses, word_list


def main():
    starter_words = sys.argv[1:]

    sample_words = answer_word_list()
    random.shuffle(sample_words)

    number_of_samples = len(sample_words)

    rounds_histogram = {}
    for actual_word in sample_words[0:number_of_samples]:
        print()
        print(actual_word)
        previous_guesses = []
        rounds = 1
        got_it_in_starter_words = False
        for starter_word in starter_words:
            if starter_word == actual_word:
                print('\nGot it in starter words!')
                got_it_in_starter_words = True
                break
            next_guesses = generate_next_guesses(previous_guesses)
            if len(next_guesses) == 1:
                print('\nBest guess in starter words!')
                got_it_in_starter_words = True
                break
            elif next_guesses[0] == actual_word:
                print('\nGot it in starter words!')
                got_it_in_starter_words = True
                break
            matches = find_matches(actual_word, starter_word)
            print(f' {starter_word} {matches}', end='')
            previous_guesses.append((starter_word, matches))
            rounds += 1
        if not got_it_in_starter_words:
            while True:
                next_guesses = generate_next_guesses(previous_guesses)
                if len(next_guesses) == 0:
                    print('\nFailed!')
                    break
                elif len(next_guesses) == 1:
                    print('\nBest guess!')
                    next_guess = next_guesses[0]
                    break
                else:
                    next_guess = next_guesses[0]
                    if next_guess == actual_word:
                        print('\nGot it!')
                        break
                    matches = find_matches(actual_word, next_guess)
                    print(f' {next_guess} {matches}', end='')
                    previous_guesses.append((next_guess, matches))
                rounds += 1
        rounds_histogram[rounds] = rounds_histogram.get(rounds, 0) + 1
    print_histogram(rounds_histogram, number_of_samples)
    total = 0
    for rounds in rounds_histogram:
        total += rounds_histogram[rounds] * rounds
    print(total / number_of_samples)


def print_histogram(histogram, number_of_samples):
    for n in sorted(histogram):
        print(f'{n:2} ', end='')
        bar_fraction = histogram[n] / number_of_samples
        for i in range(0, int(bar_fraction * 60)):
            print('*', end='')
        print(f' {bar_fraction * 100:2.1f}%')


def find_matches(word, guess):
    matches = []
    word_characters = [ch for ch in word]
    guess_characters = [ch for ch in guess]
    for (i, (word_ch, guess_ch)) in enumerate(zip(word_characters, guess_characters)):
        if word_ch == guess_ch:
            matches.append('G')
            word_characters[i] = ' '
        elif guess_ch in word_characters:
            matches.append(' ')
        else:
            matches.append(' ')

    for i in range(5):
        if matches[i] == 'G':
            continue
        if guess_characters[i] in word_characters:
            matches[i] = 'Y'
            word_characters[word_characters.index(guess_characters[i])] = ' '
        elif matches[i] == ' ':
            matches[i] = 'X'

    return ''.join(matches)


def answer_word_list():
    answer_words = []
    answer_word_file = open('answer_words.txt', 'r')
    for line in answer_word_file:
        word = line.rstrip()
        answer_words.append(word)

    return answer_words


if __name__ == '__main__':
    main()
