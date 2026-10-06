import random


def hangman():
    print("Welcome to Hangman! 🎉")

    # List of words
    words = ["software", "database", "frontend", "backend", "internet", "hardware", "terminal",
"variable", "function", "compiler", "debugger", "framework", "instance", "argument",
"operator", "iterator", "recursion", "statement", "condition", "interface", "parameter",
"security", "networks", "graphics", "protocol", "metadata", "keyboard", "processor",
"bytecode", "checkbox", "dropdown", "username", "password", "firewall", "database",
"engineer", "designer", "analytic", "solution", "creativity", "learning", "bootcamp",
"document", "tutorial", "resource", "practice", "projects", "feedback", "template",
"standard", "critical", "thinking", "strategy", "exercise", "homework", "question"]

    # Choose a random word
    word = random.choice(words)
    word_letters = set(word)
    guessed_letters = set()
    wrong_guesses = 10

    # Game loop
    while wrong_guesses > 0 and word_letters:
        # Display current progress
        display_word = [letter if letter in guessed_letters else "_" for letter in word]
        print("\nWord: " + " ".join(display_word))
        print(f"Wrong guesses left: {wrong_guesses}")
        print("Guessed letters:", " ".join(sorted(guessed_letters)))

        # Get player input
        guess = input("Guess a letter: ").lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabetic character.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        # Check guess
        if guess in word_letters:
            print("Good guess! ✅")
            guessed_letters.add(guess)
            word_letters.remove(guess)
        else:
            print("Wrong guess! ❌")
            guessed_letters.add(guess)
            wrong_guesses -= 1

    # End of game
    if not word_letters:
        print(f"\nCongratulations! You guessed the word: {word} 🎉")
    else:
        print(f"\nGame Over! The word was: {word} 💀")


if __name__ == "__main__":
    hangman()
