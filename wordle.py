import random
import string

# --- Word list (5-letter) — keep it small for speed; add more if you like ---
WORDS = [
    "apple","grape","pearl","plane","crane","stone","chili","spice","sugar","honey",
    "bread","smile","track","focus","brain","river","ocean","earth","cloud","flame",
    "cable","light","sound","dream","plain","chair","table","pride","glove","shark"
]

# ANSI colors for terminal
RESET = "\033[0m"
GREEN = "\033[92m"   # correct
YELLOW = "\033[93m"  # present
GRAY = "\033[90m"    # absent
BOLD = "\033[1m"

def pick_secret() -> str:
    return random.choice(WORDS)

def valid_guess(s: str) -> bool:
    return len(s) == 5 and all(ch in string.ascii_letters for ch in s)

def evaluate_guess(secret: str, guess: str):
    """
    Returns a list of statuses for each letter: 'correct', 'present', 'absent'.
    Handles duplicate letters using a letter-count dictionary.
    """
    secret = secret.lower()
    guess = guess.lower()

    statuses = ["absent"] * 5
    # Count letters in secret
    counts = {}
    for ch in secret:
        counts[ch] = counts.get(ch, 0) + 1

    # First pass: mark correct positions
    for i, ch in enumerate(guess):
        if ch == secret[i]:
            statuses[i] = "correct"
            counts[ch] -= 1

    # Second pass: mark present (wrong position) if counts left
    for i, ch in enumerate(guess):
        if statuses[i] == "correct":
            continue
        if ch in counts and counts[ch] > 0:
            statuses[i] = "present"
            counts[ch] -= 1
        else:
            statuses[i] = "absent"

    return statuses

def colorize(letter: str, status: str) -> str:
    if status == "correct":
        return f"{GREEN}{BOLD}{letter.upper()}{RESET}"
    if status == "present":
        return f"{YELLOW}{BOLD}{letter.upper()}{RESET}"
    return f"{GRAY}{BOLD}{letter.upper()}{RESET}"

def print_board(history):
    """
    history: list of tuples (guess, statuses_list)
    Prints each row with colored letters.
    """
    for guess, statuses in history:
        row = " ".join(colorize(ch, st) for ch, st in zip(guess, statuses))
        print(row)

def play_round():
    secret = pick_secret()
    attempts = 6
    history = []

    print(f"{BOLD}Wordle (Terminal) — guess the 5-letter word!{RESET}")
    print("Green=correct • Yellow=present • Gray=not in word")
    # Uncomment for debugging/teaching: print("DEBUG secret:", secret)

    try:
        for turn in range(1, attempts + 1):
            guess = input(f"\nGuess {turn}/{attempts}: ").strip().lower()

            if not valid_guess(guess):
                print("❌ Please enter exactly 5 letters (A–Z).")
                continue

            statuses = evaluate_guess(secret, guess)
            history.append((guess, statuses))
            print_board(history)

            if guess == secret:
                print(f"\n🎉 Nice! You got it in {turn} {'try' if turn==1 else 'tries'}.")
                return True

        print(f"\n💥 Out of tries. The word was: {BOLD}{secret.upper()}{RESET}")
        return False

    except KeyboardInterrupt:
        print("\n\n(Interrupted)")
        return False

def main():
    print("Press Ctrl+C to exit at any time.")
    wins = 0
    games = 0
    while True:
        result = play_round()
        games += 1
        wins += int(result)
        # Simple stats dictionary
        stats = {"games": games, "wins": wins, "win_rate": f"{(wins/games*100):.0f}%"}
        print(f"\nStats: {stats}")
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
