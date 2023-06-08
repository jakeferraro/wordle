# WORDLE clone

import contextlib
import pathlib
import random
from string import ascii_letters, ascii_uppercase
from rich.console import Console
from rich.theme import Theme

console = Console(width = 40, theme = Theme({"warning": "red on yellow"}))

num_letters = 5
num_guesses = 6
words_path = pathlib.Path("wordlist.txt")



def refresh_page(headline):
    console.clear()
    console.rule(f"{headline}\n")

    return

def get_random_word(word_list):
    if words := [
        word.upper()
        for word in word_list
        if len(word) == num_letters and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(words)
    else:
        console.print(f"No words of length {num_letters} in the word list", style = "warning")
        raise SystemExit()

    return

def guess_word(previous_guesses):
    guess = console.input("\nGuess word: ").upper()

    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}.", style = "warning")
        return guess_word(previous_guesses)

    if len(guess) != num_letters:
        console.print(f"Your guess must be {num_letters} letters.", style = "warning")
        return guess_word(previous_guesses)

    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(
            f"Invalid letter: '{invalid}'. Please use English letters.",
            style = "warning",
        )
        return guess_word(previous_guesses)
    
    return guess

def show_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")
            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"

        console.print("".join(styled_guess), justify = "center")
    console.print("\n" + "".join(letter_status.values()), justify = "center")

    return

def game_over(guesses, word, guessed_correctly):
    refresh_page(headline = "Game Over")
    show_guesses(guesses, word)

    if guessed_correctly:
        console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
    else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")

def main():
    """top-level function"""
    word = get_random_word(words_path.read_text(encoding="utf-8").split("\n"))
    guesses = ["_" * num_letters] * num_guesses

    with contextlib.suppress(KeyboardInterrupt):
        for idx in range(num_guesses):
            refresh_page(headline = f"Guess {idx + 1}")
            show_guesses(guesses, word)

            guesses[idx] = guess_word(previous_guesses = guesses[:idx])
            if guesses[idx] == word:
                break

    game_over(guesses, word, guessed_correctly=guesses[idx] == word)

    return

main()
