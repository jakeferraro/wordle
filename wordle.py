'''
CS 122 Spring 2023 Project 9-2
Author: Jake Ferraro
Credit: realpython.com, freecodecamp.com
Description: Personal Project: Wordle - loops, file paths, dictionaries
'''
import pathlib
import random
import doctest
from string import ascii_letters

def get_random_word(word_list):
    '''selects a random 5-letter word from a list of strings

    >>> get_random_word(['snake', 'worm', 'bug'])
    'SNAKE'
    '''
    words = [
        word.upper()
        for word in word_list
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
    ]

    return random.choice(words)

def show_guess(guess, word):
    '''shows the user's guess on the terminal, classifies letters

    >>> show_guess('CRANE', 'SNAKE')
    Correct letters: A, E
    Misplaced letters: N
    Wrong letters: C, R
    '''
    if guess == word:
        print('Correct!')
        return
    
    correct_letters = {
        letter for letter, correct in zip(guess, word) if letter == correct
    }
    misplaced_letters = set(guess) & set(word) -  correct_letters
    wrong_letters = set(guess) - set(word)

    print('Correct letters:', ', '.join(sorted(correct_letters)))
    print('Misplaced letters:', ', '.join(sorted(misplaced_letters)))
    print('Wrong letters:', ', '.join(sorted(wrong_letters)))

    return

def game_over(word):
    '''prints the word once the game has ended

    >>> game_over('SNAKE')
    The word was SNAKE
    '''
    print(f'The word was {word}')

def main():
    '''top-level function'''
    words_path = pathlib.Path('wordlist.txt')
    word = get_random_word(words_path.read_text(encoding='utf-8').split('\n'))
    print(word)

    for guess_num in range(1, 7):
        guess = input(f'\nGuess {guess_num}: ').upper()

        show_guess(guess, word)
        if guess == word:
            break

    else:
        game_over(word)

    return

main()

print(doctest.testmod())
