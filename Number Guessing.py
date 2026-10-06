import random


def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        # Set the number and attempts
        number = random.randint(1, 100)
        attempts = 10
        guessed = False

        print("\nYou have 10 attempts to guess the number.")

        while attempts > 0 and not guessed:
            try:
                guess = int(input(f"Enter your guess (Attempts left: {attempts}): "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if guess < 1 or guess > 100:
                print("Number must be between 1 and 100.")
                continue

            if guess == number:
                print(f"Congratulations! You guessed the number {number} correctly!")
                guessed = True
            elif guess < number:
                print("Too low!")
            else:
                print("Too high!")

            attempts -= 1

        if not guessed:
            print(f"Sorry! You ran out of attempts. The number was {number}.")

        # Replay option
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    number_guessing_game()