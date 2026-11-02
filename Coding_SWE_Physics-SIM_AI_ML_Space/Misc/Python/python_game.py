import random

def guessing_game():
    print("Welcome to the Guessing Game!")
    number_to_guess = random.randint(1, 100)
    guess = None
    attempts = 0

    while guess != number_to_guess:
        guess = int(input("Guess a number between 1 and 100: "))
        attempts += 1
        if guess < number_to_guess:
            print("Too low! Try again.")
        elif guess > number_to_guess:
            print("Too high! Try again.")

    print(f"Congratulations! You've guessed the correct number {number_to_guess} in {attempts} attempts.")

if __name__ == "__main__":
    guessing_game()
