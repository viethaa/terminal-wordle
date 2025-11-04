import random   # Allows us to pick a random secret word

# --- List of possible secret words ---
WORDS = [
    "apple", "grape", "plane", "stone", "spice", "sugar", "honey", "bread", "flame", "light",
    "brick", "cloud", "dream", "field", "glove", "heart", "jelly", "knife", "lemon", "mango",
    "night", "oasis", "pearl", "queen", "river", "stone", "table", "unity", "vivid", "whale", "xenon", "yacht",
    "zebra", "bloom", "charm", "daisy", "ember", "frost", "glide", "harpy", "ivory", "jewel",
    "karma", "lunar", "mirth", "novae", "optic", "plush", "quilt", "rover", "siren", "tiger", "ultra",
    "vapor", "waltz", "xerox", "yodel", "zesty", "brave", "crisp", "dwell", "eager", "fable",
    "gloom", "hover", "inbox", "jumpy", "knack", "latch", "motel", "noble", "orbit", "piano", "quark",
    "rally", "shark", "tango", "unite", "vivid", "witty", "xylem", "yummy", "zonal", "adore",
    "bliss", "crown", "drape", "elbow", "flick", "grind", "hatch", "index", "jolly", "kneel",
    "smile", "track", "focus", "brain", "river", "ocean", "earth", "cloud"
]

# --- Text color codes for terminal output ---
# These change how letters look on the screen (color + bold)
RESET = "\033[0m"
GREEN = "\033[92m"   # Correct letter, correct position
YELLOW = "\033[93m"  # Correct letter, wrong position
GRAY = "\033[90m"    # Letter not in word
BOLD = "\033[1m"

# -------------------------------------------------
# Function: colorize(letter, status)
# Purpose: return the letter with the correct color
# -------------------------------------------------
def colorize(letter, status):
    if status == "correct":
        return f"{GREEN}{BOLD}{letter.upper()}{RESET}"
    if status == "present":
        return f"{YELLOW}{BOLD}{letter.upper()}{RESET}"
    return f"{GRAY}{BOLD}{letter.upper()}{RESET}"


# -------------------------------------------------
# Function: evaluate(secret, guess)
# Purpose: check each letter of the guess
#          - correct spot -> green
#          - wrong spot but in word -> yellow
#          - not in word -> gray
# Returns: list like ["correct", "present", "absent", ...]
# -------------------------------------------------
def evaluate(secret, guess):
    result = ["absent"] * 5   # Start with all letters marked as "absent"
    secret_counts = {}        # Dictionary to count letters in secret word

    # Count each letter in secret word
    for c in secret:  # Loop through each letter in the secret word
        secret_counts[c] = secret_counts.get(c, 0) + 1

    # First pass: check correct letters in the correct position
    for i in range(5):  # Loop through every letter position 0-4
        if guess[i] == secret[i]:      # If the letter matches exactly
            result[i] = "correct"
            secret_counts[guess[i]] -= 1  # Reduce available count for that letter

    # Second pass: check letters that exist in the word but in the wrong place
    for i in range(5):
        if result[i] == "correct":
            continue  # Skip letters we already marked correct
        if guess[i] in secret_counts and secret_counts[guess[i]] > 0:
            result[i] = "present"     # Mark as yellow
            secret_counts[guess[i]] -= 1

    return result


# -------------------------------------------------
# Function: play()
# Purpose: run one full round of Wordle (6 guesses)
# Returns: True if player wins, False if loses
# -------------------------------------------------
def play():
    secret = random.choice(WORDS)   # Choose random secret word
    history = []  # Stores past guesses and results

    print(f"{BOLD}WORDLE — Guess the 5-letter word!{RESET}")
    print("(Green = correct, Yellow = wrong place, Gray = not in word)")

    # Loop for 6 guesses
    for turn in range(1, 7):
        guess = input(f"\nGuess {turn}/6: ").lower()

        # Check input validity
        if len(guess) != 5 or not guess.isalpha():
            print("❌ Enter exactly 5 letters.")
            continue  # Ask again without losing a turn

        # Check guess vs secret
        result = evaluate(secret, guess)
        history.append((guess, result))

        # Print all previous guesses with colors
        for g, r in history:  # Loop through all saved guesses
            print(" ".join(colorize(c, s) for c, s in zip(g, r)))

        # If guess is correct → win
        if guess == secret:
            print(f"\n🎉 You got it in {turn} tries!")
            return True

    # If all 6 guesses used → loss
    print(f"\n💥 Out of tries! The word was {BOLD}{secret.upper()}{RESET}")
    return False


# -------------------------------------------------
# Function: main()
# Purpose: run the game repeatedly until player stops
# Tracks games played and win rate
# -------------------------------------------------
def main():
    games, wins = 0, 0
    print("Press Ctrl+C to quit.")

    # Infinite loop until player chooses to stop
    while True:
        if play():  # If player won
            wins += 1
        games += 1

        # Show stats
        print(f"\nGames: {games}, Wins: {wins}, Win Rate: {wins/games*100:.0f}%")

        # Ask if player wants to continue
        if input("\nPlay again? (y/n): ").lower() != "y":
            print("Thanks for playing!")
            break


# -------------------------------------------------
# Start the game if this file is run directly
# -------------------------------------------------
if __name__ == "__main__":
    main()
